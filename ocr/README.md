# OCR / Document AI

> Extracting text from images. In 2026 this subtask is bifurcating fast: classical OCR still wins on clean printed pages at scale, but VLMs have eaten most of the messy real-world work.

The field has three distinct use cases with different picks. Don't pick one tool and use it for all three.

## Recommended picks

| Use case | Pick | When to use |
|----------|------|-------------|
| **Document parsing SOTA (open)** | **PaddleOCR-VL-1.5** (Baidu, 0.9B VLM) | 94.5% on OmniDocBench v1.5. Handles skew, warp, illumination, screen photos. 111 languages. |
| Messy real-world (handwriting, weird contexts) | **A flagship VLM (Gemini 2.5, GPT-5, Claude 4)** | When you want max accuracy and can afford per-page cost. Beats traditional OCR on unstructured inputs. |
| Clean printed documents at scale | **PP-OCRv5** (lightweight PaddleOCR) | Free, 1st on avg 1-edit-distance across OmniDocBench, beats GOT-OCR-0.5B / Qwen2.5-VL-72B at a fraction of size. |
| English-only + local + fast | **Tesseract 5** | Zero-dependency batch processing of clean text. |
| Structured document understanding | **Donut** or **LayoutLMv3** | Form key-value extraction with a defined schema. Training-required. |

## The big shift (2024 → 2026)

Until 2023, OCR meant Tesseract/PaddleOCR for clean, or a dedicated pipeline (Donut, LayoutLM) for forms. Post-processing the model's output was where the engineering time went.

**2024:** vision-language models (GPT-4V, Gemini, Claude, Qwen-VL) started doing "read this image" as well as or better than classical OCR on messy inputs.

**2025–2026:** the two worlds merged. The current SOTA on OmniDocBench v1.5 (94.5%) is **PaddleOCR-VL-1.5**, a **0.9B VLM** from Baidu — smaller than the classical pipelines, faster than flagship VLMs, and trained specifically for document parsing. For the first time there's a single open model that wins on both accuracy *and* deployability for documents.

Where each tier still wins:
- **PaddleOCR-VL-1.5** — the new default for document parsing (forms, receipts, PDFs, multilingual, 111 languages).
- **Flagship VLMs (Gemini 2.5, GPT-5, Claude 4)** — for inputs with scene-understanding requirements beyond OCR (reason about what the document means, not just what text it contains).
- **PP-OCRv5** — scale, cost, and latency: ranks #1 on 1-edit distance on OmniDocBench and beats bigger VLMs at a fraction of the compute.
- **Tesseract 5** — offline, zero-network, English-only Latin script.

## Why PaddleOCR-VL-1.5 is the default

Baidu's 2026 document-understanding model. 0.9B parameters (small for a VLM), trained specifically on document tasks. 111 languages. Handles PP-DocLayoutV3-flagged "tough scenarios": skew, warping, scanning artifacts, illumination variation, photos-of-screens. Adds Seal Recognition and Text Spotting.

Ships as a Hugging Face checkpoint: `PaddlePaddle/PaddleOCR-VL-1.5`. Integrates with vLLM for production serving.

## When to pick something else

- **You need offline, zero-network, low footprint** → Tesseract 5. Still the champ for "just works, no deps, English-Latin-scripts."
- **You need a specific key-value schema extracted (invoice number, amount, date)** → Donut (document understanding transformer) or LayoutLMv3. Requires fine-tuning on labeled documents.
- **Math / formulas** → pix2tex or Nougat for academic papers.
- **License plates, specific domain** → YOLO + a small classifier is often better than a general OCR.
- **Browser / JS-side** → Tesseract.js. Slow but runs client-side.
- **Indian scripts specifically** → PaddleOCR has reasonable Indic support; EasyOCR covers Devanagari decently; Bhashini (India's govt NLP platform) has dedicated models for regional scripts.

## The three questions to narrow

1. **Is the document clean or messy?** Clean → PaddleOCR/Tesseract. Messy → VLM.
2. **Do you need a schema extracted, or just raw text?** Raw → PaddleOCR. Schema → Donut/LayoutLM/VLM.
3. **Are you at scale (>100k pages/month)?** Yes → classical OCR (cost). No → VLM is fine.

## The Dump

### Classical OCR
- **Tesseract 5 (Google / open source)** — the grandfather of open-source OCR. Still viable for clean Latin-script text. Minimal deps.
- **PaddleOCR (Baidu)** — multilingual. PP-OCRv3, v4, v5 lineage.
- **PP-OCRv5 (Baidu, 2025)** — lightweight; ranks 1st on OmniDocBench by 1-edit-distance. Beats GOT-OCR-0.5B, RolmOCR-7B, Qwen2.5-VL-72B, InternVL3-78B, Gemini 2.5 Pro at a fraction of size.
- **EasyOCR** — Python-friendly wrapper around PyTorch OCR models. Easier to start with than PaddleOCR but accuracy is slightly behind.
- **MMOCR (OpenMMLab)** — research-friendly OCR framework. Use if you're training custom models.
- **TrOCR (Microsoft)** — transformer-based, strong on handwritten.

### Document-AI VLMs (the 2025–2026 wave)
- **PaddleOCR-VL-1.5 (Baidu, 2025–2026)** — 0.9B VLM, 94.5% OmniDocBench v1.5 SOTA. Current open document-parsing leader.
- **GOT-OCR 2.0 (0.5B)** — compact document VLM. Solid baseline.
- **DeepSeek-OCR 2** — 2026 entrant, competitive on OmniDocBench.
- **GLM-OCR** — Zhipu's OCR VLM, competitive in Chinese + multilingual.
- **RolmOCR (7B)** — larger VLM OCR entrant.

### Commercial APIs
- **Google Cloud Vision Text Detection** — the reference commercial OCR. Strong on most inputs.
- **AWS Textract** — specializes in forms + tables. Strong on clean documents.
- **Azure Document Intelligence** (formerly Form Recognizer) — closest competitor to Textract.
- **Mindee** — dev-friendly document API, good key-value extraction.

### Document understanding (OCR + layout)
- **Donut (Naver, 2022)** — no separate OCR step, directly trains image → structured output. Fine-tune on your docs.
- **LayoutLMv3 (Microsoft, 2022)** — pre-trained on document layouts; strong for form understanding.
- **Pix2Struct (Google, 2023)** — same family, different architecture.
- **Nougat (Meta, 2023)** — academic papers specifically.
- **Marker (VikParuchuri)** — PDF → markdown, uses a stack of OCR + layout models.

### VLM-based OCR (modern messy default)
- **GPT-4o / GPT-4-turbo-vision** — OpenAI. Strong on messy inputs. Expensive.
- **Gemini 2.5 Flash / Pro** — Google. Competitive with GPT-4, often cheaper.
- **Claude 3.5/4 Sonnet** — Anthropic. Strong, strict about factuality.
- **Qwen2-VL-72B** — strongest open VLM at this scale. Self-hostable.
- **InternVL2** — another open VLM competitor.

### Specialized
- **pix2tex / LaTeX-OCR** — math equations to LaTeX.
- **paddledetection + custom CRNN** — train your own if you have labeled data in a specific domain.
- **CRAFT** — text detection only, strong at finding text regions.

## Graveyard

- **OCR as a pure-CNN pipeline** — retired as transformers + end-to-end training became mainstream around 2021.
- **Tesseract 3/4 as a default** — use Tesseract 5 (LSTM engine) or something modern.
- **Proprietary ABBYY as the default open comparison** — no longer necessary; open options caught up.

## Last reviewed

2026-04-22.
