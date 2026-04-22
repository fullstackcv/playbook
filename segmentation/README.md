# Segmentation

> Pixel-level object boundaries. Three flavors: semantic (pixel → class), instance (pixel → instance), panoptic (both). SAM changed everything in 2023.

Segmentation used to be a painful subtask that required large annotated datasets and task-specific models. SAM (Segment Anything, Meta, 2023) and SAM 2 (video, 2024) reset the field. For most use cases in 2026, the question is *"which SAM-family model"* rather than *"train my own from scratch."*

## Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Edge / mobile | **MobileSAM** or **EfficientSAM** | On-device, low-latency interactive segmentation |
| **Default (zero-shot, concept-prompted)** | **SAM 3 / SAM 3.1** (Meta, Nov 2025 / Mar 2026) | Native text + image exemplar prompts. Doubles SAM 2 accuracy on PCS. Video tracking at 32 FPS. |
| **Default (trained task)** | **Mask2Former** or **YOLO26-seg** | When you have labeled data and want instance segmentation in one pass |
| Max accuracy (research) | **OneFormer** or **SAM 3 with concept prompts** | Research benchmarks |

Segmentation splits into "interactive / zero-shot" and "trained / one-shot" — those are different picks.

## Zero-shot: SAM 3 / SAM 3.1 (current default)

Meta shipped **SAM 3** in November 2025 and **SAM 3.1** in March 2026. The shift from SAM 2 is meaningful enough to replace SAM 2 as the default pick.

What SAM 3 added over SAM 2:
- **Concept prompts** — short noun phrases ("yellow school bus") or image exemplars, not just points/boxes. Open-vocabulary segmentation natively.
- **~2× accuracy on image and video PCS (Promptable Concept Segmentation)** vs SAM 2.
- Trained via a data engine that auto-annotated 4M+ unique concepts, the largest open-vocab segmentation dataset to date.

What SAM 3.1 added over SAM 3 (March 2026):
- **Object Multiplex** — shared-memory joint multi-object tracking.
- **2× throughput on video** — 16 → 32 FPS on H100 for medium-object-count videos.

Install: `pip install git+https://github.com/facebookresearch/sam3.git` or via Ultralytics (`docs.ultralytics.com/models/sam-3/`).

SAM 2 is still deployed in production pipelines and fine; treat as migration-when-convenient, not urgent.

## Trained task (Mask2Former / YOLOv8-seg default)

When you have 1,000+ labeled instances of the specific objects you care about and want one-pass inference:

- **YOLOv8-seg / YOLOv11-seg** — fast instance segmentation, same ecosystem as YOLO detection. Good for real-time, reasonable accuracy.
- **Mask2Former (Meta)** — unified architecture for semantic/instance/panoptic. Accuracy-leaning default.

## Edge segmentation

SAM is heavy. For on-device:
- **MobileSAM** (2023) — distilled SAM, ~10x faster, small accuracy drop. Pretrained weights available.
- **EfficientSAM** (2024) — similar goal, different distillation. Slightly better accuracy-speed frontier.
- **YOLOv8n-seg** — not SAM-family, but a fast instance segmenter for known classes.

## When to pick something else

- **Panoptic segmentation (combined instance + semantic)** → Mask2Former panoptic head.
- **Semantic only (road, sky, vegetation in autonomous driving)** → DeepLabV3+, SegFormer, or Mask2Former semantic head.
- **Medical imaging** → MONAI ecosystem. nnU-Net for tight-annotation medical segmentation.
- **Video segmentation with temporal consistency** → SAM 2. Or the XMem / Cutie family for mask propagation from a first-frame annotation.
- **Browser / real-time** → MediaPipe selfie segmentation, body segmentation.

## The three questions to narrow

1. **Do you have labeled data for your classes?** No → SAM 2 interactive. Yes → trained model.
2. **Edge or server?** Edge → MobileSAM / YOLO-seg. Server → SAM 2 or Mask2Former.
3. **Instance, semantic, or panoptic?** Pick accordingly; SAM produces instance-flavored output by default.

## The Dump

- **U-Net (2015)** — the encoder-decoder that started it all. Still the standard for medical.
- **Mask R-CNN (2017)** — instance segmentation via two-stage detection + mask head. Historical default.
- **DeepLabV3+ (2018)** — semantic segmentation. Still used in autonomous.
- **PointRend (2020)** — sharp boundaries via point-based refinement.
- **SegFormer (2021)** — ViT-based semantic. Good accuracy-efficiency.
- **Mask2Former (2022)** — unified architecture. The serious trained-model default.
- **SAM (Meta, 2023)** — open-vocabulary, promptable. Changed the field.
- **SAM 2 (Meta, 2024)** — video extension of SAM.
- **SAM 3 (Meta, Nov 2025)** — concept prompts (text + exemplars). 2× accuracy on PCS vs SAM 2.
- **SAM 3.1 (Meta, Mar 2026)** — Object Multiplex for joint MOT, 2× video throughput.
- **MobileSAM (2023)** — mobile/edge distilled SAM.
- **EfficientSAM (Meta, 2024)** — another SAM distillation.
- **FastSAM (2023)** — YOLOv8-seg adapted for SAM-style prompts. Significantly faster, less accurate.
- **HQ-SAM (2023)** — high-quality mask refinement on top of SAM.
- **YOLOv8-seg / YOLOv11-seg** — instance segmentation with the YOLO ecosystem.
- **OneFormer (2023)** — unified architecture; one model for all three segmentation types.
- **Grounded-SAM** — Grounding DINO + SAM → text-prompt segmentation.
- **SAM + CLIP** — zero-shot class-agnostic then classify.
- **nnU-Net** — self-configuring U-Net for medical. The medical default.
- **MONAI** — medical imaging AI ecosystem; includes segmentation networks and training pipelines.
- **Panoptic-DeepLab** — panoptic semantic + instance in one net.
- **MediaPipe Selfie / Image Segmenter** — browser/mobile, limited to specific classes.
- **Apple Vision VNGeneratePersonSegmentationRequest** — on-device iOS person segmentation.

## Graveyard

- **Mask R-CNN as a default for new work** — retired by Mask2Former and SAM.
- **Hand-crafted CRF post-processing** — retired ~2019; modern models produce clean masks without it.
- **FCN (fully convolutional, 2015)** — superseded by U-Net and DeepLab family.

## Last reviewed

2026-04-22. SAM 2 is still the newest major release in this space as of writing.
