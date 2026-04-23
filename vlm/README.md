# Vision-Language Models (VLMs)

> The subtask that ate half of traditional CV. In 2026, a capable VLM is often the right first try for any task where the output is text or structured data from an image.

VLMs changed the calculus of CV deployment. For any task where the output is descriptive ("what's in this image?", "extract the fields from this receipt", "is this X doing Y?"), a VLM is now a reasonable first implementation. You trade per-inference cost and latency for not training anything. For many products, that trade is correct.

The field moves *fast*. The picks below are current as of 2026-04-22 and will age in months, not years.

## Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Commercial flagship | **[Gemini 2.5 Pro](https://deepmind.google/technologies/gemini/pro/)**, **[GPT-5](https://platform.openai.com/docs/models)**, or **[Claude 4 Sonnet/Opus](https://www.anthropic.com/claude)** | Prototyping, low-volume production, when quality matters more than cost |
| Commercial budget | **[Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/flash/)**, **[GPT-5-mini](https://platform.openai.com/docs/models)**, **[Claude Haiku](https://www.anthropic.com/claude/haiku)** | High-volume, latency-sensitive. Often 10× cheaper than flagship. |
| **Open flagship** | **[Qwen3-VL-235B-A22B](https://github.com/QwenLM/Qwen3-VL)** or **[InternVL3-78B](https://github.com/OpenGVLab/InternVL)** | Rivals Gemini-2.5-Pro / GPT-5 on multimodal benchmarks. Self-hosted, data-sensitive, cost-critical at scale. |
| Open small | **[Qwen3-VL-7B](https://github.com/QwenLM/Qwen3-VL)**, **[InternVL3-8B](https://github.com/OpenGVLab/InternVL)**, **[LLaVA-OneVision-7B](https://github.com/LLaVA-VL/LLaVA-NeXT)** | Edge GPU, on-prem, prototyping |

*Reading the picks:* **Operational default** depends on your deployment constraints — for teams with existing Qwen2-VL / InternVL2 pipelines and strict stability requirements, those remain acceptable operational defaults; the move to Qwen3-VL / InternVL3 is a newer strong contender worth testing rather than an urgent upgrade. **Latest strong contender** = Qwen3-VL, InternVL3 (newer generation, better benchmarks). **Research max** shifts monthly in this space; expect this page to age the fastest.

## Why a VLM instead of training a model

Three cases where a VLM is the right first try:

1. **You have no labeled data** and the task is describable in words. Ask the VLM. Beats training from scratch on no data.
2. **The task is "understand a messy image"** (messy receipts, handwritten notes, complicated scenes). Specialized CV models struggle; VLMs are trained on billions of such inputs.
3. **You need flexibility.** VLM prompts change faster than model retraining.

## When NOT to use a VLM

- **Latency-critical** (< 100ms per inference). Even Flash-class VLMs are 500ms+ per call.
- **High-volume inference at low unit cost**. A YOLO detector at $0.0001/image crushes a VLM at $0.01/image when you're at 100M images.
- **Binary classification with plenty of labeled data**. A small fine-tuned CNN will outperform a VLM by a mile on in-distribution tasks at 1/1000th the cost.
- **On-device, no network** (phone apps). The small open VLMs barely fit; they're expensive at inference.
- **Precision-critical structured outputs** where hallucination is unacceptable (legal, medical OCR). VLMs hallucinate; use them with verification.

## The three questions to narrow

1. **Can you send data to a third party?** No → open model (Qwen, InternVL). Yes → commercial API.
2. **What's the per-inference budget?** < $0.001 → not a VLM, use a specialized model. $0.001–0.01 → budget-tier commercial. $0.01+ → any tier.
3. **Do you need structured output?** Yes → Gemini (native JSON), GPT with function calling, or Claude with tool use. Direct prompting often produces malformed JSON.

## Prompting patterns that work

- **Few-shot with 2–3 examples** → significantly better than zero-shot for structured extraction.
- **Schema in the prompt** (a JSON blueprint) → better than "please extract fields."
- **"Think step by step" for complex scenes** → VLMs benefit from explicit reasoning traces.
- **Ground truth image in the prompt** → for consistency, show the VLM a canonical example in the same call.

## Commercial APIs

- **[OpenAI](https://platform.openai.com/docs/models)** — GPT-5, GPT-5-mini, GPT-4o. Mature API. JSON mode + function calling. Image input standard.
- **[Google](https://deepmind.google/technologies/gemini/)** — Gemini 2.5 Pro / Flash. Leads LMArena and WebDevArena for vision + coding. 1M+ token context. Native multimodal from training.
- **[Anthropic](https://www.anthropic.com/claude)** — Claude 4 family (Opus, Sonnet, Haiku). Strongest factuality discipline. "Computer use" capability. PDF input native (parsed as images).
- **[xAI (Grok)](https://x.ai/)** — Grok Vision available. Less mature ecosystem.

## Open models

- **[Qwen3-VL (Alibaba)](https://github.com/QwenLM/Qwen3-VL)** — 2B / 7B / 32B / 235B variants. Flagship Qwen3-VL-235B-A22B rivals Gemini 2.5 Pro and GPT-5 on multimodal benchmarks (Q&A, 2D/3D grounding, video understanding, OCR, document comprehension).
- **[InternVL3 (Shanghai AI Lab)](https://github.com/OpenGVLab/InternVL)** — 1B / 2B / 8B / 14B / 38B / 78B. InternVL3-78B scored 72.2 on MMMU — SOTA among open MLLMs at release. Adds tool use, GUI agents, 3D vision perception.
- **[Qwen2-VL](https://github.com/QwenLM/Qwen2-VL) / InternVL2** — previous generations. Still widely deployed; upgrade when convenient.
- **[LLaVA lineage (LLaVA-OneVision, LLaVA-NeXT)](https://github.com/LLaVA-VL/LLaVA-NeXT)** — academic. Easy to fine-tune. Slightly behind Qwen/InternVL on benchmarks.
- **[CogVLM2 (Tsinghua)](https://github.com/THUDM/CogVLM2)** — 19B. Solid open option.
- **[Molmo (Allen AI)](https://molmo.allenai.org/)** — trained on open data, fully open weights + data. Slightly behind proprietary on most benchmarks.
- **[Gemma 3](https://deepmind.google/models/gemma/)** — Google's open VLM family. Strong mid-tier performer.
- **[Florence-2 (Microsoft)](https://huggingface.co/microsoft/Florence-2-large)** — not a chat VLM but a multi-task vision model (captioning, detection, segmentation). Lightweight (~0.8B).
- **[PaliGemma (Google)](https://huggingface.co/google/paligemma-3b-pt-224)** — 3B VLM, fine-tuning-friendly.

## Running open VLMs

- **[vLLM](https://github.com/vllm-project/vllm)** — the standard serving engine for open models. VLM support added 2024.
- **[Ollama](https://ollama.com/)** — easy local experimentation; limited VLM support, growing.
- **[Hugging Face Transformers](https://github.com/huggingface/transformers)** — reference implementations.
- **[SGLang](https://github.com/sgl-project/sglang)** — alternative serving; strong performance.

## Specialized multimodal tools (not general chat)

- **[CLIP (OpenAI, 2021)](https://github.com/openai/CLIP)** — image-text embedding. The grandfather. Still the default for retrieval/search.
- **[SigLIP (Google, 2023)](https://github.com/google-research/big_vision)** — CLIP improved. Better zero-shot classification.
- **[BLIP-2 (Salesforce)](https://github.com/salesforce/LAVIS/tree/main/projects/blip2)** — image captioning. Superseded by modern VLMs but still in deployed pipelines.

## The Dump

- **[GPT-5 / GPT-4o (OpenAI)](https://platform.openai.com/docs/models)** — closed commercial.
- **[Gemini 2.5 Pro / Flash (Google)](https://deepmind.google/technologies/gemini/)** — closed commercial. LMArena leader.
- **[Claude 4 Opus / Sonnet / Haiku (Anthropic)](https://www.anthropic.com/claude)** — closed commercial.
- **[Grok Vision (xAI)](https://x.ai/)** — closed commercial.
- **[Reka Core / Flash (Reka AI)](https://www.reka.ai/)** — commercial, multimodal-from-training.
- **[Qwen3-VL (Alibaba)](https://github.com/QwenLM/Qwen3-VL)** — open, current flagship.
- **[Qwen2-VL (Alibaba)](https://github.com/QwenLM/Qwen2-VL)** — open, previous generation. Still deployed.
- **[InternVL3](https://github.com/OpenGVLab/InternVL)** — open, SOTA among open MLLMs.
- **[InternVL2](https://github.com/OpenGVLab/InternVL)** — open, previous generation.
- **[LLaVA-OneVision](https://github.com/LLaVA-VL/LLaVA-NeXT)** — open, academic.
- **[LLaVA-NeXT](https://github.com/LLaVA-VL/LLaVA-NeXT)** — open, academic.
- **[Gemma 3 (Google)](https://deepmind.google/models/gemma/)** — open mid-tier.
- **[CogVLM2](https://github.com/THUDM/CogVLM2)** — open.
- **[Molmo (Allen AI)](https://molmo.allenai.org/)** — fully open.
- **[PaliGemma (Google)](https://huggingface.co/google/paligemma-3b-pt-224)** — open, small.
- **[MiniCPM-V](https://github.com/OpenBMB/MiniCPM-V)** — small open VLM.
- **[Florence-2](https://huggingface.co/microsoft/Florence-2-large)** — multi-task vision, open.
- **[CLIP](https://github.com/openai/CLIP) / [SigLIP](https://github.com/google-research/big_vision)** — embedding models, not chat.
- **[BLIP-2](https://github.com/salesforce/LAVIS/tree/main/projects/blip2)** — captioning.
- **[Kosmos-2 (Microsoft)](https://github.com/microsoft/unilm/tree/master/kosmos-2)** — grounded multimodal. Research.
- **[Flamingo (DeepMind, 2022)](https://github.com/mlfoundations/open_flamingo)** — historical, closed, not available.
- **[VILA (NVIDIA)](https://github.com/NVlabs/VILA)** — open VLM family.
- **[Idefics2](https://huggingface.co/HuggingFaceM4/idefics2-8b) / [Idefics3](https://huggingface.co/HuggingFaceM4/Idefics3-8B-Llama3) (Hugging Face)** — open, strong.
- **[Phi-3.5-vision (Microsoft)](https://huggingface.co/microsoft/Phi-3.5-vision-instruct)** — small open VLM.

## Graveyard

- **BLIP-1 as a default captioner** — retired by BLIP-2 and then by modern VLMs.
- **Training a VLM from scratch for a specific task** — 2024 onward, fine-tuning a small open VLM or just using a commercial API is almost always the right call over from-scratch.
- **OCR-specific CNN pipelines for messy documents** — VLMs eat this for breakfast on unstructured inputs.

## Last reviewed

2026-04-22. **Expect this page to age fastest of any in the playbook.** The commercial flagship probably changed between drafting and you reading this.
