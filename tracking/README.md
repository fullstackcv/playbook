# Multi-Object Tracking

> Given a video and a detector, match detections across frames into persistent IDs. The "detection + tracker" decomposition is standard; the interesting decision is which tracker on top.

Tracking is usually bolted on top of an object detector (YOLO, RT-DETR). The tracker handles association frame-to-frame — which box in frame T+1 is the same object as which box in frame T. The landscape has consolidated around a few strong choices since 2022.

## Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| **Default** | **[ByteTrack](https://github.com/ifzhang/ByteTrack)** | Fast, robust, very widely used. The 2026 default for most pipelines. |
| With appearance features (ReID) | **[BoT-SORT](https://github.com/NirAharon/BoT-SORT)** | When objects cross/occlude each other a lot and appearance disambiguates |
| Max accuracy (short-term occlusion) | **[OC-SORT](https://github.com/noahcao/OC_SORT)** or **[StrongSORT](https://github.com/dyhBUPT/StrongSORT)** | Research / benchmark submissions |

## Why ByteTrack is the default

Published 2021. The key insight: use *all* detections (including low-confidence ones) for association, not just the high-confidence ones. This makes tracking robust to a detector's confidence dip during partial occlusion. The tracker itself is lightweight (Kalman filter + Hungarian assignment), no ReID network required.

`ByteTrack` + any detector (YOLO is the common pairing). Ships in Ultralytics (`model.track(source, tracker='bytetrack.yaml')`) and in most MOT libraries.

## BoT-SORT — when ReID matters

BoT-SORT adds ReID appearance features on top of ByteTrack's motion model. Objects that look similar stay tied to their IDs across occlusions and crossings. Costs you the ReID inference per track.

Pick this when:
- Multiple similar-looking objects cross each other (sports players, identical vehicles).
- Occlusions longer than a few frames.
- ID-switch rate matters for your downstream task.

## OC-SORT — when you need MOT-benchmark accuracy

Observation-Centric SORT refines the Kalman prediction to better handle non-linear motion and longer occlusions. Historically wins on MOT20. Slightly more complex than ByteTrack; similar compute.

## When to pick something else

- **Single object tracking (SOT)**, one target to follow → different problem entirely. Use **STARK**, **OSTrack**, or **SAM 2** in video-tracking mode. Much higher per-frame compute but you get pixel-accurate masks.
- **Pedestrian-only real-time with ReID**, high-quality ReID training data → **FairMOT** (joint detection + ReID in one net). Dated now but still deployed.
- **Offline video analysis where every frame is available** → re-link tracks globally, not just online. Tools: **TrackEval** benchmark scripts include offline variants.
- **SAM-family for mask tracking** → SAM 2 tracks masks in video natively. Use when you need masks, not just boxes.

## The three questions to narrow

1. **Real-time or offline?** Real-time → ByteTrack. Offline → OC-SORT + global re-linking.
2. **Does appearance disambiguate?** (Similar-looking objects that cross) → BoT-SORT. No → ByteTrack.
3. **Single object or multiple?** Single → STARK/OSTrack/SAM 2. Multiple → ByteTrack family.

## The Dump

- **[SORT (2016)](https://github.com/abewley/sort)** — original Simple Online Realtime Tracking. Kalman + Hungarian. Foundational.
- **[DeepSORT (2017)](https://github.com/nwojke/deep_sort)** — SORT + a ReID network. Historical default for ReID-enhanced tracking.
- **IOU Tracker (2017)** — the absolute simplest tracker — match by bounding box IoU. Surprisingly decent baseline.
- **[FairMOT (2020)](https://github.com/ifzhang/FairMOT)** — joint detection + ReID. Historically strong for pedestrians.
- **[ByteTrack (2021)](https://github.com/ifzhang/ByteTrack)** — the current default. Uses low-confidence detections.
- **[BoT-SORT (2022)](https://github.com/NirAharon/BoT-SORT)** — ByteTrack + ReID.
- **[OC-SORT (2022)](https://github.com/noahcao/OC_SORT)** — observation-centric Kalman.
- **[StrongSORT (2022)](https://github.com/dyhBUPT/StrongSORT)** — modernized DeepSORT with better ReID. Strong in occlusions and camera shifts.
- **[Hybrid-SORT (AAAI 2024)](https://github.com/ymzis69/HybridSORT)** — SOTA heuristic tracker on DanceTrack; also strong on MOT17/20.
- **SolidTrack (2025)** — marginal accuracy win over ByteTrack (80.6 vs ~80.3 MOTA on MOT17). Lower variance across settings. Worth trying if ID-switch rate matters.
- **[MOTR / MOTRv2](https://github.com/megvii-research/MOTRv2) (end-to-end transformer tracker)** — research-register, slower.
- **[BoxMOT (mikel-brostrom)](https://github.com/mikel-brostrom/boxmot)** — Python library bundling multiple modern trackers with a unified interface. Best starting point for prototyping trackers.
- **[OpenMMLab MMTracking](https://github.com/open-mmlab/mmtracking)** — trackers in the MM ecosystem. Has SOT and MOT.
- **[Norfair](https://github.com/tryolabs/norfair)** — lightweight Python tracker library. Simpler than BoxMOT.
- **[Supervision (Roboflow)](https://github.com/roboflow/supervision)** — tracker wrapper on top of YOLO outputs. Makes tracking a 2-line addition to detection.
- **[SAM 2 (video mode)](https://github.com/facebookresearch/sam2)** — mask tracking in video. Different output than box trackers.
- **[STARK](https://github.com/researchmm/Stark) / [OSTrack](https://github.com/botaoye/OSTrack) (single object tracking)** — SOT transformers for one-object scenarios.
- **[Yolov8-track / Ultralytics tracking](https://docs.ultralytics.com/modes/track/)** — one-line ByteTrack or BoT-SORT on top of YOLO.
- **RealSense / depth-aware trackers** — if you have depth, you can improve association. Niche.

## Graveyard

- **DeepSORT as a default** — retired by ByteTrack for most use cases (similar accuracy, no ReID network needed).
- **Classical optical flow trackers (Lucas-Kanade, MedianFlow) as MOT** — retired. Still used for single-frame pixel tracking.
- **Hand-crafted appearance features (HOG/HSV histograms) as ReID** — retired when learned ReID models arrived (~2018).

## Last reviewed

2026-04-22.
