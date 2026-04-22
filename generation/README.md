# Image Generation

> Diffusion models, image edits, controllable synthesis. The default open pick flipped from SDXL to Flux in 2024. Commercial keeps its lead on prompt adherence.

Generation is a distinct world from perception — different libraries, different compute profiles, different failure modes. Most CV engineers don't need it for product #1; it becomes relevant for content tooling, synthetic data, editing, or generative UX.

## Recommended picks

| Use case | Pick | When to use |
|----------|------|-------------|
| Commercial flagship | **Midjourney v7**, **Flux Pro**, or **DALL-E 3** | Marketing / hero images; prompt adherence matters; quality > control |
| **Open default** | **Flux.1 [dev]** | Self-hosted, high-quality open image generation |
| Stable / mature open | **SDXL 1.0 + LoRAs** | Massive ecosystem of fine-tunes and tools; prefer over Flux only if you need an existing LoRA |
| Controllable generation | **Flux + ControlNet** or **SDXL + ControlNet** | Pose-controlled, edge-controlled, depth-controlled generation |
| Editing (img2img / inpainting) | **Flux Fill**, **SDXL Inpainting**, or a commercial "edit" API | Targeted regions of an existing image |
| Fast / real-time | **SDXL Turbo**, **SD Lightning**, or **Flux Schnell** | Live preview, sketch-to-image, interactive apps |

## Why Flux is the new open default

Flux.1 (Black Forest Labs, the team behind Stable Diffusion's original work, 2024) shipped open weights that beat SDXL on prompt adherence, aesthetic quality, and text rendering. Three variants:

- **Flux.1 [dev]** — non-commercial license, 12B params, best quality.
- **Flux.1 [schnell]** — Apache 2 license, faster, 1-step or 4-step generation.
- **Flux.1 [pro]** — API-only commercial, highest quality, not self-hostable.

For self-hosted production: `Flux.1 [schnell]` (Apache) or `Flux.1 [dev]` (non-commercial).

## SDXL — still the mature ecosystem

SDXL 1.0 shipped mid-2023 and spawned the largest ecosystem in image generation: hundreds of thousands of LoRAs on Civitai, dozens of ControlNet variants, strong community tooling (ComfyUI, Automatic1111). It's sometimes the right pick *because* of the ecosystem, not despite age:

- You need a specific style LoRA → probably on SDXL, not Flux.
- You need IP-Adapter for face consistency → mature on SDXL.
- You're using an existing ComfyUI graph → it's SDXL-shaped.

## Controllable generation

Plain text → image is often not enough for production use. You usually want to constrain output — pose a character, preserve layout, edit one region. That's ControlNet territory.

- **ControlNet** (Zhang et al., 2023) — the control-by-condition framework. Variants for pose (OpenPose / DWPose input), depth, edges (Canny / SoftEdge), segmentation, scribble, lineart.
- **IP-Adapter** — image prompting; condition the output on a reference image's style or identity.
- **T2I-Adapter** — lighter-weight alternative to ControlNet.

Both Flux and SDXL have ControlNet support. SDXL's ecosystem is broader; Flux is catching up.

## When to pick something else

- **Consistent characters across many images** → specialized pipelines (LoRA training on the character, or InstantID / PhotoMaker).
- **Text rendering in the image** (signs, logos) → Flux is the open winner. DALL-E 3 and Midjourney also strong. SDXL is weak here.
- **Video generation** → different world. See *Video Generation* dump below. Moving target.
- **3D-aware generation** → NeRF / Gaussian Splatting / 3D-native models. Out of scope for this page.

## Running Flux / SDXL locally

- **ComfyUI** — node-graph UI. The power-user default. Every ControlNet, LoRA, adapter works here first.
- **Automatic1111 WebUI** — classic interface. SDXL-focused, less current on Flux.
- **Forge / Fooocus / SwarmUI** — alternative UIs. Fooocus in particular is "simple mode" for SDXL.
- **Diffusers (Hugging Face)** — the Python library. Script-first.
- **InvokeAI** — another UI, artist-friendly.

## Commercial APIs

- **Midjourney** — Discord/web interface. Highest aesthetic quality. No API until recently (now limited beta).
- **DALL-E 3** (via OpenAI API) — strong prompt adherence, tight content policy.
- **Imagen 3** (via Google AI Studio / Vertex) — fast, strong.
- **Stable Diffusion 3 Large** (via Stability AI API) — the commercial variant of SD3.
- **Flux Pro** (via Black Forest Labs / replicate) — hosted.
- **Ideogram** — specialized in text-in-image.
- **Leonardo / Stability / Replicate / fal.ai** — aggregator/hosting platforms.

## Video generation (brief notes, fast-moving)

- **Sora (OpenAI)** — commercial, long coherent video.
- **Veo 3 (Google)** — commercial, strong.
- **Runway Gen-4** — commercial.
- **Kling (Kuaishou)** — commercial, strong physics.
- **Luma Dream Machine** — commercial.
- **HunyuanVideo (Tencent)** — open weights.
- **Wan2.1 (Alibaba)** — open weights.
- **LTX-Video** — open, fast.
- **CogVideoX** — open.
- **AnimateDiff** — motion LoRA on top of SD/SDXL. Lower quality than dedicated video models.

Video generation is moving faster than image generation and the recommendations here will age inside 6 months.

## The Dump

### Diffusion model families
- **Stable Diffusion 1.5 (SD 1.5)** — the classic. Still running in many pipelines for backwards compat.
- **SDXL 1.0 (Stability AI, 2023)** — mature open default.
- **SD 3 / SD 3.5 (Stability AI, 2024)** — mixed reception, license complications.
- **Flux.1 (Black Forest Labs, 2024)** — the current open leader.
- **Pixart-α / Pixart-Σ** — alternative open model families.
- **Kolors (Kuaishou)** — strong Chinese-text generation.
- **Playground v3** — aesthetic-tuned SDXL variant.
- **Juggernaut / DreamShaper / RealVis** — popular SDXL fine-tunes on Civitai.

### Tools
- **ComfyUI** — node-based UI, most flexible.
- **Automatic1111** — classic WebUI.
- **Fooocus / Forge / InvokeAI** — alternative UIs.
- **Diffusers** — Python library.
- **OneTrainer / Kohya** — LoRA training.

### Control / edit
- **ControlNet variants** — Canny, Depth, Pose, Scribble, etc.
- **IP-Adapter** — image-as-prompt.
- **InstantID / PhotoMaker** — identity preservation.
- **LCM / Hyper-SD / Turbo / Lightning** — few-step sampling.

### Commercial
- **Midjourney, DALL-E, Imagen, Flux Pro, Ideogram** — see above.

## Graveyard

- **SD 1.5 as a default for new work** — retired; use SDXL or Flux unless ecosystem-locked.
- **DALL-E 2** — retired by OpenAI.
- **Disco Diffusion / VQ-VAE-2** — historical.
- **Original ControlNet 1.0 weights** — succeeded by 1.1 and SDXL-native variants.

## Last reviewed

2026-04-22. Generation is second-fastest-moving page after VLM.
