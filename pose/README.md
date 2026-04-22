# Pose Estimation

> Finding keypoints on people (and sometimes hands and faces). The default stack changed in 2023 when RTMPose distilled the ViTPose accuracy into a fast CNN, and again in 2024 as MediaPipe fully replaced OpenPose for browser/mobile.

Pose splits into two deployment flavors — server-side accuracy and on-device real-time — plus a research tier. Different picks for each.

## Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Browser / mobile | **MediaPipe Pose** | JS in the browser, iOS/Android, real-time, no server |
| **Default** | **RTMPose (OpenMMLab)** | Server-side real-time, production accuracy |
| Max accuracy | **ViTPose** | Research benchmarks, offline batch |

## Why RTMPose is the default

Published 2023 by OpenMMLab. Top-down architecture (detect box, then estimate keypoints inside) with a strong training recipe. Hits ViTPose-level accuracy at 5–10× the speed. ONNX-exportable. Ships with COCO and whole-body (COCO-WholeBody: face + body + hand) weights.

`mmpose` is the reference library. Install via `pip install mmpose`. Can be finicky with PyTorch versions; the InsightFace team's `rtmlib` packages RTMPose with fewer dependencies.

## MediaPipe Pose — browser/mobile default

Google's on-device pose library. 33 body keypoints. TFLite-backed, runs in WASM (browser) or native (iOS/Android). ~30 FPS on a modern phone. Accuracy a few points below RTMPose on hard sets but the deployment story is unbeatable for client-side work.

If you're building anything that runs in a browser tab or a phone app without a server, this is your pick.

## When to pick something else

- **Hand pose only** → MediaPipe Hands (21 keypoints per hand) or OpenMMLab's hand-specific RTMPose variant.
- **Whole-body with face + hands in one pass** → RTMPose with COCO-WholeBody weights (133 keypoints total).
- **3D pose from a single image** → MediaPipe Pose already outputs pseudo-3D. For metric 3D, MotionBERT or the MMHuman3D family.
- **Crowded scenes** → bottom-up methods (HRNet bottom-up, DEKR) handle many people better than top-down.
- **Action recognition from pose** → pose first (RTMPose), then a downstream action model (STGCN++, PoseC3D).

## The three questions to narrow

1. **Server or client?** Server → RTMPose. Client → MediaPipe.
2. **Body only or whole-body?** Body only → either pick works. Whole-body → RTMPose with WholeBody weights.
3. **2D or 3D?** 2D → any. Pseudo-3D → MediaPipe. Metric 3D → MotionBERT family.

## The Dump

- **OpenPose (2017)** — the original multi-person pose pipeline. Historical weight, supplanted.
- **HRNet (2019)** — high-resolution network. Still the backbone of many modern pose models.
- **AlphaPose (SJTU)** — strong top-down system. Outpaced by RTMPose.
- **Detectron2 Keypoint R-CNN** — Facebook's keypoint detection in Detectron2. Reasonable but dated.
- **MediaPipe Pose (Google)** — TFLite, 33 keypoints, browser/mobile default.
- **MediaPipe Hands** — 21 keypoints per hand, same ecosystem.
- **MediaPipe Holistic** — body + face + hands together, same shot.
- **DEKR** — bottom-up keypoint regression. Crowded scenes.
- **ViTPose (2022)** — ViT backbone, strong accuracy. Expensive.
- **ViTPose++** — improved training recipe. Same compute class.
- **RTMPose (2023)** — OpenMMLab's distilled real-time pose. The current default.
- **RTMW / RTMO** — whole-body and bottom-up variants from the same team.
- **DWPose (2023)** — distilled whole-body, used as the ControlNet pose preprocessor.
- **MotionBERT** — 3D human motion representation. Strong on video.
- **MMHuman3D (OpenMMLab)** — SMPL body fitting from video.
- **Yolov8-pose / Yolov11-pose (Ultralytics)** — YOLO with a keypoint head. Fast, good ecosystem, less accurate than RTMPose.
- **PoseNet (Google, TFJS)** — the browser default before MediaPipe. Retired.
- **MMPose (OpenMMLab)** — the reference training/inference library for top-down pose.
- **rtmlib** — lightweight wrapper around RTMPose without the MMPose dependency chain.

## Graveyard

- **OpenPose as a production default** — retired ~2020. Licensing (non-commercial for original OpenPose weights) plus slower than modern alternatives.
- **PoseNet in the browser** — retired when MediaPipe Pose launched. Less accurate.
- **Stacked Hourglass (2016)** — historically important, no longer competitive.

## Last reviewed

2026-04-22.
