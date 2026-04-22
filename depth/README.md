# Depth Estimation

> Getting a depth map from an image or a stereo pair. Monocular depth leapt forward in 2024 with Depth Anything V2; stereo is a different, older, still-relevant story.

Depth splits into two very different problems. Monocular (one image → depth map) is pure ML and has reset twice in 2 years. Stereo (two images → disparity → depth) is mostly classical CV that occasionally gets a neural boost.

## Recommended picks

| Flavor | Pick | When to use |
|--------|------|-------------|
| **Monocular default** | **Depth Anything 3** (ByteDance, ICLR 2026) | Supersedes DA2; single-transformer architecture with DINOv2 encoder. Over 10% improvement on ETH3D vs DA2. |
| Monocular metric depth | **Depth Anything 3 Metric-Large** | `metric_depth = focal * net_output / 300`. Single model for indoor + outdoor metric. |
| Multi-view geometry | **Depth Anything 3** (multi-view mode) | Same model predicts spatially consistent geometry from any number of views. Beats VGGT by 44.3% on camera pose, 25.1% on geometric accuracy. |
| Stereo / depth sensor | **OpenCV StereoSGBM** or **RAFT-Stereo** | If you already have a stereo rig or RGB-D camera. |
| Commercial depth sensor | **Intel RealSense / Orbbec / Luxonis OAK-D** | If hardware is still in the budget. On-device depth, no ML cost. |

## Monocular: why Depth Anything 3 is the default

**Depth Anything 3** (ByteDance Seed, ICLR 2026) reset the field in November 2025. A single plain transformer (vanilla DINOv2 encoder) as backbone, with a singular depth-ray prediction target — no multi-task specialization. Predicts spatially consistent geometry from any number of views, with or without camera poses.

Improvements over DA2 (itself the 2024 default):
- **>10% relative improvement on ETH3D and KITTI** for monocular depth.
- Unified architecture handles multi-view reconstruction too: beats prior SOTA VGGT by 44.3% on camera pose accuracy, 25.1% on geometric accuracy.
- The same checkpoint handles monocular, stereo, and multi-view — no switching models.

Install via [GitHub](https://github.com/ByteDance-Seed/Depth-Anything-3). Fast on GPU; usable but slow on CPU.

"Relative depth" is what you want for AR occlusion, portrait mode blur, novel-view synthesis, any use case where the ratio matters more than the metric scale.

## Metric monocular — when you need meters

DA3 ships a dedicated **DA3 Metric-Large** checkpoint fine-tuned for metric depth. Conversion formula in the docs: `metric_depth = focal * net_output / 300` where `focal` is the camera focal length in pixels. Handles indoor + outdoor.

For robotics or measurement use cases with high reliability requirements, a stereo rig or RGB-D sensor is still more consistent than monocular metric depth across domains.

Historical alternatives (still seen in deployed pipelines):
- **ZoeDepth (Intel ISL, 2023)** — indoor + outdoor metric depth. Pre-DA3.
- **Depth Anything V2 Metric** — DA2 metric fine-tunes. Pre-DA3.
- **Metric3D** — universal metric depth via camera intrinsics.

## Stereo — the old reliable

If you have two cameras with known baseline, classical stereo matching (disparity → depth via `depth = baseline * focal / disparity`) is fast, deterministic, and gives metric depth.

- **OpenCV StereoSGBM** — semi-global matching. ~30 FPS on CPU for 720p. The 2000s-era default that still works.
- **RAFT-Stereo (2021)** — neural stereo. Slower but more accurate on edges and textureless surfaces.

If you don't already have a stereo setup, don't add one just for depth; Depth Anything V2 is probably enough.

## When to pick something else

- **Video with temporal consistency matters** (no flickering frame-to-frame) → Depth Anything V2 has video-consistent variants. Or post-process with temporal smoothing.
- **Point clouds / 3D reconstruction** → COLMAP or InstantNGP / Gaussian Splatting territory, not single-image depth.
- **Autonomous driving** → you probably want lidar + radar + stereo, not monocular. If monocular, specialized self-supervised models (Monodepth2 lineage) that trained on driving scenes.
- **Portrait mode / background blur** → the dedicated mobile SoC pipelines (Apple / Google) ship specialized small models. For DIY: MiDaS or Depth Anything V2 Small suffices.

## The three questions to narrow

1. **Do you need metric distance, or just relative?** Relative → Depth Anything V2. Metric → ZoeDepth, or add a stereo/depth sensor.
2. **Single image or video?** Single → any. Video → pick with temporal consistency.
3. **Do you already have a stereo rig or depth sensor?** Yes → use it (cheaper, deterministic). No → monocular ML.

## The Dump

- **Stereo SGBM (OpenCV, classical)** — the CPU-era default. Still effective.
- **RAFT-Stereo (2021)** — neural stereo, slow, accurate.
- **CREStereo (2022)** — refinement-based neural stereo.
- **MiDaS (Intel ISL, 2019)** — the original "robust monocular depth." Relative.
- **MiDaS v3.x / DPT (2021)** — transformer-based MiDaS. Strong for years.
- **Monodepth2 (2019)** — self-supervised from video, still used in driving.
- **Depth Anything (2024)** — massive dataset + semi-supervised training.
- **Depth Anything V2 (mid-2024)** — improved training. Pre-DA3.
- **Depth Anything 3 (ByteDance, Nov 2025, ICLR 2026)** — current SOTA; single-transformer architecture for depth + multi-view geometry.
- **ZoeDepth (2023)** — metric depth, indoor+outdoor.
- **Marigold (2023)** — diffusion-based depth, slower, very clean outputs.
- **Metric3D v2** — universal metric depth with intrinsics.
- **Intel RealSense** — depth camera hardware (D435i, D455, etc.). Active IR stereo.
- **Orbbec Astra / Femto** — budget depth cameras.
- **Luxonis OAK-D** — embedded depth + detection in one device.
- **iPhone TrueDepth / LiDAR** — on-device depth via Apple's ARKit. Very accurate at short range.
- **Kinect (deprecated)** — historical Microsoft depth sensor. Replaced by Azure Kinect, also deprecated. Niche.
- **StructureFromMotion (SfM) tools** — COLMAP for multi-image depth + pose. Not real-time, not single-image.
- **Gaussian Splatting** — not depth per se, but a modern 3D reconstruction alternative.

## Graveyard

- **MiDaS as the monocular default** — retired by Depth Anything V2 in 2024.
- **Monodepth (original, 2017)** — retired by better self-supervised variants.
- **Kinect v1/v2 as a default depth sensor** — Microsoft discontinued; community moved to RealSense, Orbbec, Luxonis.

## Last reviewed

2026-04-22.
