# Cloud Vision APIs

> Managed services for common CV tasks. Useful when you don't want to operate models yourself, accept per-request cost, and trust a vendor.

Cloud vision has bifurcated in 2026 into two worlds: **task-specific APIs** (detect faces, read text, label scenes) that charge per-request at low unit cost, and **VLM APIs** (send an image + a prompt, get unstructured output) that cost more but do almost anything. For many use cases, a VLM API has replaced the specialized one.

## Recommended picks

| Use case | Pick | When to use |
|----------|------|-------------|
| **General "what's in this image"** | **Gemini 2.5 Flash**, **GPT-4o**, or **Claude Sonnet** (a VLM) | Anything that doesn't fit a rigid template. |
| Face rec at scale | **AWS Rekognition** or **Face++** | Pre-enrolled identity matching, large volumes, regulatory compliance. |
| OCR at scale | **Google Cloud Vision Text** or **AWS Textract** | Structured invoice/form extraction at volume. |
| Content moderation | **AWS Rekognition Content Moderation**, **Hive**, **Sightengine** | Explicit content detection, structured label output. |
| Live video analysis | **AWS Rekognition Video** or **Azure Video Indexer** | Large-scale video with indexing/search needs. |

## The VLM-ate-the-cloud-API shift

Gemini/GPT-4o/Claude can now:
- Describe an image in detail.
- Extract structured JSON from an image given a schema.
- Read handwritten text.
- Identify known objects (within their training data).
- Detect faces (not for identity — just presence).
- Moderate content (sometimes, with post-filtering).

This doesn't kill task-specific APIs. It does mean: **if you're prototyping and volume is low, start with a VLM API; migrate to task-specific APIs only when cost justifies it.**

Rough cost comparison (2026 pricing, varies):
- VLM API flagship: ~$0.005–0.02 per image.
- VLM API budget (Flash-class): ~$0.0005–0.002 per image.
- AWS Rekognition label detection: ~$0.001 per image.
- Google Cloud Vision label detection: ~$0.0015 per image.

For low/medium volume (< 10K images/day), VLM APIs are competitive. At 1M+ images/day, task-specific APIs win on cost.

## Task-specific API stacks

### AWS Rekognition
- **Label detection** — general "what's in this image."
- **Face detection + analysis** — emotion, age, glasses. Not identity.
- **Face comparison / Search** — enrolled identity matching.
- **Face Liveness** — challenge-response anti-spoofing. Strong.
- **Content moderation** — explicit content.
- **Text detection** — basic OCR.
- **PPE detection** — purpose-built for safety gear.
- **Celebrity recognition** — pre-enrolled famous-person identification.
- **Rekognition Video** — same tasks for video streams.

### Google Cloud Vision
- **Label detection** — general tagging.
- **Text detection / Document text detection** — OCR, strong.
- **Object localization** — detection.
- **Face detection** — bounding boxes + landmarks. Not identity (Google doesn't offer identity).
- **Web detection** — "where does this image appear online." Unique.
- **Safe search** — content moderation.
- **Cloud Vision AutoML** — custom classifier/detector training.
- **Document AI** — structured extraction (invoices, forms). Stronger than base Vision.

### Azure Computer Vision / Azure AI Vision
- **Image Analysis 4.0** — labels, tags, descriptions. The **Florence foundation model integration (2025)** significantly improved caption quality and natural-language image queries; tends to beat Google/AWS on those specific axes.
- **Spatial Analysis** — people-counting, movement tracking, occupancy for physical spaces. Unique to Azure among the three; Google and AWS don't offer the equivalent.
- **Read / OCR** — document text.
- **Face API** — detection, analysis, identity. *Microsoft restricted Face identity access to approved customers in 2022.*
- **Custom Vision** — custom classifier/detector training.
- **Azure Document Intelligence** — structured doc extraction.
- **Azure Video Indexer** — video analysis with search.

### Other task-specific
- **Face++ / Megvii** — Chinese market. Strong face rec. Cheaper than AWS/Azure in Asia.
- **Clarifai** — Custom model hosting + pre-built APIs.
- **Amazon Textract** — specialized on forms/tables, beats base Vision for structured docs.
- **OpenAI Moderation API** — text + image content moderation (text stronger than image).
- **Hive** — content moderation specialist. NSFW, violence, etc.
- **Sightengine** — content moderation, general CV API.

## When to pick something else

- **Regulated data (healthcare, government)** → on-prem / self-hosted. Don't send patient data to commercial APIs without BAA/contract review.
- **Identity verification with KYC compliance** → specialized providers (Jumio, Onfido, Persona, IDnow). Not general cloud APIs; they handle the full KYC flow.
- **Very high volume with a narrow task** → self-host YOLO or similar. Break-even is somewhere around 10M+ images/month depending on task.
- **Latency below 100ms round-trip** → edge / self-hosted. Cloud round-trip eats your latency budget.

## The three questions to narrow

1. **Volume?** < 10K/day → VLM API. 10K–1M → task API. 1M+ → consider self-hosting.
2. **Data sensitivity?** Regulated → self-host or vendor-with-BAA. Public → any.
3. **Task specificity?** Rigid (invoice fields) → Textract/Document AI. Flexible (describe this) → VLM API.

## The Dump

### AWS
- **Rekognition** (image + video, face, label, liveness, moderation, PPE, celebrity).
- **Textract** (forms + tables + handwriting).
- **Comprehend** (text, not CV, but often chained).
- **SageMaker** (if you train your own).

### Google Cloud
- **Cloud Vision API** (labels, text, objects, landmarks, faces, web detection, safe search).
- **Document AI** (structured extraction).
- **Vertex AI** (custom model training/deployment).
- **Video Intelligence** (video analysis).

### Azure
- **Azure AI Vision** (image analysis, OCR/Read, face — restricted).
- **Document Intelligence** (forms).
- **Video Indexer** (video).
- **Custom Vision** (AutoML).

### Anthropic / OpenAI / Google AI (VLM APIs)
- **Claude 4 Sonnet / Opus / Haiku** (Anthropic).
- **GPT-5 / GPT-4o / GPT-4o-mini** (OpenAI).
- **Gemini 2.5 Pro / Flash** (Google AI Studio / Vertex).

### Specialized / regional
- **Face++ (Megvii)** — face identity, especially in China.
- **Baidu AI Open Platform** — Chinese market.
- **Yandex Vision** — Russian market.
- **Kakao Vision / Naver Clova** — Korean market.

### Content moderation specialists
- **Hive** — ML-based moderation.
- **Sightengine** — images + video.
- **Amazon Rekognition Content Moderation** — AWS-native.
- **Microsoft Content Moderator** — deprecated in 2024, replaced by Azure AI Content Safety.

### KYC / Identity verification (chain includes face rec)
- **Jumio** — full KYC stack.
- **Onfido** — full KYC stack.
- **Persona** — developer-friendly KYC.
- **IDnow** — European market.
- **Veriff** — European-focused.
- **Socure** — US-focused.

### Other
- **Clarifai** — model hub + APIs.
- **Mindee** — document AI API, dev-friendly.
- **Nanonets** — document AI + OCR + data extraction.

## Graveyard

- **Microsoft Face API (for general identity)** — restricted in 2022. Still works for existing customers in approved use cases.
- **Cognitive Services Custom Vision as a leader** — eclipsed by SageMaker / Vertex for custom model training.
- **AWS DeepLens** — AWS's edge hardware, discontinued.
- **Google Cloud AutoML Vision** — subsumed into Vertex AI.

## Last reviewed

2026-04-22.
