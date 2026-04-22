# Image Classification

> Given an image, return a label (or a probability distribution over labels). The oldest CV task and mostly a solved one — but the "solved" part has shifted from CNNs to embeddings + a shallow head.

Pure image classification is rarely the primary product in 2026. It's usually a component: a subroutine inside detection, or a gate on top of an embedding. But when it *is* the task — "is this X or Y or Z?" — the field has consolidated into a few clear picks.

## Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Zero-shot (no training) | **CLIP** or **SigLIP** + cosine similarity to text labels | When you have no training data and the classes are describable in words. |
| **Default with labeled data** | **Fine-tune a timm model** (ConvNeXt, ViT, EfficientNet) | Classic supervised classification. 100s–1000s of examples per class. |
| Max accuracy | **DINOv3 embeddings + linear probe** or **ViT-L** fine-tune | Few-shot, transfer learning. |
| Edge | **MobileNetV3** or **EfficientNet-Lite** | On-device, small footprint. |

## Why zero-shot CLIP is often the right first try

CLIP (OpenAI, 2021) and its successor SigLIP (Google, 2023) produce image embeddings and text embeddings in a shared space. Cosine similarity between an image embedding and a text embedding tells you how well "this text describes this image."

Zero-shot classification with CLIP:
```
text_candidates = ["a photo of a dog", "a photo of a cat", "a photo of a car"]
image_embedding = clip.encode_image(image)
text_embeddings = [clip.encode_text(t) for t in text_candidates]
scores = image_embedding @ text_embeddings.T
prediction = text_candidates[scores.argmax()]
```

5 lines. No training. Works shockingly well on common-object classes.

When CLIP fails:
- Fine-grained distinctions (bird species, product SKUs) — classes CLIP wasn't trained to distinguish.
- Domain gap (medical, satellite, industrial defects).
- Highly specific labels ("defective weld type B" vs "defective weld type A").

For those, fine-tune.

## Fine-tuning a timm model — the supervised default

`timm` (Hugging Face / Ross Wightman) is the reference library for pretrained image models. 1,000+ model variants, consistent API, trained on ImageNet-21K for strong transfer.

Picks within timm, roughly:
- **ConvNeXt-base** — best balance of speed + accuracy in 2026 for ~100M-param budget.
- **ViT-B/16** — the ViT default. Scales to larger variants if you have data.
- **EfficientNet-B3 / EfficientNetV2-S** — edge-leaning.
- **Swin Transformer V2** — alternative to ViT.
- **ResNet-50** — historical baseline. Still in deployed pipelines.

Typical recipe: load the pretrained model, replace the classification head with your N classes, fine-tune with low learning rate on the backbone + higher LR on the head.

## DINOv3 + linear probe — few-shot / transfer (current default)

**DINOv3** (Meta, August 2025) scaled DINOv2 by 6× in parameters (to 7B) and 12× in training data (to 1.7B images). Key innovation: *Gram anchoring* prevents dense feature map degradation during long training. First time a self-supervised vision model outperforms weakly-supervised models across a broad range of tasks — from fine-grained classification to semantic segmentation to video object tracking.

Released under a **commercial license** — both training code and pre-trained backbones. Real-world deployments already: World Resources Institute for forestry (tree canopy height error 4.1m → 1.2m in Kenya), NASA JPL for Mars rover vision.

Standard recipe, unchanged from DINOv2:

```
embeddings = dinov3.encode(images)  # frozen, no training
classifier = LogisticRegression().fit(embeddings[:N], labels[:N])
```

With 10–50 examples per class, DINOv3 + linear probe often beats fine-tuning a smaller model from scratch. The current default for low-data classification, transfer learning, and as a backbone for downstream models (RF-DETR uses DINOv2; a DINOv3-backed detector is a natural next step).

DINOv2 is still fine — similar recipe, slightly less accuracy, smaller. Migrate when convenient.

## When to pick something else

- **Hierarchical classification** (order → family → genus → species) → a custom architecture with hierarchical heads, or post-process with a taxonomy.
- **Multi-label** (multiple labels per image) → same models, swap softmax for sigmoid.
- **Regression** (age, quality score) → same backbones, different head + loss.
- **Face classification (who is this person)** → see `face/` section. Uses embeddings + nearest-neighbor, not softmax classifier.
- **Out-of-distribution detection** → embedding distance to training set. CLIP/DINOv2 embeddings + kNN, then threshold.

## The three questions to narrow

1. **Do you have labeled data?** No → CLIP zero-shot. Yes → fine-tune or linear probe.
2. **How much data?** < 100 per class → DINOv2 linear probe. 100–10K → timm fine-tune. 10K+ → train from scratch or fine-tune large models.
3. **Edge or server?** Edge → MobileNetV3 / EfficientNet-Lite. Server → ConvNeXt / ViT.

## The Dump

### Backbones (still in use in 2026)
- **ResNet-50 / 101 (2015)** — the historical default. Still solid.
- **ResNeXt, Wide ResNet** — ResNet variants, minor improvements.
- **DenseNet** — connection-dense. Historical.
- **MobileNet V1/V2/V3** — mobile-efficient.
- **EfficientNet B0–B7 / V2** — compound scaling.
- **ConvNeXt / ConvNeXtV2 (2022/2023)** — modernized CNN. Competitive with ViT at similar size.
- **ViT / ViT-B/L/H** — the transformer default.
- **Swin / Swin V2** — hierarchical ViT.
- **DeiT** — data-efficient ViT training.
- **BEiT, MAE** — self-supervised pretraining for ViT.
- **CoAtNet, EfficientFormer** — CNN+transformer hybrids.
- **RegNet (Meta)** — Neural Architecture Search results. Strong.

### Self-supervised / embedding models
- **CLIP (OpenAI, 2021)** — image-text contrastive.
- **OpenCLIP** — open re-implementation.
- **SigLIP (Google, 2023)** — improved CLIP.
- **DINOv1 / DINOv2 / DINOv3 (Meta)** — self-supervised ViT. DINOv3 (Aug 2025) is the current default; 7B params, 1.7B training images, commercial license.
- **MAE (Masked Autoencoder)** — self-supervised pretraining.
- **I-JEPA (Meta)** — joint embedding, self-supervised.

### Libraries
- **timm (Hugging Face)** — 1,000+ pretrained models. The reference.
- **torchvision** — PyTorch's built-in model zoo. Smaller than timm.
- **Keras Applications** — TF/Keras pretrained models.

### Datasets
- **ImageNet-1K** — 1000-class classification benchmark.
- **ImageNet-21K** — 21K classes, used for pretraining.
- **iNaturalist** — fine-grained species classification.
- **CIFAR-10 / 100** — toys.
- **Places365** — scene classification.

## Graveyard

- **AlexNet (2012)** — historical.
- **VGG (2014)** — the "deep but simple" era. Retired.
- **Training from scratch on ImageNet** — retired for most use cases. Pretrained + fine-tune is almost always better.
- **Ad-hoc CNN architectures in Keras** — retired. Use timm or torchvision backbones.

## Last reviewed

2026-04-22.
