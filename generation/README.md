# Image Generation

> Diffusion models, image edits, controllable synthesis. The default open pick flipped from SDXL to Flux in 2024. Commercial keeps its lead on prompt adherence.

Generation is a distinct world from perception — different libraries, different compute profiles, different failure modes. Most CV engineers don't need it early; it becomes relevant for content tooling, synthetic data, editing, or generative UX.

## Recommended picks

| Use case | Pick | When to use |
|----------|------|-------------|
| Commercial flagship | **[Midjourney v7](https://www.midjourney.com/)**, **[Flux 2 Pro](https://blackforestlabs.ai/)**, or **[DALL-E 3](https://openai.com/index/dall-e-3/)** | Marketing / hero images; prompt adherence matters; quality > control |
| **Open default (photorealism)** | **[Flux 2](https://github.com/black-forest-labs/flux)** (Black Forest Labs, Nov 2025) | Up to 4MP output, best open photorealism, strong prompt adherence |
| **Open default (text-in-image)** | **[Qwen-Image](https://github.com/QwenLM/Qwen-Image)** (Alibaba, Apache 2.0) | Best-in-class multilingual text rendering within images. Commercial-friendly license. |
| Stable / mature open | **[SDXL 1.0](https://github.com/Stability-AI/generative-models) + LoRAs** | Massive ecosystem of fine-tunes and community tools; prefer over Flux only if you need an existing LoRA |
| Controllable generation | **Flux + [ControlNet](https://github.com/lllyasviel/ControlNet)** or **SDXL + ControlNet** | Pose-controlled, edge-controlled, depth-controlled generation |
| Editing (img2img / inpainting) | **[Flux Fill](https://huggingface.co/black-forest-labs/FLUX.1-Fill-dev)**, **SDXL Inpainting**, or a commercial "edit" API | Targeted regions of an existing image |
| Fast / real-time | **[SDXL Turbo](https://huggingface.co/stabilityai/sdxl-turbo)**, **[SD Lightning](https://huggingface.co/ByteDance/SDXL-Lightning)**, or **[Flux Schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell)** | Live preview, sketch-to-image, interactive apps |

## Why Flux 2 is the current open leader

**Flux 2** (Black Forest Labs, November 2025) is the biggest open-model step forward since SDXL. Superior photorealism, better prompt comprehension, up to 4MP output. Best single choice for portrait / product / hero image quality.

Flux family as of 2026:
- **Flux 2 Pro** — API-only commercial, max quality.
- **Flux.1 [dev]** — 12B params, non-commercial license. Still widely used because of the maturing ecosystem.
- **Flux.1 [schnell]** — Apache 2 license, 1-step or 4-step generation. Use for self-hosted commercial.

For self-hosted commercial: Flux.1 [schnell] (Apache) or Qwen-Image (Apache). For highest-quality self-hosted with non-commercial acceptable: Flux 2 via HF weights or Flux.1 [dev].

## Why Qwen-Image for text-in-image

Qwen-Image (Alibaba, Apache 2.0) integrates language and layout reasoning directly into the architecture. Best-in-class multilingual text rendering within images — font consistency, spatial alignment, complex backgrounds. If your use case involves typography in the generated image, Qwen-Image beats Flux and SDXL on that axis. And it's Apache 2, which matters for commercial use.

## SDXL — still the mature ecosystem

SDXL 1.0 shipped mid-2023 and spawned the largest ecosystem in image generation: hundreds of thousands of LoRAs on Civitai, dozens of ControlNet variants, strong community tooling (ComfyUI, Automatic1111). It's sometimes the right pick *because* of the ecosystem, not despite age:

- You need a specific style LoRA → probably on SDXL, not Flux.
- You need IP-Adapter for face consistency → mature on SDXL.
- You're using an existing ComfyUI graph → it's SDXL-shaped.

## Controllable generation

Plain text → image is often not enough for production use. You usually want to constrain output — pose a character, preserve layout, edit one region. That's ControlNet territory.

- **[ControlNet](https://github.com/lllyasviel/ControlNet)** (Zhang et al., 2023) — the control-by-condition framework. Variants for pose (OpenPose / DWPose input), depth, edges (Canny / SoftEdge), segmentation, scribble, lineart.
- **[IP-Adapter](https://github.com/tencent-ailab/IP-Adapter)** — image prompting; condition the output on a reference image's style or identity.
- **[T2I-Adapter](https://github.com/TencentARC/T2I-Adapter)** — lighter-weight alternative to ControlNet.

Both Flux and SDXL have ControlNet support. SDXL's ecosystem is broader; Flux is catching up.

## When to pick something else

- **Consistent characters across many images** → specialized pipelines (LoRA training on the character, or InstantID / PhotoMaker).
- **Text rendering in the image** (signs, logos) → Flux is the open winner. DALL-E 3 and Midjourney also strong. SDXL is weak here.
- **Video generation** → different world. See *Video Generation* dump below. Moving target.
- **3D-aware generation** → NeRF / Gaussian Splatting / 3D-native models. Out of scope for this page.

## Running Flux / SDXL locally

- **[ComfyUI](https://github.com/comfyanonymous/ComfyUI)** — node-graph UI. The power-user default. Every ControlNet, LoRA, adapter works here first.
- **[Automatic1111 WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)** — classic interface. SDXL-focused, less current on Flux.
- **[Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge) / [Fooocus](https://github.com/lllyasviel/Fooocus) / [SwarmUI](https://github.com/mcmonkeyprojects/SwarmUI)** — alternative UIs. Fooocus in particular is "simple mode" for SDXL.
- **[Diffusers (Hugging Face)](https://github.com/huggingface/diffusers)** — the Python library. Script-first.
- **[InvokeAI](https://github.com/invoke-ai/InvokeAI)** — another UI, artist-friendly.

## Commercial APIs

- **[Midjourney](https://www.midjourney.com/)** — Discord/web interface. Highest aesthetic quality. No API until recently (now limited beta).
- **[DALL-E 3](https://openai.com/index/dall-e-3/)** (via OpenAI API) — strong prompt adherence, tight content policy.
- **[Imagen 3](https://deepmind.google/technologies/imagen-3/)** (via Google AI Studio / Vertex) — fast, strong.
- **[Stable Diffusion 3 Large](https://stability.ai/news/stable-diffusion-3)** (via Stability AI API) — the commercial variant of SD3.
- **[Flux Pro](https://blackforestlabs.ai/)** (via Black Forest Labs / replicate) — hosted.
- **[Ideogram](https://ideogram.ai/)** — specialized in text-in-image.
- **[Leonardo](https://leonardo.ai/) / [Stability](https://stability.ai/) / [Replicate](https://replicate.com/) / [fal.ai](https://fal.ai/)** — aggregator/hosting platforms.

## Video generation (fast-moving, verify before relying on)

Leaderboard as of April 2026 (these rotate every 1–2 months):

### Commercial
- **[Kling 3.0](https://www.klingai.com/)** (Kuaishou, Feb 2026) — multi-shot sequences 3–15 seconds, 4K native, subject consistency across shots. Cost-effective (~$0.50/clip).
- **[Veo 3.1](https://deepmind.google/technologies/veo/)** (Google, Jan 2026) — 4K native, best-in-class lip sync for talking heads.
- **[Seedance 2.0](https://seed.bytedance.com/seedance/)** (ByteDance, Feb 2026) — first with unified audio-video joint generation, multi-shot storytelling from a single prompt, phoneme-level lip sync in 8+ languages.
- **[Runway Gen-4](https://runwayml.com/)** — commercial, broad creative tooling.
- **[Luma Dream Machine](https://lumalabs.ai/dream-machine)** — commercial.

### Open
- **[Wan 2.6](https://github.com/Wan-Video/Wan2.1)** (Alibaba) — open-weight, strong, full control over the generation process.
- **[HunyuanVideo](https://github.com/Tencent/HunyuanVideo)** (Tencent) — open weights.
- **[LTX-Video](https://github.com/Lightricks/LTX-Video)** — open, fast.
- **[CogVideoX](https://github.com/THUDM/CogVideo)** — open.
- **[AnimateDiff](https://github.com/guoyww/AnimateDiff)** — motion LoRA on top of SD/SDXL. Lower quality than dedicated video models.

### Graveyard (video)
- **Sora (OpenAI)** — **shut down March 24, 2026**, six months after launch. Do not recommend.
- **Sora 2** — preceded the shutdown; coherent prompts and camera control were praised.

Video generation is moving faster than image generation and the recommendations here will age inside 3 months. Verify before citing.

## The Dump

### Diffusion model families
- **[Stable Diffusion 1.5 (SD 1.5)](https://huggingface.co/runwayml/stable-diffusion-v1-5)** — the classic. Still running in many pipelines for backwards compat.
- **[SDXL 1.0 (Stability AI, 2023)](https://github.com/Stability-AI/generative-models)** — mature open default.
- **[SD 3 / SD 3.5 (Stability AI, 2024)](https://stability.ai/news/stable-diffusion-3-5)** — mixed reception, license complications.
- **[Flux.1 (Black Forest Labs, 2024)](https://github.com/black-forest-labs/flux)** — the current open leader.
- **[Pixart-α](https://github.com/PixArt-alpha/PixArt-alpha) / [Pixart-Σ](https://github.com/PixArt-alpha/PixArt-sigma)** — alternative open model families.
- **[Kolors (Kuaishou)](https://github.com/Kwai-Kolors/Kolors)** — strong Chinese-text generation.
- **[Playground v3](https://playground.com/)** — aesthetic-tuned SDXL variant.
- **[Juggernaut / DreamShaper / RealVis](https://civitai.com/)** — popular SDXL fine-tunes on Civitai.

### Tools
- **[ComfyUI](https://github.com/comfyanonymous/ComfyUI)** — node-based UI, most flexible.
- **[Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui)** — classic WebUI.
- **[Fooocus](https://github.com/lllyasviel/Fooocus) / [Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge) / [InvokeAI](https://github.com/invoke-ai/InvokeAI)** — alternative UIs.
- **[Diffusers](https://github.com/huggingface/diffusers)** — Python library.
- **[OneTrainer](https://github.com/Nerogar/OneTrainer) / [Kohya](https://github.com/kohya-ss/sd-scripts)** — LoRA training.

### Control / edit
- **[ControlNet variants](https://github.com/lllyasviel/ControlNet)** — Canny, Depth, Pose, Scribble, etc.
- **[IP-Adapter](https://github.com/tencent-ailab/IP-Adapter)** — image-as-prompt.
- **[InstantID](https://github.com/InstantID/InstantID) / [PhotoMaker](https://github.com/TencentARC/PhotoMaker)** — identity preservation.
- **[LCM](https://github.com/luosiallen/latent-consistency-model) / [Hyper-SD](https://huggingface.co/ByteDance/Hyper-SD) / [Turbo](https://huggingface.co/stabilityai/sdxl-turbo) / [Lightning](https://huggingface.co/ByteDance/SDXL-Lightning)** — few-step sampling.

### Commercial
- **Midjourney, DALL-E, Imagen, Flux Pro, Ideogram** — see above.

## Graveyard

- **SD 1.5 as a default for new work** — retired; use SDXL or Flux unless ecosystem-locked.
- **DALL-E 2** — retired by OpenAI.
- **Disco Diffusion / VQ-VAE-2** — historical.
- **Original ControlNet 1.0 weights** — succeeded by 1.1 and SDXL-native variants.

## Last reviewed

2026-04-22. Generation is second-fastest-moving page after VLM.
