# Face Recognition

> The full stack: detect → align → embed → search. Plus anti-spoofing if you're doing anything customer-facing.

Face recognition is the most mature subtask in CV. The pipeline shape has been stable since 2015 (FaceNet) and the current defaults have been stable since 2019 (ArcFace). Which means: most of the 600 repos on GitHub are solving a solved problem, and the decision you actually need to make is *"which of the 3 picks for my constraint"* — not *"which of the 600."*

This page covers five sub-topics, each with its own picks table. Collapsed to one sentence each:

- **Detection:** commercial-safe → **YuNet** default, MediaPipe for browser, Haar on Pi-class. Research / internal → SCRFD.
- **Alignment:** 5-point similarity transform. In most pipelines, don't skip this.
- **Recognition:** no open-weights pick has both a commercial license *and* ArcFace-class accuracy. Commercial → managed service (AWS Rekognition / Face++) or **dlib ResNet** (weaker). Research / internal → ArcFace R100 default, AdaFace IR101 surveillance, MobileFaceNet edge.
- **Search:** numpy 1-NN below 50k vectors; FAISS at 50k–10M; pgvector if multi-tenant.
- **Anti-spoofing:** Silent-Face-Anti-Spoofing open-source; commercial (AWS Liveness, Face++) for production.

Scroll for the *why* on each.

> [!WARNING]
> **License matters more than benchmarks in face recognition.** The strongest open face-rec weights — InsightFace's SCRFD / ArcFace R100 / MobileFaceNet, AdaFace pretrained, and most "SOTA on LFW" models you'll find on GitHub — are **non-commercial research use only**. The code is MIT; the *weights* are not. They were trained on datasets like MS1MV2, Glint360K, and WebFace260M whose licenses forbid commercial use.
>
> If you're shipping a product, **don't use those weights**. Use the commercial-safe picks below, pay for a managed service, or train your own on commercially-licensed data. Each picks table in Detection and Recognition below is split into a **commercial-safe** stack (ship this) and an **open-research** stack (higher accuracy, non-commercial use only).

---

## 1. Detection

**What it does:** find face bounding boxes in an image.

### Recommended picks — commercial-safe (ship this)

