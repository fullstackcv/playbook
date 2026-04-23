# Object Detection

> Finding bounding boxes around objects, usually with labels. The subtask with the most churn — new YOLO variants ship every quarter. The picks rotate faster here than anywhere else.

Object detection has fragmented into three deployment tiers that need different models. The "best" detector is whichever fits your constraint tier. A research model achieving +3 points AP won't help if you're on a Jetson Nano with a tight latency budget.

## Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Edge / real-time | **[YOLO26n](https://github.com/ultralytics/ultralytics)** (Ultralytics, Jan 2026) | Jetson, Pi, phones; NMS-free, ~43% faster CPU vs YOLO11 nano |
| **Default (CNN)** | **[YOLO26m](https://github.com/ultralytics/ultralytics)** | Server-side, real-time-ish, unified multi-task (det/seg/cls/pose/OBB) |
| **Default (transformer)** | **[RF-DETR](https://github.com/roboflow/rf-detr)** (Roboflow, ICLR 2026) | First real-time detector to clear 60 AP on COCO; DINOv2 backbone |
| Max accuracy | **[Co-DETR](https://github.com/Sense-X/Co-DETR)** or **[DINO-family](https://github.com/IDEA-Research/DINO)** | Offline / batch; GPU available; every AP point matters |

*Reading the picks:* **Operational default** = YOLO26 (export + deployment maturity). **Latest strong contender** = RF-DETR (ICLR 2026 SOTA, NMS-free transformer; worth testing for GPU-side deployments). **Research max** = Co-DETR / DINO family. YOLO11 and YOLOv8 remain reasonable picks if your team is ecosystem-locked; the move from YOLO11 → YOLO26 is not urgent, just available.

## YOLO26 — the current CNN default

Ultralytics shipped YOLO26 in January 2026 as a fully end-to-end, NMS-free architecture built specifically for edge deployment. Key changes vs YOLO11:

- **NMS-free inference natively** — no post-processing NMS, simpler serving.
- **Distribution Focal Loss removed**, replaced with Progressive Loss Balancing (ProgLoss).
- **Small-Target-Aware Label Assignment (STAL)** — noticeable improvement on small/dense objects.
- **MuSGD optimizer** for training stability.
- **~43% faster CPU inference** on the nano variant vs YOLO11n.
- **Unified multi-task** — one model family covers detection, instance segmentation, classification, pose estimation, and oriented bounding boxes.

If you had a YOLO11 deployment, YOLO26 is a drop-in upgrade with meaningful latency wins and a cleaner serving path. YOLO11 and YOLOv8 remain reasonable if you're ecosystem-locked.

The YOLO naming is still confusing: YOLOv1–v4 (Redmon / AlexeyAB lineage), YOLOv5 (Ultralytics), YOLOv6 (Meituan), YOLOv7 (Wang et al.), YOLOv8 / v9 / v10 / v11 / 26 (Ultralytics, current lineage). "YOLO" in production 2026 means "Ultralytics YOLO26."

## RF-DETR — the serious transformer alternative

Roboflow's RF-DETR (ICLR 2026) is the first real-time detector to hit **60+ mean AP on COCO**. Built on a DINOv2 vision transformer backbone, tuned explicitly for real-time latency:

- **RF-DETR nano** — 48.0 AP on COCO, beats D-FINE nano by 5.3 AP at similar latency.
- **RF-DETR 2x-large** — outperforms GroundingDINO-tiny by 1.2 AP on Roboflow100-VL while running 20× as fast.
- Evaluated directly against YOLO11 / YOLOv8 and LW-DETR / D-FINE — consistently #1 or #2 across categories.

Pick RF-DETR when:
- You're on a GPU and want SOTA accuracy without sacrificing real-time latency.
- You need strong transfer to custom domains — RF100-VL shows it adapts better than YOLO-class models.
- NMS-free serving matters operationally.

Pick YOLO26 over RF-DETR when:
- CPU-only deployment (transformer overhead still matters at the low end).
- Deep ecosystem lock-in (Ultralytics Hub, existing fine-tuning pipelines).

## When to pick something else

- **You need the absolute highest AP number on a paper benchmark** → Co-DETR or DINO family. Slow, offline, research-register.
- **You're detecting a single well-defined object and have lots of data** → train a YOLO from scratch. The ecosystem for fine-tuning is mature.
- **You have no training data and need zero-shot detection** → **GroundingDINO** or **Florence-2** or a general-purpose VLM (Gemini, Qwen-VL). You give a text prompt, it returns boxes. Slower per-inference but no training needed.
- **You're inside a web browser** → TensorFlow.js + YOLOv8n (TFJS export), or MediaPipe Object Detector. Limited accuracy but no server.
- **Fruit / traffic / retail counting as a SaaS** → look at managed platforms like Roboflow or RF-DETR deployments; you may not need to train anything.

## The three questions to narrow

1. **Do you have training data?** If no → zero-shot (GroundingDINO, VLM). If yes → YOLO or RT-DETR.
2. **What's your latency budget per frame?** <15ms on GPU → YOLO nano / RT-DETR small. 15–50ms → YOLO medium / RT-DETR. 50ms+ → DETR-family, Co-DETR.
3. **CPU or GPU at inference?** CPU → YOLO. GPU → anything.

## The Dump

- **[YOLOv1 (2015)](https://arxiv.org/abs/1506.02640)** — the original. Real-time object detection made accessible.
- **[YOLOv4 (Bochkovskiy et al., 2020)](https://github.com/AlexeyAB/darknet)** — last of the Darknet-native YOLO family.
- **[YOLOv5 / YOLOv8 / YOLOv11 / YOLO26 (Ultralytics)](https://github.com/ultralytics/ultralytics)** — the dominant practical YOLO lineage. YOLO26 (Jan 2026) is current. Python-first.
- **[RF-DETR (Roboflow, 2025–2026, ICLR 2026)](https://github.com/roboflow/rf-detr)** — first real-time detector at 60+ COCO AP. DINOv2 backbone. SOTA accuracy + real-time.
- **[YOLOX (Megvii, 2021)](https://github.com/Megvii-BaseDetection/YOLOX)** — anchor-free, competitive. Less deployment polish than Ultralytics.
- **[YOLOv7 (Wang, 2022)](https://github.com/WongKinYiu/yolov7)** — strong accuracy. Less active.
- **[YOLOv9](https://github.com/WongKinYiu/yolov9) / [YOLOv10](https://github.com/THU-MIG/yolov10) (2024)** — incremental improvements; some prefer v10's NMS-free variant.
- **[YOLO-NAS (Deci / Roboflow)](https://github.com/Deci-AI/super-gradients)** — neural architecture search + quantization-aware training. Strong at edge.
- **[DETR (Carion et al., 2020)](https://github.com/facebookresearch/detr)** — transformer-based detection. NMS-free. Original paper, slow.
- **[Deformable DETR](https://github.com/fundamentalvision/Deformable-DETR)** — accelerated convergence.
- **[DINO / DINO-DETR](https://github.com/IDEA-Research/DINO)** — the strongest DETR-family variants on COCO.
- **[Co-DETR](https://github.com/Sense-X/Co-DETR)** — the current COCO SOTA-ish. Slow.
- **[RT-DETR / RT-DETRv2 (Baidu, 2023/2024)](https://github.com/lyuwenyu/RT-DETR)** — real-time DETR. Competitive with YOLO.
- **[RTMDet (MMDetection / OpenMMLab)](https://github.com/open-mmlab/mmdetection/tree/main/configs/rtmdet)** — strong across tiers. Less marketing than YOLO.
- **[Faster R-CNN](https://arxiv.org/abs/1506.01497) / [Mask R-CNN](https://arxiv.org/abs/1703.06870)** — historical. Still used in research.
- **[CenterNet](https://github.com/xingyizhou/CenterNet) / [FCOS](https://github.com/tianzhi0549/FCOS)** — anchor-free approaches; superseded.
- **[GroundingDINO](https://github.com/IDEA-Research/GroundingDINO)** — open-vocabulary detection. Text prompt → boxes.
- **[Florence-2 (Microsoft)](https://huggingface.co/microsoft/Florence-2-large)** — grounding + captioning + OCR in one model. Open-vocab detection included.
- **[SAM](https://github.com/facebookresearch/segment-anything) + [CLIP](https://github.com/openai/CLIP) for detection** — segment everything, classify each with CLIP. Slow but zero-shot.
- **[Google MediaPipe Object Detector](https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector)** — browser/mobile.
- **[Apple Vision Framework](https://developer.apple.com/documentation/vision)** — on-device iOS, CoreML-backed.
- **[Roboflow RF-DETR](https://github.com/roboflow/rf-detr)** — hosted deployment on top of DETR family.
- **[Ultralytics Hub](https://hub.ultralytics.com/)** — managed YOLO training + deployment.

## Graveyard

- **[SSD (2015)](https://arxiv.org/abs/1512.02325)** — overtaken. Still ships in OpenCV but rarely the right choice.
- **Anchor-based R-CNN family as default** — retired in favor of one-stage detectors.
- **YOLOv3 (2018) as a modern default** — use v8+ unless you have legacy weights.

## Last reviewed

2026-04-22.
