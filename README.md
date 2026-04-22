# fullstackcv / playbook

> An opinionated reference for building CV systems. Three picks per subtask, when to use each, and when not to — plus a dump of everything else worth knowing.

[![License: MIT](https://img.shields.io/github/license/fullstackcv/playbook?style=for-the-badge&color=3f51b5)](./LICENSE)
[![Site](https://img.shields.io/website?url=https%3A%2F%2Ffullstackcv.github.io%2Fplaybook%2F&style=for-the-badge&label=site&up_color=ffc107&up_message=live)](https://fullstackcv.github.io/playbook/)
[![Last commit](https://img.shields.io/github/last-commit/fullstackcv/playbook?style=for-the-badge&color=3f51b5)](https://github.com/fullstackcv/playbook/commits/main)
[![Sections](https://img.shields.io/badge/sections-14-ffc107?style=for-the-badge)](https://fullstackcv.github.io/playbook/)

> [!TIP]
> **[Browse the rendered site →](https://fullstackcv.github.io/playbook/)**
>
> Better mobile formatting, full-text search, sidebar navigation, light/dark toggle. This README is the raw markdown — fine for quick scanning on GitHub; the site is where you want to actually read it.

---

## The problem this solves

Most CV resource lists optimise for completeness. They grow by accretion — someone submits a PR for a new library, it goes in. After two years the list has 600 entries and is useless as a decision aid. You can't tell which pick is load-bearing and which is archaeological.

This repo inverts that. Each section leads with **three picks** — usually a default, an edge/low-end fallback, and a max-accuracy option — and every pick has a written *why* and *when not to*. The exhaustive list still exists (in each section's **Dump**), but it sits behind the picks, not in front of them.

The picks are opinions. They will age. Every section has a "last reviewed" date.

## Start here

New to the playbook? Read [the Face section](https://fullstackcv.github.io/playbook/face/) first — it's the most complete and shows the format end-to-end. Or dive straight into whichever subtask you're shipping.

## How to read this

| Situation | What to do |
|-----------|-----------|
| You know the subtask | Jump to the section. Read the 3–4 rows of the picks table. Often enough. |
| Picks don't fit your constraint | Read the Dump behind them for context, then "When to pick something else." |
| Browsing to learn the field | Read the picks across sections — ~20 min tour of what matters in each subtask. |

---

## Sections

### Perception

| Section | One-line |
|---------|----------|
| [Classification](https://fullstackcv.github.io/playbook/classification/) | CLIP zero-shot / timm fine-tune / DINOv2 probe, by data availability. |
| [Object Detection](https://fullstackcv.github.io/playbook/object-detection/) | YOLO for most cases; RT-DETR if on GPU; Co-DETR for research. |
| [Segmentation](https://fullstackcv.github.io/playbook/segmentation/) | SAM 2 for zero-shot; Mask2Former / YOLOv8-seg for trained. |
| [Pose Estimation](https://fullstackcv.github.io/playbook/pose/) | RTMPose server; MediaPipe browser; ViTPose research. |
| [OCR / Document AI](https://fullstackcv.github.io/playbook/ocr/) | PaddleOCR for clean; VLMs for messy; Donut for structured forms. |
| [Tracking](https://fullstackcv.github.io/playbook/tracking/) | ByteTrack default; BoT-SORT with ReID; OC-SORT for benchmarks. |
| [Depth Estimation](https://fullstackcv.github.io/playbook/depth/) | Depth Anything V2 monocular; stereo if hardware available. |
| [Retrieval / Embeddings](https://fullstackcv.github.io/playbook/retrieval/) | SigLIP embeddings + FAISS; DINOv2 for image-only. |

### Face (the one vertical)

| Section | One-line |
|---------|----------|
| [Face](https://fullstackcv.github.io/playbook/face/) | SCRFD detect, 5-point align, ArcFace embed, 1-NN + threshold search. |

> [!NOTE]
> More verticals (medical, satellite, industrial, retail, robotics) will be added as products ship content-backed opinions in each. Not adding them as empty placeholders.

### Multimodal

| Section | One-line |
|---------|----------|
| [VLM / Multimodal](https://fullstackcv.github.io/playbook/vlm/) | Gemini / GPT / Claude commercial; Qwen2-VL / InternVL2 open. |
| [Image Generation](https://fullstackcv.github.io/playbook/generation/) | Flux for open; SDXL for ecosystem; ControlNet for control. |

### Stack & deployment

| Section | One-line |
|---------|----------|
| [Inference Runtimes](https://fullstackcv.github.io/playbook/runtimes/) | ONNX Runtime default; TensorRT on NVIDIA; CoreML on Apple. |
| [Edge Deployment](https://fullstackcv.github.io/playbook/edge/) | Jetson Orin Nano Super, Raspberry Pi 5, CoreML for mobile. |
| [Cloud Vision APIs](https://fullstackcv.github.io/playbook/cloud-apis/) | VLMs for flexible; task APIs (Rekognition / Vision) for scale. |
| [Data, Annotation, Datasets](https://fullstackcv.github.io/playbook/data/) | CVAT / Roboflow / SAM-based auto-labeling; COCO / ImageNet / etc. |

---

## How each section is structured

Every page follows the same shape:

```
Intro            — 2 paragraphs on what this subtask is and why the picks differ
Recommended      — 3-row table with when-to-use + when-to-avoid + install
Narrowing        — 3 questions that disambiguate to one pick
The Dump         — exhaustive list, one-line verdict each
Graveyard        — retired picks and why
Last reviewed    — a date so you can tell when this went stale
```

Some sections adjust the axis (Face uses clean-input / surveillance / edge instead of default / edge / max-accuracy).

## Reference

| File | Purpose |
|------|---------|
| [CONTRIBUTING](./CONTRIBUTING.md) | How to propose additions; Dump vs Recommended vs Graveyard rules |
| [Evaluation criteria](./rubrics/evaluation-criteria.md) | How picks are judged (what counts, what doesn't) |
| [Section template](./rubrics/section-template.md) | Canonical page structure for new sections |
| [Refresh pipeline](./scripts/refresh.md) | LLM-in-the-loop regeneration sketch |

## License

MIT. Use anything here however you like.

## Maintainer

**Vikas Gupta** [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vikas-gupta-2913a276/) — Founder, [DeepVidya.ai](https://deepvidya.ai)

---

*Last full review: 2026-04-22. Each section carries its own review date.*