| Tier | Pick | License | When to use |
|------|------|---------|-------------|
| Edge / dep-light | **[Haar cascade](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)** (OpenCV built-in) | BSD (OpenCV) | Pi Zero / Pi 3, no ONNX, frontal faces only |
| **Default** | **[YuNet](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)** (OpenCV Zoo) | Apache-2.0 | Laptop/server CPU, 30+ FPS on small frames, commercial ship. |
| Browser / mobile | **[MediaPipe Face Detection](https://github.com/google-ai-edge/mediapipe)** | Apache-2.0 | JS/WASM or iOS/Android, no server. |
| Landmarks in one pass | **[MTCNN](https://github.com/kpzhang93/MTCNN_face_detection_alignment)** | MIT (original) | Returns 5 landmarks free; slower than YuNet. |

### Recommended picks — open-research stack (non-commercial)

| Tier | Pick | Training license | Accuracy |
|------|------|------------------|----------|
| **Default (research/internal)** | **[SCRFD-500MF](https://github.com/deepinsight/insightface/tree/master/detection/scrfd)** | InsightFace non-commercial | Strong on WIDER Face |
| Max accuracy | **[RetinaFace R50](https://github.com/deepinsight/insightface/tree/master/detection/retinaface)** | InsightFace non-commercial | Slightly stronger than SCRFD |

*Accuracy and FPS numbers vary by backbone, input resolution, and hardware; treat the above as rough ordering rather than exact figures. Benchmark against your own pipeline before committing.*

### Why YuNet is the commercial-safe default

YuNet ships in the [OpenCV Zoo](https://github.com/opencv/opencv_zoo) under Apache-2.0 — weights and code. ~100 KB model, ~30 FPS on a modern laptop CPU at 320×320, ~AP 0.87 on WIDER Face Easy. Accuracy is below SCRFD-500MF on WIDER Hard, but it's the strongest **commercial-safe** detector you can ship today without license exposure. Drop-in via `cv2.FaceDetectorYN_create()`.

### Why SCRFD wins on accuracy (research / internal only)

InsightFace shipped SCRFD in 2021 as a distilled detector that matches RetinaFace's accuracy at ~5× the speed. **The weights are non-commercial research use only** — trained on data whose license forbids commercial deployment. Use it for research, academic evaluation, or internal non-product work. For a shipping product, go with YuNet (or train your own SCRFD on commercially-licensed data).

### When to pick something else

- **Pi Zero / Pi 3 or other ONNX-hostile hardware:** Haar. Zero dependencies beyond OpenCV. 20–30 FPS on small frames. Fails on side profiles; fine for kiosks.
- **Need landmarks and detection in one pass:** MTCNN. Slower than YuNet/SCRFD but returns 5 landmarks free.
- **Browser / webcam-only:** MediaPipe Face Detection. Runs in JS via TFLite WASM, no server required.
- **Max accuracy offline batch, license permitting:** RetinaFace R50 or SCRFD-10G (non-commercial). For commercial batch, train your own.
- **YOLOv8-Face / YOLOv11-Face:** strong accuracy, but **AGPL-3.0** via Ultralytics — commercial use requires an Ultralytics enterprise license. Not commercial-safe by default.

### The three questions to narrow

1. **Is this going into a commercial product?** Yes → commercial-safe picks (YuNet / MediaPipe / Haar / MTCNN). No → SCRFD / RetinaFace fine.
2. **Are you on hardware that can run ONNX Runtime?** If no → Haar. If yes → continue.
3. **Are you in the browser?** If yes → MediaPipe. If no → YuNet (commercial) or SCRFD (research).

### The Dump

- **[Viola-Jones / Haar cascade (2001)](https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf)** — the classical cascade. Integral image + boosted weak classifiers. Still in OpenCV. Still runs on anything.
- **[LBP cascade](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)** — Local Binary Pattern variant of Viola-Jones. Slightly faster, slightly worse accuracy. Rarely worth choosing over Haar.
- **[HOG + dlib (2005)](http://dlib.net/)** — Histogram of Oriented Gradients. CPU-only, ~15 FPS laptop, more robust to lighting than Haar. Dated but alive in legacy systems.
- **[MTCNN (2016)](https://github.com/kpzhang93/MTCNN_face_detection_alignment)** — 3-stage cascaded CNN. Returns 5 landmarks. Slower than SCRFD. Historically important.
- **[SSD via OpenCV DNN (2015 SSD, 2018 weights)](https://docs.opencv.org/4.x/d6/d0f/group__dnn.html)** — `cv2.dnn.readNetFromCaffe` with the ResNet-10 SSD weights. Ships with OpenCV. Legacy default for "DNN in OpenCV" tutorials.
- **[RetinaFace (2019)](https://github.com/deepinsight/insightface/tree/master/detection/retinaface)** — anchor-based detector with landmark branch. Accuracy king. Slow on CPU.
- **[SCRFD (2021)](https://github.com/deepinsight/insightface/tree/master/detection/scrfd)** — the current default. Ships multiple variants (500MF, 2.5G, 10G) at different speed/accuracy tradeoffs. Default: SCRFD-500MF or SCRFD-2.5G.
- **[YuNet (2022)](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)** — very fast, lightweight. Good for embedded. OpenCV ships it in `cv2.FaceDetectorYN`.
- **[MediaPipe Face Detection (Google, ongoing)](https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector)** — browser-friendly, TFLite-backed. ~30 FPS in JS.
- **[YOLOv8-Face / YOLOv11-Face](https://github.com/derronqi/yolov8-face)** — fine-tuned YOLO on face datasets. Marginally above SCRFD on hard sets at higher compute cost.
- **[BlazeFace (Google, 2019)](https://github.com/hollance/BlazeFace-PyTorch)** — predecessor to MediaPipe's current face detector. On-device mobile.

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
| Don't skip | **No alignment** | Only acceptable if your detector already produces canonicalised crops. Otherwise typically a meaningful accuracy loss. |
| **Default** | **5-point similarity transform** (InsightFace convention) | Standard for most face recognition systems. ~15 lines of numpy. |
| Overkill | **[Dense 68-point elastic alignment (dlib)](http://dlib.net/face_landmark_detection.py.html)** | Academic / research. Not typically needed for recognition accuracy. |

Alignment is not really a "pick which model" question — the 5-point similarity transform is the common industry default. The practical question is whether to do it at all. Skipping it is a frequent mistake in tutorial code and usually costs noticeable accuracy in production.

### Why alignment matters

A face at a 30° tilt has a different ArcFace embedding than the same face upright. The recognizer was trained on aligned faces — it expects eyes on a horizontal line at fixed positions. Feed it a non-aligned crop and recognition accuracy typically drops meaningfully (exact degradation varies with the backbone, input distribution, and pose range; rule of thumb: it's large enough that skipping alignment usually isn't worth it).

The fix is a similarity transform (rotate + uniform scale + translate) that maps the detected 5 landmarks (left eye, right eye, nose tip, left and right mouth corners) to a fixed canonical position on a 112×112 crop. `cv2.estimateAffinePartial2D` + `cv2.warpAffine`. 15 lines.

### When to pick something else

Honestly, you don't. Use the 5-point similarity transform. The only exception: if your face cropper is already producing aligned outputs (some face SDKs do), don't double-align.

### The Dump

- **5-point similarity transform** — rotate + uniform scale + translate using 5 landmarks. The standard.
- **Affine transform (6-point)** — adds shear. Not needed; skew artifacts hurt recognition.
- **Perspective transform (4+ points)** — overkill for faces. Reserved for documents.
- **[Dense 68-point alignment (dlib)](http://dlib.net/face_landmark_detection.py.html)** — uses every dlib landmark. More expensive, not more accurate for recognition. Useful for expression analysis, not recognition.
- **[MediaPipe Face Mesh (468 points)](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker)** — different use case entirely (AR filters, 3D face reconstruction). Not for recognition alignment.

### Graveyard

- **3D alignment (Frontalization, ~2014)** — rotate the face to frontal using a 3D model. Outperformed by just doing 2D alignment + training the recognizer on varied poses.

### Last reviewed

2026-04-22.

---

## 3. Recognition (embedding)

**What it does:** given an aligned 112×112 face crop, produce a 512-dim vector such that same-person vectors are close and different-person vectors are far on a hypersphere.

### The license reality

**There is no open-source face recognizer with both a commercial license *and* ArcFace-class accuracy.** This is not an oversight on the playbook's part — it's a real constraint in the industry. Every strong open recognizer you'll find on GitHub (ArcFace, AdaFace, MobileFaceNet via InsightFace; MagFace; ElasticFace; TransFace) was trained on a dataset — MS1MV2, Glint360K, WebFace260M, MS-Celeb-1M — whose license forbids commercial use. The architectures are published; the *weights that make them accurate* are locked behind research licenses.

Your commercial options are genuinely limited:

### Recommended picks — commercial-safe (ship this)

| Tier | Pick | License | Accuracy | Cost |
|------|------|---------|----------|------|
| **Open weights (easy)** | **[face_recognition](https://github.com/ageitgey/face_recognition) (dlib ResNet)** | Boost/MIT | ~99.38% LFW (paper). Notably weaker on surveillance / hard pose. | Free |
| **Managed (default for product)** | **[AWS Rekognition](https://aws.amazon.com/rekognition/)** / **[Face++](https://www.faceplusplus.com/)** / **[GCP Face](https://cloud.google.com/vision/docs/face-tutorial)** | Commercial T&C | Production-grade; vendor-managed | Per-call (~$0.001/face) |
| **DIY (hard)** | Train MobileFaceNet / ArcFace architecture yourself | Your code | Tunable | Weeks + a commercially-licensed dataset you curate |

### Recommended picks — open-research stack (non-commercial)

| Tier | Pick | Training license | LFW | Surveillance |
|------|------|------------------|----:|-------------:|
| Edge | **[MobileFaceNet](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch)** | InsightFace non-commercial | ~99% | moderate |
| **Default** | **[ArcFace R100](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch)** (buffalo_l) | InsightFace non-commercial | ~99.8% | moderate |
| Surveillance | **[AdaFace IR101](https://github.com/mk-minchul/AdaFace)** | Non-commercial (trained on WebFace4M) | ~99.8% | Stronger than ArcFace |

*LFW numbers are saturated and come from the respective papers; they don't predict real-world performance on your data. The "Surveillance" column is a qualitative ordering, not a benchmarked number — measure against your own footage before committing.*

### dlib face_recognition — the commercial-safe default

Adam Geitgey's [`face_recognition`](https://github.com/ageitgey/face_recognition) library wraps [dlib](http://dlib.net/)'s ResNet-34 face embedding model. License is clean: Boost Software License for dlib, MIT for the Python wrapper. ~99.38% on LFW (dlib's published number) — **not** ArcFace-class, and it degrades faster than ArcFace on pose / occlusion / low-quality inputs.

Accept the gap if you're shipping commercial and can't pay for a managed service. Don't use it for high-security applications (surveillance identification, doorway access control at scale) — accept a managed-service baseline there instead.

### When a managed service is the right answer

For most commercial face recognition products in 2026, **a managed service is the honest production default**. AWS Rekognition, Face++, and GCP Face API all:

- Handle the license problem for you (it's their training data, their lawyers' problem).
- Ship vendor-audited accuracy (often ArcFace-class or better on clean input).
- Rotate models without you re-enrolling (they maintain a stable embedding-space contract).
- Include anti-spoofing and bias monitoring as part of the product.

Pricing is roughly $0.001–0.002 per face at volume — at 1M faces/month, that's $1–2K. Often cheaper than the engineer time to curate a commercial dataset, train, evaluate, and maintain a recognizer yourself.

### ArcFace / AdaFace / MobileFaceNet — research and internal only

For research, academic evaluation, or internal non-product work (e.g., organizing your own photo library, evaluating a benchmark, prototyping before production), the InsightFace stack is the strongest open option and the rest of this section still applies.

**ArcFace R100.** Published 2019 (Deng et al., InsightFace). The additive angular margin loss `cos(theta + m)` forces same-class angular clusters to be tight and between-class angles to be wide on a unit hypersphere. Install via `insightface` (pip). The `buffalo_l` model pack bundles SCRFD for detection + ArcFace R100 for recognition, pre-trained, ONNX-ready. *Non-commercial research use only.*

**AdaFace IR101.** Published 2022 (Kim et al.). Scales the angular margin per-sample based on the feature norm, which correlates with image quality. Matches ArcFace on clean data, significantly beats it on low-res / blurry / poorly-lit inputs — the pick for surveillance research. *Non-commercial research use only.*

**MobileFaceNet.** Smaller backbone (~4M params vs ArcFace R100's ~65M). ~5× faster on CPU, ~1–2 percentage points lower accuracy on clean data. *Non-commercial research use only.*

### When to pick something else

- **Single Python library to try multiple recognizers:** [DeepFace](https://github.com/serengil/deepface) (by Sefik Serengil). Wraps ArcFace, FaceNet, VGG-Face, SFace, Dlib. Convenient for prototyping — but license varies per backbone; check before shipping.
- **Existing FaceNet embeddings enrolled:** keep FaceNet. Migrating means re-enrolling everyone.
- **Magnitude-aware (MagFace):** also non-commercial. Same dataset problem.
- **Willing to train from scratch on commercially-licensed data:** CelebA (CC BY-NC-SA, *still non-commercial*), CASIA-WebFace (research only), VGGFace2 (non-commercial) — almost every academic face dataset is research-only. You'd likely need to scrape/license your own data, which is a legal project in itself.

### The Dump

*Assume every entry's **pretrained weights** below are **non-commercial research use only** unless noted otherwise. The architectures and loss functions are published; the weights are trained on research-license datasets.*

- **Eigenfaces (1991)** — PCA on face pixels. Historical only. (Commercial-OK if you implement yourself.)
- **Fisherfaces (1997)** — LDA. Historical. (Commercial-OK if you implement yourself.)
- **LBPH (2006)** — local binary pattern histograms. Still ships in `cv2.face.LBPHFaceRecognizer_create()`. Survives on embedded hardware that cannot run deep models. **Apache-2.0 via OpenCV — commercial OK.**
- **[dlib ResNet-34 (2017)](http://dlib.net/)** — the model behind `face_recognition`. ~99.38% LFW. **Boost Software License — commercial OK.**
- **[DeepFace / Facebook (2014)](https://research.facebook.com/publications/deepface-closing-the-gap-to-human-level-performance-in-face-verification/)** — first deep recognizer at human accuracy. Historical.
- **[FaceNet (2015)](https://github.com/davidsandberg/facenet)** — triplet loss, 128-d embeddings. The one that made production face recognition real. Still usable; AdaFace/ArcFace both outperform it.
- **[SphereFace (2017)](https://github.com/wy1iu/sphereface)** — first angular margin (multiplicative). Superseded by CosFace/ArcFace.
- **[CosFace (2018)](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch)** — additive cosine margin. Cleaner math than SphereFace. Superseded by ArcFace.
- **[ArcFace (2019)](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch)** — additive *angular* margin. The current research default.
- **[AdaFace (2022)](https://github.com/mk-minchul/AdaFace)** — quality-adaptive angular margin.
- **[MagFace (2021)](https://github.com/IrvingMeng/MagFace)** — magnitude encodes quality. Alternative framing to AdaFace.
- **[ElasticFace (2022)](https://github.com/fdbtrs/ElasticFace)** — randomly sampled margin at training time. Marginal improvement over ArcFace.
- **[TransFace (2023)](https://github.com/DanJun6737/TransFace)** — ViT backbone with patch-level data augmentation and hard sample mining. 99.3%+ on clean benchmarks.
- **TopoFR (2024–2025)** — topology alignment + hard sample mining. Improves generalization vs ArcFace/AdaFace on OOD benchmarks.
- **LVFace (2025)** — Large Vision model for Face Recognition. ViT-based, simplified architecture.
- **[SFace (2023)](https://github.com/zhongyy/SFace)** — smaller backbone, safety-focused training. Mid-tier option.
- **[InsightFace](https://github.com/deepinsight/insightface)** (library) — MIT-licensed code; *the pretrained weights it distributes are non-commercial.*
- **[DeepFace](https://github.com/serengil/deepface)** (library, by Sefik Serengil) — MIT-licensed code; the wrapped *backbones* carry their own (mostly non-commercial) license.

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
| **Small-scale (roughly sub-50K vectors)** | **[numpy](https://numpy.org/) dot product + threshold** | Most products with a modest enrolment count. Don't over-engineer. |
| **Medium-to-large scale** | **[FAISS](https://github.com/facebookresearch/faiss) IndexFlatIP / HNSW** | When numpy dot product gets slow. FAISS is free and fast. |
| **Multi-tenant / Postgres-first** | **[pgvector](https://github.com/pgvector/pgvector)** | Per-tenant isolation, or your stack already runs Postgres. Slower than FAISS per query but operationally simpler. |

The exact crossover between numpy / FAISS / pgvector depends on your latency target, tenanting model, and infra. The scale ranges above are rough guides, not hard thresholds.

### Why 1-NN + threshold, not SVM

Because face recognition is **open-set**. The right answer for an unknown face is "unknown," not "the closest trained class." For open-set identity search, 1-NN + threshold is usually the cleaner default than SVM.

Four reasons it's the better default for this problem:

1. **"Unknown" handling is natural.** SVM doesn't output "unknown" by default — you can threshold the decision function, but you're working against the tool instead of with it.
2. **Re-enrollment is cheap.** Adding a person = appending a row. With SVM you retrain.
3. **The margin is already in the embedding.** ArcFace's angular margin is applied at training time; adding SVM's margin on top is redundant.
4. **Scale tends to be better.** 1-NN is O(N × D) brute, O(log N × D) with HNSW. SVM prediction is O(#support vectors × features), which can be worse above ~10K classes.

SVM *is* a good fit for closed-set binary classification (anti-spoofing, for example) where the class set is fixed and small. For open-set identity search with a growing enrolment database, nearest-neighbor is usually the better default.

### Why 1-NN + threshold specifically

Open-set recognition is: given a query embedding, find the nearest enrolled embedding, and return it only if the similarity exceeds a threshold. Otherwise, return "unknown."

The threshold is the single most important hyperparameter in a face recognition deployment. Too low → strangers match enrolled people. Too high → enrolled people get missed.

Typical thresholds on cosine similarity: **0.60** for ArcFace, **0.55** for AdaFace. Tune for *your* camera + lighting + subject distribution. Don't copy numbers.

### When to pick something else

- **Billion-scale:** FAISS with IVF + PQ, or dedicated vector DBs (Milvus, Weaviate). You're outside face recognition territory at this point; you're in generic ANN.
- **You want zero infrastructure:** SQLite with embeddings as BLOBs + numpy for search. Ugly but works to ~10k vectors.

### The Dump

- **[numpy](https://numpy.org/) dot product** — `reference_embeddings @ query_embedding`. Vectorized. Sub-millisecond at 10k vectors, ~10ms at 100k. The default until it gets slow.
- **[FAISS IndexFlatIP](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)** — same math as numpy, different storage. Persistence + slightly faster at scale.
- **[FAISS HNSW](https://github.com/nmslib/hnswlib)** — Hierarchical Navigable Small World graph. Approximate nearest-neighbor. Sub-millisecond at 10M vectors.
- **[FAISS IVF + PQ](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)** — inverted file + product quantization. Billion-scale at some accuracy cost.
- **[pgvector](https://github.com/pgvector/pgvector)** — Postgres extension. SQL-native. Slower than FAISS per query; much simpler operationally.
- **[Pinecone](https://www.pinecone.io/) / [Weaviate](https://weaviate.io/) / [Milvus](https://milvus.io/) / [Qdrant](https://qdrant.tech/)** — managed or self-hosted vector DBs. Overkill for most face recognition unless you're multi-tenant at scale.
- **SQLite + BLOBs + numpy** — the "zero infrastructure" option.
- **[Annoy (Spotify)](https://github.com/spotify/annoy)** — older tree-based ANN. Largely displaced by HNSW.

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
| Open-source | **[Silent-Face-Anti-Spoofing (MiniVision)](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing)** | Open-source project, good enough for low-stakes product demos |
| **Managed (default for prod)** | **[AWS Rekognition Liveness](https://aws.amazon.com/rekognition/face-liveness/)** or **[Face++ Liveness](https://www.faceplusplus.com/face-liveness-detection/)** | Customer-facing auth, KYC, bank-grade |
| Research | **[CelebA-Spoof-trained models](https://github.com/ZhangYuanhan-AI/CelebA-Spoof), or Face Anti-Spoofing Challenge submissions** | When you need to train your own |

### Why a managed service is the production default

Anti-spoofing has an attacker. The attacker will iterate against your model. Open-source anti-spoofing models are publicly known — attackers train against them. Managed services rotate their models, have challenge-response systems (blink, move head), and have orders of magnitude more training data than you'll ever have.

For anything customer-facing where being spoofed has cost (KYC, building access, banking), use a managed service. For demos and internal tooling, open-source is fine.

### When to pick something else

- **On-device, no network:** use the open-source model. Accept the weaker security.
- **Multi-modal sensors available (depth, IR):** use the sensor. A TrueDepth camera on iPhone beats any RGB-only anti-spoof. Apple's Face ID is this.

### The Dump

- **[Silent-Face-Anti-Spoofing (MiniVision)](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing)** — public model, RGB-only, works for printed photo + screen replay attacks. Pretrained weights on GitHub.
- **[CelebA-Spoof](https://github.com/ZhangYuanhan-AI/CelebA-Spoof)** — dataset + baseline model. Good for training custom anti-spoofs.
- **[MiniFASNet](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing)** — lightweight anti-spoof net, mobile-friendly.
- **[AWS Rekognition Liveness](https://aws.amazon.com/rekognition/face-liveness/)** — challenge-response + managed model. 2–3 seconds of user action required. Integrates with face verification.
- **[Face++ Liveness Detection](https://www.faceplusplus.com/face-liveness-detection/)** — similar; better in some Asian markets.
- **[IDnow](https://www.idnow.io/) / [Onfido](https://onfido.com/) / [Jumio](https://www.jumio.com/)** — identity verification stacks. Anti-spoofing is one component of a KYC pipeline.
- **[FaceTec ZoOm](https://www.facetec.com/)** — claims iBeta Level 2 compliance. Used in fintech.
- **[Apple FaceID](https://support.apple.com/en-us/102381) / Face ID-equivalent systems** — hardware-based (structured light / IR). Not something you deploy yourself.

### Graveyard

- **Blink detection as the entire anti-spoof** — trivially defeated by video replay. Historical.
- **Texture analysis (LBP on face) as a standalone** — defeated by high-res screens.

### Last reviewed

2026-04-22.

---

## Libraries that pull multiple sub-topics together

- **[InsightFace](https://github.com/deepinsight/insightface)** — the reference implementation of the *research* stack. SCRFD + ArcFace + landmarks + anti-spoof-ish. Open-source code (MIT), actively maintained, ONNX-ready. **The bundled pretrained weights are non-commercial research use only** — install it for research or internal work; don't ship the weights in a commercial product.
- **[face_recognition](https://github.com/ageitgey/face_recognition) (Adam Geitgey)** — dlib-based, historically popular, mostly unmaintained. Uses HOG + dlib ResNet encodings. Weaker than ArcFace on surveillance / pose, but **Boost/MIT-licensed end-to-end** — the commercial-safe open default for face rec in 2026.
- **[DeepFace](https://github.com/serengil/deepface) ([Sefik Serengil](https://github.com/serengil))** — Python wrapper around many detector/recognizer combinations. Good for prototype experiments ("what does FaceNet give me vs ArcFace?"). Library is MIT; the backbones it wraps carry their own (mostly non-commercial) licenses — check per-backbone before shipping.
- **[CompreFace](https://github.com/exadel-inc/CompreFace)** — self-hostable API server with enrollment and recognition endpoints. Uses InsightFace models under the hood, so inherits the same non-commercial constraint on the weights.
- **[facenet-pytorch](https://github.com/timesler/facenet-pytorch)** — if you specifically need PyTorch FaceNet. Niche now.

---

*Last reviewed: 2026-04-22. Written by Vikas Gupta.*
