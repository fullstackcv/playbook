# Face Recognition

> The full stack: detect → align → embed → search. Plus anti-spoofing if you're doing anything customer-facing.

Face recognition is the most mature subtask in CV. The pipeline shape has been stable since 2015 (FaceNet) and the current defaults have been stable since 2019 (ArcFace). Which means: most of the 600 repos on GitHub are solving a solved problem, and the decision you actually need to make is *"which of the 3 picks for my constraint"* — not *"which of the 600."*

This page covers five sub-topics, each with its own picks table. Collapsed to one sentence each:

- **Detection:** SCRFD by default, Haar only on Pi-class hardware.
- **Alignment:** 5-point similarity transform. Never skip this.
- **Recognition:** ArcFace R100 default; AdaFace IR101 for surveillance; MobileFaceNet for edge.
- **Search:** numpy 1-NN below 50k vectors; FAISS at 50k–10M; pgvector if multi-tenant.
- **Anti-spoofing:** Silent-Face-Anti-Spoofing open-source; commercial (AWS Liveness, Face++) for production.

Scroll for the *why* on each.

---

## 1. Detection

**What it does:** find face bounding boxes in an image.

### Recommended picks

| Tier | Pick | Accuracy | FPS (CPU laptop) | When to use |
|------|------|---------:|-----------------:|-------------|
| Edge / dep-light | **Haar cascade** (OpenCV built-in) | ~75% on easy sets | 30 | Pi Zero / Pi 3, no ONNX, frontal faces only |
| **Default** | **SCRFD-500MF** | ~95% on WIDER Face | 15 | Anything with enough juice for ONNX Runtime |
| Max accuracy | **RetinaFace R50** | ~96% on WIDER Face | 3 | Offline / batch / GPU available |

### Why SCRFD is the default

InsightFace shipped SCRFD in 2021 as a distilled detector that matches RetinaFace's accuracy at 5× the speed. It runs via ONNX Runtime, which installs cleanly everywhere except the very low end. It ships as the default detector inside the InsightFace pipeline that the rest of your face stack (ArcFace, anti-spoof) already uses, so zero integration friction.

### When to pick something else

- **Pi Zero / Pi 3 or other ONNX-hostile hardware:** Haar. Zero dependencies beyond OpenCV. 20–30 FPS on small frames. Fails on side profiles; fine for kiosks.
- **Need landmarks and detection in one pass:** MTCNN. Slower than SCRFD but returns 5 landmarks free, saving a step if you're not using the InsightFace alignment chain.
- **Browser / webcam-only:** MediaPipe Face Detection. Runs in JS via TFLite WASM, no server required.
- **Absolute max accuracy for offline batch:** YOLOv8-Face or YOLOv11-Face. Slightly higher WIDER-hard numbers than SCRFD at 2–3× the parameters.

### The three questions to narrow

1. **Are you on hardware that can run ONNX Runtime?** If no → Haar. If yes → continue.
2. **Do you need real-time (>15 FPS)?** If no and you have GPU → RetinaFace. If yes → SCRFD.
3. **Are you in the browser?** If yes → MediaPipe. If no → SCRFD.

### The Dump

- **Viola-Jones / Haar cascade (2001)** — the classical cascade. Integral image + boosted weak classifiers. Still in OpenCV. Still runs on anything.
- **LBP cascade** — Local Binary Pattern variant of Viola-Jones. Slightly faster, slightly worse accuracy. Rarely worth choosing over Haar.
- **HOG + dlib (2005)** — Histogram of Oriented Gradients. CPU-only, ~15 FPS laptop, more robust to lighting than Haar. Dated but alive in legacy systems.
- **MTCNN (2016)** — 3-stage cascaded CNN. Returns 5 landmarks. Slower than SCRFD. Historically important.
- **SSD via OpenCV DNN (2015 SSD, 2018 weights)** — `cv2.dnn.readNetFromCaffe` with the ResNet-10 SSD weights. Ships with OpenCV. Legacy default for "DNN in OpenCV" tutorials.
- **RetinaFace (2019)** — anchor-based detector with landmark branch. Accuracy king. Slow on CPU.
- **SCRFD (2021)** — the current default. Ships multiple variants (500MF, 2.5G, 10G) at different speed/accuracy tradeoffs. Default: SCRFD-500MF or SCRFD-2.5G.
- **YuNet (2022)** — very fast, lightweight. Good for embedded. OpenCV ships it in `cv2.FaceDetectorYN`.
- **MediaPipe Face Detection (Google, ongoing)** — browser-friendly, TFLite-backed. ~30 FPS in JS.
- **YOLOv8-Face / YOLOv11-Face** — fine-tuned YOLO on face datasets. Marginally above SCRFD on hard sets at higher compute cost.
- **BlazeFace (Google, 2019)** — predecessor to MediaPipe's current face detector. On-device mobile.

