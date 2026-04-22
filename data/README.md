# Data: Annotation, Datasets, Synthetic

> Where your training data comes from. Annotation tools changed in 2023 when SAM started auto-labeling segmentation masks. Benchmark datasets haven't changed much; trust them with caveats.

Data is where most CV projects actually spend their time. Model choice is a 1-day decision; data is a 6-month investment. The tools for collecting, labeling, and benchmarking data are worth picking deliberately.

## Recommended picks

| Use case | Pick | When to use |
|----------|------|-------------|
| **Open-source labeling (team)** | **CVAT** | Self-hosted, mature, video support |
| Open-source labeling (solo) | **Label Studio** | Broader (text, audio, image, video); easier to spin up |
| **Managed labeling platform** | **Roboflow** | End-to-end (upload → label → train → deploy). Best developer experience. |
| Pro/enterprise managed | **V7** or **Labelbox** | Medical, industrial, compliance-heavy. Expensive. |
| Auto-labeling | **SAM 2 + Grounding DINO** (programmatic) or **Roboflow / CVAT SAM integrations** | Accelerate labeling 5–10×. |

## Why CVAT for teams

Computer Vision Annotation Tool (Intel, open source). Self-hostable, supports boxes / polygons / masks / keypoints / tracks. Video annotation is first-class — interpolation between keyframes saves hours on MOT / action recognition datasets.

`docker-compose up` and you have a working labeling server. Role-based access control. Supports most common export formats (COCO, Pascal VOC, YOLO, custom).

## Why Roboflow for managed

End-to-end pipeline: upload → label → augment → split → train → deploy → monitor. Developer-first. Free tier is generous. Commercial tier scales.

Their SaaS is what most small CV teams reach for in 2026. If you don't need self-hosting, start here.

## The SAM auto-label shift

Before SAM (2023): labeling segmentation masks was the most expensive annotation task. You traced polygons by hand. Dozens of hours per thousand images.

After SAM: click a point, get a high-quality mask. Correct where needed. 5–10× speedup in practice.

Every major annotation platform integrated SAM in 2023–2024: CVAT, Label Studio, Roboflow, V7, Labelbox. Don't label segmentation masks by hand anymore.

## Programmatic labeling

When you don't need a UI and can label in a script:
- **SAM 2 (Meta)** — click / box / text → mask.
- **Grounding DINO** — text → bounding box. Open-vocabulary detection.
- **Grounded-SAM** — combine the above: text → mask.
- **Autodistill (Roboflow)** — wraps several of the above into a `"detect cars" → labeled dataset` pipeline.
- **LabelGPT-style (using a VLM to label)** — send each image to a VLM, get labels. Expensive but flexible.

## Benchmark datasets (the canonical ones)

### Detection
- **COCO (2014)** — 80 classes, 330K images. The universal detection benchmark.
- **Open Images V7** — ~9M images, 600+ classes. Larger but noisier than COCO.
- **Objects365** — 365 classes, more diversity than COCO.
- **LVIS** — COCO images re-labeled with 1,200 long-tail categories.
- **Visual Genome** — dense scene graphs. More about relationships than pure detection.

### Segmentation
- **COCO (instance + panoptic)** — reuses COCO images with mask annotations.
- **ADE20K** — 20K images, 150 classes, semantic segmentation.
- **Cityscapes** — street scenes, semantic segmentation, autonomous driving.
- **SA-1B (SAM training set)** — 1B masks. Meta released ~11M for research.

### Face
- **LFW (Labeled Faces in the Wild, 2007)** — saturated. 99.8%+ accuracy for any modern recognizer. Not diagnostic anymore.
- **MS1M / MS-Celeb-1M** — training set, not benchmark.
- **IJB-C** — unconstrained face recognition. Still useful as a harder benchmark.
- **MegaFace** — 1M distractors. Historical.
- **WIDER Face** — face detection benchmark.
- **QMUL-SurvFace** — surveillance-quality. Useful for modern face recognition benchmarks.

