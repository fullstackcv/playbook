# OCR / Document AI

> Extracting text from images. In 2026 this subtask is bifurcating fast: classical OCR still wins on clean printed pages at scale, but VLMs have eaten most of the messy real-world work.

The field has three distinct use cases with different picks. Don't pick one tool and use it for all three.

## Recommended picks

| Use case | Pick | When to use |
|----------|------|-------------|
| Messy real-world (receipts, handwriting, weird layouts) | **A VLM (Gemini 2.5, GPT-4o, Claude, Qwen2-VL)** | When documents don't fit a rigid template. Expensive per page but high accuracy. |
| **Clean printed documents at scale** | **PaddleOCR** | Invoices, forms, PDFs you control. Free, multi-language, good layout support. |
| English-only + local + fast | **Tesseract 5** | Zero-dependency batch processing of clean text. |
| Structured document understanding | **Donut** or **LayoutLMv3** | Form key-value extraction with a defined schema. Training-required. |

## The big shift

Until 2023, OCR meant Tesseract/PaddleOCR for clean, or a dedicated pipeline (Donut, LayoutLM) for forms. The work was running the model; the hard part was post-processing bad recognitions.

Since 2024, vision-language models (GPT-4V, Gemini, Claude, Qwen-VL) do "give me the text from this image" as well as or better than classical OCR on messy inputs. For scanned receipts with faded ink, photographed whiteboards, handwritten notes, weird rotated layouts — a VLM wins. It's also more expensive per page and has no on-device option at reasonable quality.

So: use classical OCR for scale and clean inputs; use VLMs for messy and complex; know where the line is.

## Why PaddleOCR is the default classical

Baidu's OCR. Two-stage (detection + recognition) with strong multilingual support (100+ languages, real support for Chinese / Arabic / Indic / Thai). Fast, open source, well-maintained. `paddleocr` in pip.

Ships a structure-understanding model (PP-StructureV2) that handles tables and layouts, which is rare in open-source OCR.

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
- **PaddleOCR (Baidu)** — multilingual, strong, the current default.
- **EasyOCR** — Python-friendly wrapper around PyTorch OCR models. Easier to start with than PaddleOCR but accuracy is slightly behind.
- **MMOCR (OpenMMLab)** — research-friendly OCR framework. Use if you're training custom models.
- **TrOCR (Microsoft)** — transformer-based, strong on handwritten.

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