### Graveyard

- **MTCNN as a default** — retired 2020. SCRFD replaced it for speed; the "free landmarks" advantage was outweighed by the speed gap.
- **Classical cascades (Haar/LBP) as general-purpose** — retired ~2018. Still valid on Pi-class hardware; not valid as a default on a laptop or phone.

### Last reviewed

2026-04-22.

---

## 2. Alignment

**What it does:** given a face bounding box + landmarks, warp the face into a canonical pose (eyes horizontal, fixed scale) before passing to the recognizer.

### Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Never | **No alignment** | Never. Costs you 10–20 points of recognition accuracy. Stop. |
| **Default** | **5-point similarity transform** (InsightFace convention) | Every face recognition system. 15 lines of numpy. |
| Overkill | **Dense 68-point elastic alignment (dlib)** | Academic / research. Not needed for recognition accuracy. |

Alignment is not really a "pick which model" question — the 5-point similarity transform is the industry default and works. The question is whether you do it at all. Many tutorials skip it and silently lose accuracy.

### Why alignment matters

A face at a 30° tilt has a different ArcFace embedding than the same face upright. The recognizer was trained on aligned faces — it expects eyes on a horizontal line at fixed positions. Feed it a non-aligned crop and recognition accuracy drops 10–20 percentage points.

The fix is a similarity transform (rotate + uniform scale + translate) that maps the detected 5 landmarks (left eye, right eye, nose tip, left and right mouth corners) to a fixed canonical position on a 112×112 crop. `cv2.estimateAffinePartial2D` + `cv2.warpAffine`. 15 lines.

### When to pick something else

Honestly, you don't. Use the 5-point similarity transform. The only exception: if your face cropper is already producing aligned outputs (some face SDKs do), don't double-align.

### The Dump

- **5-point similarity transform** — rotate + uniform scale + translate using 5 landmarks. The standard.
- **Affine transform (6-point)** — adds shear. Not needed; skew artifacts hurt recognition.
- **Perspective transform (4+ points)** — overkill for faces. Reserved for documents.
- **Dense 68-point alignment (dlib)** — uses every dlib landmark. More expensive, not more accurate for recognition. Useful for expression analysis, not recognition.
- **MediaPipe Face Mesh (468 points)** — different use case entirely (AR filters, 3D face reconstruction). Not for recognition alignment.

### Graveyard

- **3D alignment (Frontalization, ~2014)** — rotate the face to frontal using a 3D model. Outperformed by just doing 2D alignment + training the recognizer on varied poses.

### Last reviewed

2026-04-22.

---

## 3. Recognition (embedding)

**What it does:** given an aligned 112×112 face crop, produce a 512-dim vector such that same-person vectors are close and different-person vectors are far on a hypersphere.

### Recommended picks

| Tier | Pick | LFW accuracy | Surveillance accuracy | When to use |
|------|------|-------------:|----------------------:|-------------|
| Edge | **MobileFaceNet** | ~99.2% | ~87% | Raspberry Pi 4/5, phones, browser |
| **Default** | **ArcFace R100** (buffalo_l) | 99.83% | ~87% | Kiosks, attendance, identity verification — controlled input |
| Surveillance | **AdaFace IR101** | 99.82% | ~92% | CCTV, doorway, any low-quality or distant input |

### Why three picks, not one

Because LFW accuracy is saturated and doesn't predict real-world. ArcFace and AdaFace tie on LFW; AdaFace wins by 4–7 points on surveillance footage because its angular margin is *quality-adaptive* rather than fixed. If you pick based on LFW, you pick ArcFace. If you pick based on your actual deployment, you might pick AdaFace.

### ArcFace — the default

Published 2019 (Deng et al., InsightFace). The additive angular margin loss `cos(theta + m)` forces same-class angular clusters to be tight and between-class angles to be wide on a unit hypersphere. Became the production default within 18 months of publication and has not been displaced for clean-input tasks.

Install via `insightface` (pip). The `buffalo_l` model pack bundles SCRFD for detection + ArcFace R100 for recognition, pre-trained, ONNX-ready.

### AdaFace — surveillance default

Published 2022 (Kim et al.). Scales the angular margin per-sample based on the feature norm, which correlates with image quality. Low-quality inputs get a smaller effective margin, which prevents the network over-penalising ambiguous matches that are genuinely ambiguous. Matches ArcFace on clean data, significantly beats it on low-res / blurry / poorly-lit inputs.

If your deployment is a CCTV camera mounted above a door at 5 meters, this is your pick.

### MobileFaceNet — edge

