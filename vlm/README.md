# Vision-Language Models (VLMs)

> The subtask that ate half of traditional CV. In 2026, a capable VLM is often the right first try for any task where the output is text or structured data from an image.

VLMs changed the calculus of CV deployment. For any task where the output is descriptive ("what's in this image?", "extract the fields from this receipt", "is this X doing Y?"), a VLM is now a reasonable first implementation. You trade per-inference cost and latency for not training anything. For many products, that trade is correct.

The field moves *fast*. The picks below are current as of 2026-04-22 and will age in months, not years.

## Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Commercial flagship | **Gemini 2.5 Pro**, **GPT-5**, or **Claude 4 Sonnet/Opus** | Prototyping, low-volume production, when quality matters more than cost |
| Commercial budget | **Gemini 2.5 Flash**, **GPT-5-mini**, **Claude Haiku** | High-volume, latency-sensitive. Often 10× cheaper than flagship. |
| **Open flagship** | **Qwen3-VL-235B-A22B** or **InternVL3-78B** | Rivals Gemini-2.5-Pro / GPT-5 on multimodal benchmarks. Self-hosted, data-sensitive, cost-critical at scale. |
| Open small | **Qwen3-VL-7B**, **InternVL3-8B**, **LLaVA-OneVision-7B** | Edge GPU, on-prem, prototyping |

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

- **OpenAI** — GPT-5, GPT-5-mini, GPT-4o. Mature API. JSON mode + function calling. Image input standard.
- **Google** — Gemini 2.5 Pro / Flash. Leads LMArena and WebDevArena for vision + coding. 1M+ token context. Native multimodal from training.
- **Anthropic** — Claude 4 family (Opus, Sonnet, Haiku). Strongest factuality discipline. "Computer use" capability. PDF input native (parsed as images).
- **xAI (Grok)** — Grok Vision available. Less mature ecosystem.

## Open models

- **Qwen3-VL (Alibaba)** — 2B / 7B / 32B / 235B variants. Flagship Qwen3-VL-235B-A22B rivals Gemini 2.5 Pro and GPT-5 on multimodal benchmarks (Q&A, 2D/3D grounding, video understanding, OCR, document comprehension).
- **InternVL3 (Shanghai AI Lab)** — 1B / 2B / 8B / 14B / 38B / 78B. InternVL3-78B scored 72.2 on MMMU — SOTA among open MLLMs at release. Adds tool use, GUI agents, 3D vision perception.
- **Qwen2-VL / InternVL2** — previous generations. Still widely deployed; upgrade when convenient.
- **LLaVA lineage (LLaVA-OneVision, LLaVA-NeXT)** — academic. Easy to fine-tune. Slightly behind Qwen/InternVL on benchmarks.
- **CogVLM2 (Tsinghua)** — 19B. Solid open option.
- **Molmo (Allen AI)** — trained on open data, fully open weights + data. Slightly behind proprietary on most benchmarks.
- **Gemma 3** — Google's open VLM family. Strong mid-tier performer.
- **Florence-2 (Microsoft)** — not a chat VLM but a multi-task vision model (captioning, detection, segmentation). Lightweight (~0.8B).
- **PaliGemma (Google)** — 3B VLM, fine-tuning-friendly.

## Running open VLMs

- **vLLM** — the standard serving engine for open models. VLM support added 2024.
- **Ollama** — easy local experimentation; limited VLM support, growing.
- **Hugging Face Transformers** — reference implementations.
- **SGLang** — alternative serving; strong performance.

## Specialized multimodal tools (not general chat)

- **CLIP (OpenAI, 2021)** — image-text embedding. The grandfather. Still the default for retrieval/search.
- **SigLIP (Google, 2023)** — CLIP improved. Better zero-shot classification.
- **BLIP-2 (Salesforce)** — image captioning. Superseded by modern VLMs but still in deployed pipelines.

## The Dump

- **GPT-5 / GPT-4o (OpenAI)** — closed commercial.
- **Gemini 2.5 Pro / Flash (Google)** — closed commercial. LMArena leader.
- **Claude 4 Opus / Sonnet / Haiku (Anthropic)** — closed commercial.
- **Grok Vision (xAI)** — closed commercial.
- **Reka Core / Flash (Reka AI)** — commercial, multimodal-from-training.
- **Qwen3-VL (Alibaba)** — open, current flagship.
- **Qwen2-VL (Alibaba)** — open, previous generation. Still deployed.
- **InternVL3** — open, SOTA among open MLLMs.
- **InternVL2** — open, previous generation.
- **LLaVA-OneVision** — open, academic.
- **LLaVA-NeXT** — open, academic.
- **Gemma 3 (Google)** — open mid-tier.
- **CogVLM2** — open.
- **Molmo (Allen AI)** — fully open.
- **PaliGemma (Google)** — open, small.
- **MiniCPM-V** — small open VLM.
- **Florence-2** — multi-task vision, open.
- **CLIP / SigLIP** — embedding models, not chat.
- **BLIP-2** — captioning.
- **Kosmos-2 (Microsoft)** — grounded multimodal. Research.
- **Flamingo (DeepMind, 2022)** — historical, closed, not available.
- **VILA (NVIDIA)** — open VLM family.
- **Idefics2 / Idefics3 (Hugging Face)** — open, strong.
- **Phi-3.5-vision (Microsoft)** — small open VLM.

## Graveyard

- **BLIP-1 as a default captioner** — retired by BLIP-2 and then by modern VLMs.
- **Training a VLM from scratch for a specific task** — 2024 onward, fine-tuning a small open VLM or just using a commercial API is almost always the right call over from-scratch.
- **OCR-specific CNN pipelines for messy documents** — VLMs eat this for breakfast on unstructured inputs.

## Last reviewed

2026-04-22. **Expect this page to age fastest of any in the playbook.** The commercial flagship probably changed between drafting and you reading this.
