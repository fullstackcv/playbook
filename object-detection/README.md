# Object Detection

> Finding bounding boxes around objects, usually with labels. The subtask with the most churn — new YOLO variants ship every quarter. The picks rotate faster here than anywhere else.

Object detection has fragmented into three deployment tiers that need different models. The "best" detector is whichever fits your constraint tier. A Co-DETR model achieving +3 points AP won't help if you're on a Jetson Nano at 3 FPS.

## Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Edge / real-time | **YOLOv11n** or **YOLOv8n** | Jetson, Pi, phones; when FPS > accuracy |
| **Default** | **YOLOv11m** or **RT-DETRv2** | Server-side, real-time-ish, good accuracy |
| Max accuracy | **Co-DETR** or **DINO-family** | Offline / batch; GPU available; every AP point matters |

## Why YOLO is still the default in 2026

Fifteen years of incremental improvements, a massive ecosystem, trivial ONNX export, excellent inference-runtime support everywhere (TensorRT, CoreML, ONNX Runtime, TFLite). When in doubt, YOLO.

The YOLO naming is confusing: YOLOv1–v4 (Redmon / AlexeyAB lineage), YOLOv5 (Ultralytics), YOLOv6 (Meituan), YOLOv7 (Wang et al.), YOLOv8 (Ultralytics), YOLOv9, YOLOv10, YOLOv11 (Ultralytics). The current Ultralytics YOLO is what most people mean by "YOLO" in production. YOLOv11 shipped late 2024; YOLOv8 is still a reasonable default because the ecosystem is deeper.

## RT-DETR — the serious alternative to YOLO

Transformer-based, no NMS post-processing (a real win operationally). RT-DETRv2 (2024) hits YOLOv11-m accuracy at similar latency on GPUs. If you're starting fresh and on a GPU, it's worth considering. On CPU it's less competitive than YOLO.

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

- **YOLOv1 (2015)** — the original. Real-time object detection made accessible.
- **YOLOv4 (Bochkovskiy et al., 2020)** — last of the Darknet-native YOLO family.
- **YOLOv5 / YOLOv8 / YOLOv11 (Ultralytics)** — the dominant practical YOLO lineage. Python-first.
- **YOLOX (Megvii, 2021)** — anchor-free, competitive. Less deployment polish than Ultralytics.
- **YOLOv7 (Wang, 2022)** — strong accuracy. Less active.
- **YOLOv9 / YOLOv10 (2024)** — incremental improvements; some prefer v10's NMS-free variant.
- **YOLO-NAS (Deci / Roboflow)** — neural architecture search + quantization-aware training. Strong at edge.
- **DETR (Carion et al., 2020)** — transformer-based detection. NMS-free. Original paper, slow.
- **Deformable DETR** — accelerated convergence.
- **DINO / DINO-DETR** — the strongest DETR-family variants on COCO.
- **Co-DETR** — the current COCO SOTA-ish. Slow.
- **RT-DETR / RT-DETRv2 (Baidu, 2023/2024)** — real-time DETR. Competitive with YOLO.
- **RTMDet (MMDetection / OpenMMLab)** — strong across tiers. Less marketing than YOLO.
- **Faster R-CNN / Mask R-CNN** — historical. Still used in research.
- **CenterNet / FCOS** — anchor-free approaches; superseded.
- **GroundingDINO** — open-vocabulary detection. Text prompt → boxes.
- **Florence-2 (Microsoft)** — grounding + captioning + OCR in one model. Open-vocab detection included.
- **SAM + CLIP for detection** — segment everything, classify each with CLIP. Slow but zero-shot.
- **Google MediaPipe Object Detector** — browser/mobile.
- **Apple Vision Framework** — on-device iOS, CoreML-backed.
- **Roboflow RF-DETR** — hosted deployment on top of DETR family.
- **Ultralytics Hub** — managed YOLO training + deployment.

## Graveyard

- **SSD (2015)** — overtaken. Still ships in OpenCV but rarely the right choice.
- **Anchor-based R-CNN family as default** — retired in favor of one-stage detectors.
- **YOLOv3 (2018) as a modern default** — use v8+ unless you have legacy weights.

## Last reviewed

2026-04-22.
