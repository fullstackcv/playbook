# fullstackcv/playbook

> An opinionated reference for building CV systems. For each subtask: three picks, when to use each, and when not to. Plus a dump of everything else worth knowing.

## Why this exists

Most CV resource lists optimise for completeness. They grow by accretion — someone submits a PR for a new library, it goes in. After two years the list has 600 entries and is useless as a decision aid. You can't tell which pick is load-bearing and which is archaeological.

This repo inverts that. Each section leads with **three picks** — usually a default, an edge/low-end fallback, and a max-accuracy option — and every pick has a written *why* and *when not to*. The exhaustive list still exists (in each section's **Dump**), but it sits behind the picks, not in front of them.

The picks are opinions. They will age. Every section has a "last reviewed" date and I expect to rewrite them as the field moves. See [`scripts/refresh.md`](./scripts/refresh.md) for the long-term plan to keep the picks in sync with the Dump via an LLM-in-the-loop pipeline.

## How to read this

If you know what subtask you need, jump to the section. The section README leads with a picks table. Read the 3–4 rows. That's usually enough.

If the picks don't fit your constraint (unusual hardware, unusual domain, unusual accuracy target), read the Dump for context, then read "When to pick something else."

If you're browsing to learn the field, read the picks in order — they'll give you a 15-minute tour of what matters in each subtask and why.

## Sections

### Perception primitives

| Section | One-line |
|---------|----------|
| [Classification](./classification/) | CLIP zero-shot / timm fine-tune / DINOv2 probe, by data availability. |
| [Object Detection](./object-detection/) | YOLO for most cases; RT-DETR if on GPU; Co-DETR for research. |
| [Segmentation](./segmentation/) | SAM 2 for zero-shot; Mask2Former / YOLOv8-seg for trained. |
| [Pose Estimation](./pose/) | RTMPose server; MediaPipe browser; ViTPose research. |
| [OCR / Document AI](./ocr/) | PaddleOCR for clean; VLMs for messy; Donut for structured forms. |
| [Tracking](./tracking/) | ByteTrack default; BoT-SORT with ReID; OC-SORT for benchmarks. |
| [Depth Estimation](./depth/) | Depth Anything V2 monocular; stereo if hardware available. |
| [Retrieval / Embeddings](./retrieval/) | SigLIP embeddings + FAISS; DINOv2 for image-only. |

### Face (the one vertical)

| Section | One-line |
|---------|----------|
| [Face](./face/) | SCRFD detect, 5-point align, ArcFace embed, 1-NN + threshold search. |

*More verticals (medical, satellite, industrial, retail, robotics) will be added as products 2–12 ship content-backed opinions in each. Not adding them as empty placeholders.*

### Multimodal

| Section | One-line |
|---------|----------|
| [VLM / Multimodal](./vlm/) | Gemini/GPT/Claude commercial; Qwen2-VL/InternVL2 open. |
| [Image Generation](./generation/) | Flux for open; SDXL for ecosystem; ControlNet for control. |

### Stack / deployment

| Section | One-line |
|---------|----------|
| [Inference Runtimes](./runtimes/) | ONNX Runtime default; TensorRT on NVIDIA; CoreML on Apple. |
| [Edge Deployment](./edge/) | Jetson Orin Nano Super, Raspberry Pi 5, CoreML for mobile. |
| [Cloud Vision APIs](./cloud-apis/) | VLMs for flexible; task APIs (Rekognition/Vision) for scale. |
| [Data, Annotation, Datasets](./data/) | CVAT / Roboflow / SAM-based auto-labeling; COCO/ImageNet/etc. |

## Format each section follows

```
Intro — 2 paragraphs on what this subtask is and why the picks differ

Recommended picks (3 rows) — with when-to-use, when-to-avoid, install

The three questions to narrow further

The Dump — everything else worth knowing, one-line verdict each

Graveyard — what used to be the pick but isn't anymore, and why

Last reviewed — a date, so you can tell when this went stale
```

Some sections adjust the axis (for face recognition, the 3 picks are clean-input / surveillance / edge instead of the usual default/edge/max).

## The meta

- [`CONTRIBUTING.md`](./CONTRIBUTING.md) — how to propose additions, Dump vs Recommended vs Graveyard rules.
- [`rubrics/evaluation-criteria.md`](./rubrics/evaluation-criteria.md) — how picks are judged (what counts, what doesn't).
- [`templates/section-template.md`](./templates/section-template.md) — the canonical page structure.
- [`scripts/refresh.md`](./scripts/refresh.md) — the LLM-in-the-loop pipeline (planned).
- [`.github/`](./.github/) — PR and issue templates.

## License

MIT. Use anything here however you like.

## Who maintains this

Vikas Gupta ([@vikasguptaai](https://www.linkedin.com/in/vikasgptai/)), senior CV engineer, 13 years in the field. Also maintains [facestack](https://github.com/fullstackcv/facestack) and the `@vikasguptaai` YouTube channel. Reach via LinkedIn or open an issue here.

This playbook is research I'd want to hand my past self. If something here is wrong, tell me — I'll fix it.

---

*Last full review: 2026-04-22. Each section carries its own review date.*