### OCR
- **ICDAR series** — the standard OCR/text detection benchmarks.
- **SROIE** — receipt parsing.
- **FUNSD** — form understanding.
- **DocVQA** — document visual question answering.
- **TextVQA** — scene text VQA.

### Pose
- **COCO Keypoints** — the default 2D pose benchmark.
- **MPII** — older, still referenced.
- **CrowdPose** — crowded scenes.
- **COCO-WholeBody** — 133 keypoints per person.

### Video / Tracking
- **MOT17 / MOT20** — multi-object tracking benchmarks.
- **Kinetics-400 / 700** — action recognition.
- **ActivityNet** — action localization.
- **DAVIS** — video object segmentation.

### Classification
- **ImageNet-1K (ILSVRC 2012)** — historical default. Saturated.
- **ImageNet-21K** — larger, better for pretraining.
- **CIFAR-10 / 100** — toy. Use for pedagogy, not actual benchmarks.

## When to pick something else

- **Medical data (HIPAA, PHI)** → air-gapped labeling. V7 or Labelbox with on-prem install. Don't use SaaS for patient data without BAA.
- **Sensitive security data** → self-hosted CVAT or custom tooling.
- **Synthetic data for rare classes** → Blender / Unreal / NVIDIA Omniverse for rendering. Or generate with diffusion models (Flux / SDXL) for specific object edits.
- **Data versioning beyond annotation** → DVC, LakeFS, Weights & Biases Artifacts, Roboflow's versioning.

## The three questions to narrow

1. **Who labels?** Team → CVAT / Roboflow. Solo or hobby → Label Studio / Roboflow free tier.
2. **Data sensitivity?** Sensitive → self-hosted. Not sensitive → managed SaaS.
3. **Is SAM enough to bootstrap?** Yes (most modern tasks) → use SAM-integrated tool. No → hand labeling with a motivated team.

## The Dump

### Open-source labeling
- **CVAT (Intel)** — teams, video support.
- **Label Studio (HumanSignal)** — general-purpose; images, audio, text.
- **VGG Image Annotator (VIA)** — single HTML file, no install. Toy-level but amazing for one-off.
- **LabelImg** — bounding boxes, classic desktop tool.
- **Labelme** — polygons, desktop.
- **AnyLabeling** — Labelme + AI assistance (SAM integration).
- **X-AnyLabeling** — enhanced AnyLabeling.
- **MakeSense.AI** — browser-based, free.

### Managed platforms
- **Roboflow** — dev-first end-to-end.
- **V7** — enterprise, medical/industrial focus.
- **Labelbox** — enterprise.
- **Scale AI** — huge projects, Fortune 500.
- **SuperAnnotate** — solid mid-market.
- **Kili Technology** — European.
- **Supervisely** — strong for 3D / point clouds.
- **Dataloop** — MLOps-heavy.
- **Encord** — video + DICOM.

### Auto-labeling tools
- **SAM 2** — the interactive default.
- **Grounding DINO** — text → boxes.
- **Grounded-SAM** — text → masks.
- **Autodistill** (Roboflow) — combine open models into a labeling pipeline.
- **Cleanlab** — find labeling errors in existing datasets.

### Data management
- **DVC** — Data Version Control, git-style.
- **LakeFS** — Git for object storage.
- **Weights & Biases Artifacts** — dataset versioning within W&B.
- **Roboflow Universe** — public datasets.
- **Hugging Face Datasets** — general ML dataset hub.
- **Kaggle** — competitions + datasets.

### Synthetic data
- **NVIDIA Omniverse / Isaac Sim** — physics-based synthetic.
- **Unity Perception** — Unity-based synthetic.
- **Blender + python** — DIY rendering.
- **Diffusion-generated (Flux, SDXL)** — image augmentation with control.
- **Gretel** — mostly tabular, some CV.

## Graveyard

- **Labelbox's original free tier** — retired; now enterprise-focused.
- **Amazon SageMaker Ground Truth as a leader** — still exists, but dev experience lags Roboflow.
- **Hand-labeling segmentation masks without SAM** — retired. You shouldn't be doing this in 2026.
- **Google AutoML Vision** — folded into Vertex.

## Last reviewed

2026-04-22.
