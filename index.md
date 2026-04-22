# Full Stack CV — Playbook

> An opinionated reference for building CV systems. Three picks per subtask, when to use each, and when not to — plus a dump of everything else worth knowing.

## The problem this solves

Most CV resource lists optimise for completeness. They grow by accretion — someone submits a PR for a new library, it goes in. After two years the list has 600 entries and is useless as a decision aid. You can't tell which pick is load-bearing and which is archaeological.

This site inverts that. Each section leads with **three picks** — usually a default, an edge/low-end fallback, and a max-accuracy option — and every pick has a written *why* and *when not to*. The exhaustive list still exists (in each section's **Dump**), but it sits behind the picks, not in front of them.

The picks are opinions. They will age. Every section has a "last reviewed" date.

## Start here

New to the playbook? Read [the Face section](face/README.md) first — it's the most complete and shows the format end-to-end. Or jump to whichever subtask you're shipping.

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
| [Classification](classification/README.md) | CLIP zero-shot / timm fine-tune / DINOv2 probe, by data availability. |
| [Object Detection](object-detection/README.md) | YOLO for most cases; RT-DETR if on GPU; Co-DETR for research. |
| [Segmentation](segmentation/README.md) | SAM 2 for zero-shot; Mask2Former / YOLOv8-seg for trained. |
| [Pose Estimation](pose/README.md) | RTMPose server; MediaPipe browser; ViTPose research. |
| [OCR / Document AI](ocr/README.md) | PaddleOCR for clean; VLMs for messy; Donut for structured forms. |
| [Tracking](tracking/README.md) | ByteTrack default; BoT-SORT with ReID; OC-SORT for benchmarks. |
| [Depth Estimation](depth/README.md) | Depth Anything V2 monocular; stereo if hardware available. |
| [Retrieval / Embeddings](retrieval/README.md) | SigLIP embeddings + FAISS; DINOv2 for image-only. |

### Face (the one vertical)

| Section | One-line |
|---------|----------|
| [Face](face/README.md) | SCRFD detect, 5-point align, ArcFace embed, 1-NN + threshold search. |

!!! note "More verticals coming"
    Medical, satellite, industrial, retail, and robotics sections will be added once there are content-backed opinions to put in each. Not adding them as empty placeholders.

### Multimodal

| Section | One-line |
|---------|----------|
| [VLM / Multimodal](vlm/README.md) | Gemini / GPT / Claude commercial; Qwen2-VL / InternVL2 open. |
| [Image Generation](generation/README.md) | Flux for open; SDXL for ecosystem; ControlNet for control. |

### Stack & deployment

| Section | One-line |
|---------|----------|
| [Inference Runtimes](runtimes/README.md) | ONNX Runtime default; TensorRT on NVIDIA; CoreML on Apple. |
| [Edge Deployment](edge/README.md) | Jetson Orin Nano Super, Raspberry Pi 5, CoreML for mobile. |
| [Cloud Vision APIs](cloud-apis/README.md) | VLMs for flexible; task APIs (Rekognition / Vision) for scale. |
| [Data, Annotation, Datasets](data/README.md) | CVAT / Roboflow / SAM-based auto-labeling; COCO / ImageNet / etc. |

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
| [Contributing](CONTRIBUTING.md) | How to propose additions; Dump vs Recommended vs Graveyard rules |
| [Evaluation criteria](rubrics/evaluation-criteria.md) | How picks are judged (what counts, what doesn't) |
| [Section template](rubrics/section-template.md) | Canonical page structure for new sections |
| [Refresh pipeline](scripts/refresh.md) | LLM-in-the-loop regeneration sketch |

## License

MIT. Use anything here however you like.

## Maintainer

**Vikas Gupta** — Founder, [DeepVidya.ai](https://deepvidya.ai) · [LinkedIn](https://www.linkedin.com/in/vikas-gupta-2913a276/)

---

*Last full review: 2026-04-22. Each section carries its own review date.*
