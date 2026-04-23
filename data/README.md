# Data: Annotation, Datasets, Synthetic

> Where your training data comes from. Annotation tools changed in 2023 when SAM started auto-labeling segmentation masks. Benchmark datasets haven't changed much; trust them with caveats.

Data is where most CV projects actually spend their time. Model choice is a 1-day decision; data is a 6-month investment. The tools for collecting, labeling, and benchmarking data are worth picking deliberately.

## Recommended picks

| Use case | Pick | When to use |
|----------|------|-------------|
| **Open-source labeling (team)** | **[CVAT](https://github.com/cvat-ai/cvat)** | Self-hosted, mature, video support |
| Open-source labeling (solo) | **[Label Studio](https://github.com/HumanSignal/label-studio)** | Broader (text, audio, image, video); easier to spin up |
| **Managed labeling platform** | **[Roboflow](https://roboflow.com/)** | End-to-end (upload → label → train → deploy). Best developer experience. |
| Pro/enterprise managed | **[V7](https://www.v7labs.com/)** or **[Labelbox](https://labelbox.com/)** | Medical, industrial, compliance-heavy. Expensive. |
| Auto-labeling | **[SAM 2](https://github.com/facebookresearch/sam2) + [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO)** (programmatic) or **Roboflow / CVAT SAM integrations** | Accelerate labeling 5–10×. |

## Why CVAT for teams

Computer Vision Annotation Tool (Intel, open source). Self-hostable, supports boxes / polygons / masks / keypoints / tracks. Video annotation is first-class — interpolation between keyframes saves hours on MOT / action recognition datasets.

`docker-compose up` and you have a working labeling server. Role-based access control. Supports most common export formats (COCO, Pascal VOC, YOLO, custom).

## Why Roboflow for managed

End-to-end pipeline: upload → label → augment → split → train → deploy → monitor. Developer-first. Free tier is generous. Commercial tier scales.

Their SaaS is what most small CV teams reach for in 2026. If you don't need self-hosting, start here.

## The SAM auto-label shift

Before SAM (2023): labeling segmentation masks was the most expensive annotation task. You traced polygons by hand. Dozens of hours per thousand images.

After SAM: click a point, get a high-quality mask. Correct where needed. 5–10× speedup in practice.

Every major annotation platform integrated SAM in 2023–2024: CVAT, Label Studio, Roboflow, V7, Labelbox. By 2026, most have moved on to SAM 2 / SAM 3 integration for concept-prompted (text-driven) labeling. CVAT and Roboflow have direct integrations: Roboflow Annotate supports a SAM-2-powered label assistant in the interface, and CVAT integrates SAM, Mask R-CNN, YOLO models for auto-labeling. Don't label segmentation masks by hand anymore.

## Programmatic labeling

When you don't need a UI and can label in a script:
- **[SAM 2 (Meta)](https://github.com/facebookresearch/sam2)** — click / box / text → mask.
- **[Grounding DINO](https://github.com/IDEA-Research/GroundingDINO)** — text → bounding box. Open-vocabulary detection.
- **[Grounded-SAM](https://github.com/IDEA-Research/Grounded-Segment-Anything)** — combine the above: text → mask.
- **[Autodistill (Roboflow)](https://github.com/autodistill/autodistill)** — wraps several of the above into a `"detect cars" → labeled dataset` pipeline.
- **LabelGPT-style (using a VLM to label)** — send each image to a VLM, get labels. Expensive but flexible.

## Benchmark datasets (the canonical ones)

### Detection
- **[COCO (2014)](https://cocodataset.org/)** — 80 classes, 330K images. The universal detection benchmark.
- **[Open Images V7](https://storage.googleapis.com/openimages/web/index.html)** — ~9M images, 600+ classes. Larger but noisier than COCO.
- **[Objects365](https://www.objects365.org/)** — 365 classes, more diversity than COCO.
- **[LVIS](https://www.lvisdataset.org/)** — COCO images re-labeled with 1,200 long-tail categories.
- **[Visual Genome](https://homes.cs.washington.edu/~ranjay/visualgenome/)** — dense scene graphs. More about relationships than pure detection.

### Segmentation
- **[COCO (instance + panoptic)](https://cocodataset.org/)** — reuses COCO images with mask annotations.
- **[ADE20K](https://groups.csail.mit.edu/vision/datasets/ADE20K/)** — 20K images, 150 classes, semantic segmentation.
- **[Cityscapes](https://www.cityscapes-dataset.com/)** — street scenes, semantic segmentation, autonomous driving.
- **[SA-1B (SAM training set)](https://ai.meta.com/datasets/segment-anything/)** — 1B masks. Meta released ~11M for research.

### Face
- **[LFW (Labeled Faces in the Wild, 2007)](http://vis-www.cs.umass.edu/lfw/)** — saturated. 99.8%+ accuracy for any modern recognizer. Not diagnostic anymore.
- **MS1M / MS-Celeb-1M** — training set, not benchmark.
- **[IJB-C](https://www.nist.gov/itl/iad/image-group/ijb-c)** — unconstrained face recognition. Still useful as a harder benchmark.
- **[MegaFace](http://megaface.cs.washington.edu/)** — 1M distractors. Historical.
- **[WIDER Face](http://shuoyang1213.me/WIDERFACE/)** — face detection benchmark.
- **[QMUL-SurvFace](https://qmul-survface.github.io/)** — surveillance-quality. Useful for modern face recognition benchmarks.

### OCR
- **[ICDAR series](https://rrc.cvc.uab.es/)** — the standard OCR/text detection benchmarks.
- **[SROIE](https://rrc.cvc.uab.es/?ch=13)** — receipt parsing.
- **[FUNSD](https://guillaumejaume.github.io/FUNSD/)** — form understanding.
- **[DocVQA](https://www.docvqa.org/)** — document visual question answering.
- **[TextVQA](https://textvqa.org/)** — scene text VQA.

### Pose
- **[COCO Keypoints](https://cocodataset.org/#keypoints-2020)** — the default 2D pose benchmark.
- **[MPII](http://human-pose.mpi-inf.mpg.de/)** — older, still referenced.
- **[CrowdPose](https://github.com/Jeff-sjtu/CrowdPose)** — crowded scenes.
- **[COCO-WholeBody](https://github.com/jin-s13/COCO-WholeBody)** — 133 keypoints per person.

### Video / Tracking
- **[MOT17 / MOT20](https://motchallenge.net/)** — multi-object tracking benchmarks.
- **[Kinetics-400 / 700](https://www.deepmind.com/open-source/kinetics)** — action recognition.
- **[ActivityNet](http://activity-net.org/)** — action localization.
- **[DAVIS](https://davischallenge.org/)** — video object segmentation.

### Classification
- **[ImageNet-1K (ILSVRC 2012)](https://www.image-net.org/)** — historical default. Saturated.
- **[ImageNet-21K](https://www.image-net.org/)** — larger, better for pretraining.
- **[CIFAR-10 / 100](https://www.cs.toronto.edu/~kriz/cifar.html)** — toy. Use for pedagogy, not actual benchmarks.

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
- **[CVAT (Intel)](https://github.com/cvat-ai/cvat)** — teams, video support.
- **[Label Studio (HumanSignal)](https://github.com/HumanSignal/label-studio)** — general-purpose; images, audio, text.
- **[VGG Image Annotator (VIA)](https://www.robots.ox.ac.uk/~vgg/software/via/)** — single HTML file, no install. Toy-level but amazing for one-off.
- **[LabelImg](https://github.com/HumanSignal/labelImg)** — bounding boxes, classic desktop tool.
- **[Labelme](https://github.com/wkentaro/labelme)** — polygons, desktop.
- **[AnyLabeling](https://github.com/vietanhdev/anylabeling)** — Labelme + AI assistance (SAM integration).
- **[X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling)** — enhanced AnyLabeling.
- **[MakeSense.AI](https://www.makesense.ai/)** — browser-based, free.

### Managed platforms
- **[Roboflow](https://roboflow.com/)** — dev-first end-to-end.
- **[V7](https://www.v7labs.com/)** — enterprise, medical/industrial focus.
- **[Labelbox](https://labelbox.com/)** — enterprise.
- **[Scale AI](https://scale.com/)** — huge projects, Fortune 500.
- **[SuperAnnotate](https://www.superannotate.com/)** — solid mid-market.
- **[Kili Technology](https://kili-technology.com/)** — European.
- **[Supervisely](https://supervisely.com/)** — strong for 3D / point clouds.
- **[Dataloop](https://dataloop.ai/)** — MLOps-heavy.
- **[Encord](https://encord.com/)** — video + DICOM.

### Auto-labeling tools
- **[SAM 2](https://github.com/facebookresearch/sam2)** — the interactive default.
- **[Grounding DINO](https://github.com/IDEA-Research/GroundingDINO)** — text → boxes.
- **[Grounded-SAM](https://github.com/IDEA-Research/Grounded-Segment-Anything)** — text → masks.
- **[Autodistill](https://github.com/autodistill/autodistill)** (Roboflow) — combine open models into a labeling pipeline.
- **[Cleanlab](https://github.com/cleanlab/cleanlab)** — find labeling errors in existing datasets.

### Data management
- **[DVC](https://dvc.org/)** — Data Version Control, git-style.
- **[LakeFS](https://lakefs.io/)** — Git for object storage.
- **[Weights & Biases Artifacts](https://wandb.ai/site/artifacts)** — dataset versioning within W&B.
- **[Roboflow Universe](https://universe.roboflow.com/)** — public datasets.
- **[Hugging Face Datasets](https://huggingface.co/datasets)** — general ML dataset hub.
- **[Kaggle](https://www.kaggle.com/datasets)** — competitions + datasets.

### Synthetic data
- **[NVIDIA Omniverse](https://www.nvidia.com/en-us/omniverse/) / [Isaac Sim](https://developer.nvidia.com/isaac-sim)** — physics-based synthetic.
- **[Unity Perception](https://github.com/Unity-Technologies/com.unity.perception)** — Unity-based synthetic.
- **[Blender](https://www.blender.org/) + python** — DIY rendering.
- **Diffusion-generated (Flux, SDXL)** — image augmentation with control.
- **[Gretel](https://gretel.ai/)** — mostly tabular, some CV.

## Graveyard

- **Labelbox's original free tier** — retired; now enterprise-focused.
- **Amazon SageMaker Ground Truth as a leader** — still exists, but dev experience lags Roboflow.
- **Hand-labeling segmentation masks without SAM** — retired. You shouldn't be doing this in 2026.
- **Google AutoML Vision** — folded into Vertex.

## Last reviewed

2026-04-22.