Smaller backbone (~4M params vs ArcFace R100's ~65M). Trained with the same margin loss family. ~5× faster on CPU, ~1–2 percentage points lower accuracy on clean data. Ships inside InsightFace.

Pick this if you're on Raspberry Pi 4, a phone, or browser WASM.

### When to pick something else

- **You need a single Python library to try multiple recognizers:** use DeepFace (by Sefik Serengil). It wraps ArcFace, FaceNet, VGG-Face, DeepFace-original, SFace, all behind a unified API. Great for prototyping.
- **You already have FaceNet embeddings enrolled:** keep using FaceNet. Migrating means re-enrolling everyone (embeddings from different models aren't comparable). The accuracy gap over ArcFace on most deployments isn't worth the migration.
- **You need a magnitude-aware recognizer (MagFace):** edge case. MagFace encodes quality in the magnitude instead of using a quality-adaptive margin. Similar target as AdaFace; less widely deployed.

### The Dump

- **Eigenfaces (1991)** — PCA on face pixels. Historical only.
- **Fisherfaces (1997)** — LDA. Historical.
- **LBPH (2006)** — local binary pattern histograms. Still ships in `cv2.face.LBPHFaceRecognizer_create()`. Survives on embedded hardware that cannot run deep models.
- **DeepFace / Facebook (2014)** — first deep recognizer at human accuracy. Historical.
- **FaceNet (2015)** — triplet loss, 128-d embeddings. The one that made production face recognition real. Still usable; AdaFace/ArcFace both outperform it.
- **SphereFace (2017)** — first angular margin (multiplicative). Superseded by CosFace/ArcFace.
- **CosFace (2018)** — additive cosine margin. Cleaner math than SphereFace. Superseded by ArcFace.
- **ArcFace (2019)** — additive *angular* margin. The current default.
- **AdaFace (2022)** — quality-adaptive angular margin.
- **MagFace (2021)** — magnitude encodes quality. Alternative framing to AdaFace.
- **ElasticFace (2022)** — randomly sampled margin at training time. Marginal improvement over ArcFace.
- **TransFace (2023)** — ViT backbone with patch-level data augmentation and hard sample mining. 99.3%+ on clean benchmarks.
- **TopoFR (2024–2025)** — topology alignment + hard sample mining. Improves generalization vs ArcFace/AdaFace on OOD benchmarks.
- **LVFace (2025)** — Large Vision model for Face Recognition. ViT-based, simplified architecture.
- **SFace (2023)** — smaller backbone, safety-focused training. Mid-tier option.
- **InsightFace** (library) — the reference implementation. Bundles most of the above.
- **DeepFace** (library, by Sefik Serengil) — prototype-friendly multi-model wrapper.

### Graveyard

- **Eigenfaces / Fisherfaces as recognizers** — retired 1997 and 2014 respectively. LDA is still taught but nobody ships it.
- **FaceNet as a 2026 default** — retired when ArcFace's angular margin beat triplet loss on both accuracy and training stability.
- **VGG-Face** — retired. Interesting historical artifact, not competitive.

### Last reviewed

2026-04-22.

---

## 4. Search (identity matching)

**What it does:** given a new face embedding and a database of enrolled embeddings, return "who is this" or "unknown".

### Recommended picks

| Scale | Pick | When to use |
|-------|------|-------------|
| **< 50k enrolled vectors** | **numpy dot product + threshold** | Any product with fewer than ~50k enrolled identities. Don't over-engineer. |
| **50k – 10M** | **FAISS IndexFlatIP / HNSW** | Scale where numpy dot product gets slow. FAISS is free and fast. |
| **Multi-tenant / Postgres-first** | **pgvector** | Per-tenant isolation, or your stack already has Postgres. Slower than FAISS but operationally simpler. |

### Why not SVM

Because face recognition is **open-set**. The right answer for an unknown face is "unknown," not "the closest trained class."

Four reasons SVM is wrong for this:
1. SVM doesn't natively output "unknown." You can threshold the decision function, but you're fighting the tool.
2. Re-enrolling means retraining. Nearest-neighbor means appending a row.
3. ArcFace already does the margin work at training time. SVM's margin is redundant.
4. Scale is worse. 1-NN is O(N × 512) without index, O(log N × 512) with HNSW.

SVM *is* the right tool for closed-set binary classification (anti-spoofing, for instance). It is not right for identity.

### Why 1-NN + threshold specifically

Open-set recognition is: given a query embedding, find the nearest enrolled embedding, and return it only if the similarity exceeds a threshold. Otherwise, return "unknown."

The threshold is the single most important hyperparameter in a face recognition deployment. Too low → strangers match enrolled people. Too high → enrolled people get missed.

Typical thresholds on cosine similarity: **0.60** for ArcFace, **0.55** for AdaFace. Tune for *your* camera + lighting + subject distribution. Don't copy numbers.

### When to pick something else

- **Billion-scale:** FAISS with IVF + PQ, or dedicated vector DBs (Milvus, Weaviate). You're outside face recognition territory at this point; you're in generic ANN.
- **You want zero infrastructure:** SQLite with embeddings as BLOBs + numpy for search. Ugly but works to ~10k vectors.

### The Dump

- **numpy dot product** — `reference_embeddings @ query_embedding`. Vectorized. Sub-millisecond at 10k vectors, ~10ms at 100k. The default until it gets slow.
- **FAISS IndexFlatIP** — same math as numpy, different storage. Persistence + slightly faster at scale.
- **FAISS HNSW** — Hierarchical Navigable Small World graph. Approximate nearest-neighbor. Sub-millisecond at 10M vectors.
- **FAISS IVF + PQ** — inverted file + product quantization. Billion-scale at some accuracy cost.
- **pgvector** — Postgres extension. SQL-native. Slower than FAISS per query; much simpler operationally.
- **Pinecone / Weaviate / Milvus / Qdrant** — managed or self-hosted vector DBs. Overkill for most face recognition unless you're multi-tenant at scale.
- **SQLite + BLOBs + numpy** — the "zero infrastructure" option.
- **Annoy (Spotify)** — older tree-based ANN. Largely displaced by HNSW.

### Graveyard

- **SVM for identity** — never right. Use 1-NN.
- **Siamese network classifiers as the final step** — the margin loss at training time removes the need.

### Last reviewed

2026-04-22.

---

## 5. Anti-spoofing (liveness)

**What it does:** tell whether the face in front of the camera is a real person or a photo/video/mask.

### Recommended picks

| Tier | Pick | When to use |
|------|------|-------------|
| Open-source | **Silent-Face-Anti-Spoofing (MiniVision)** | Open-source project, good enough for low-stakes product demos |
| **Managed (default for prod)** | **AWS Rekognition Liveness** or **Face++ Liveness** | Customer-facing auth, KYC, bank-grade |
| Research | **CelebA-Spoof-trained models, or Face Anti-Spoofing Challenge submissions** | When you need to train your own |

### Why a managed service is the production default

Anti-spoofing has an attacker. The attacker will iterate against your model. Open-source anti-spoofing models are publicly known — attackers train against them. Managed services rotate their models, have challenge-response systems (blink, move head), and have orders of magnitude more training data than you'll ever have.

For anything customer-facing where being spoofed has cost (KYC, building access, banking), use a managed service. For demos and internal tooling, open-source is fine.

### When to pick something else

- **On-device, no network:** use the open-source model. Accept the weaker security.
- **Multi-modal sensors available (depth, IR):** use the sensor. A TrueDepth camera on iPhone beats any RGB-only anti-spoof. Apple's Face ID is this.

### The Dump

- **Silent-Face-Anti-Spoofing (MiniVision)** — public model, RGB-only, works for printed photo + screen replay attacks. Pretrained weights on GitHub.
- **CelebA-Spoof** — dataset + baseline model. Good for training custom anti-spoofs.
- **MiniFASNet** — lightweight anti-spoof net, mobile-friendly.
- **AWS Rekognition Liveness** — challenge-response + managed model. 2–3 seconds of user action required. Integrates with face verification.
- **Face++ Liveness Detection** — similar; better in some Asian markets.
- **IDnow / Onfido / Jumio** — identity verification stacks. Anti-spoofing is one component of a KYC pipeline.
- **FaceTec ZoOm** — claims iBeta Level 2 compliance. Used in fintech.
- **Apple FaceID / Face ID-equivalent systems** — hardware-based (structured light / IR). Not something you deploy yourself.

### Graveyard

- **Blink detection as the entire anti-spoof** — trivially defeated by video replay. Historical.
- **Texture analysis (LBP on face) as a standalone** — defeated by high-res screens.

### Last reviewed

2026-04-22.

---

## Libraries that pull multiple sub-topics together

- **InsightFace** — the reference implementation of the default stack. SCRFD + ArcFace + landmarks + anti-spoof-ish. Open-source, actively maintained, ONNX-ready. If you're starting a face project in 2026, install `insightface`.
- **DeepFace (Sefik Serengil)** — Python wrapper around many detector/recognizer combinations. Good for prototype experiments ("what does FaceNet give me vs ArcFace?"). Not the production library.
- **face_recognition (Adam Geitgey)** — dlib-based, historically popular, mostly unmaintained. Uses HOG + dlib face encodings. Not competitive with InsightFace for 2026 work.
- **CompreFace** — self-hostable API server with enrollment and recognition endpoints. Based on InsightFace under the hood.
- **facenet-pytorch** — if you specifically need PyTorch FaceNet. Niche now.

---

*Last reviewed: 2026-04-22. Written by Vikas Gupta.*
