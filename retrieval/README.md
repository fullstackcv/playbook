# Image Retrieval / Embeddings

> "Find similar images to this query." The general version of face-search. Image embedding models + ANN (approximate nearest-neighbor) index.

Retrieval is the subtask of "given a database of images and a query image (or text), find the most similar ones." The default stack in 2026 is **CLIP-family embeddings + FAISS (or a vector DB)**. It's simple, strong, and scales to tens of millions of images on one box.

This page is the *general* retrieval case. For *face identity search specifically*, see the [`face/` section](../face/) — it uses face-specific embeddings (ArcFace) with the same ANN infrastructure.

## Recommended picks

| Component | Pick | When to use |
|-----------|------|-------------|
| **Embedding model (text + image)** | **SigLIP** or **OpenCLIP ViT-L/14** | Cross-modal retrieval, zero-shot classification doubling as retrieval |
| Embedding model (image only, strong transfer) | **DINOv2** | No text side; pure image-to-image. |
| Fine-tuned for retrieval | **train a SigLIP LoRA** or a model from the `sentence-transformers` image family | Domain-specific retrieval. |
| ANN index (self-hosted, one machine) | **FAISS** | < 100M vectors, you control the infra. |
| Managed vector DB | **pgvector** (Postgres ext), **Qdrant**, **Weaviate**, **Pinecone** | Multi-tenant, SQL integration, managed ops. |

## Why SigLIP/CLIP for most retrieval

Two reasons.

First, they're multimodal: you can query with text ("orange cat on a windowsill") or with an image. That's useful even if your current product is image-to-image — future product features might want text-driven search.

Second, they're pretrained at massive scale on web image-text pairs, which makes them strong at general-purpose "what is this about." Domain-specific fine-tuning improves them further but you often don't need it.

**SigLIP beats CLIP on the same compute budget.** Google's SigLIP replaced CLIP's contrastive softmax with a pairwise sigmoid loss, which trains better on large batches. SigLIP-L/14 is the current recommended baseline.

**OpenCLIP** is an open re-implementation of CLIP that's released many model variants (including on LAION-2B). Use it when you need weights CLIP didn't release (B/32, H/14, etc.).

## DINOv2 — when you don't need text

DINOv2 embeddings don't have a text side but they transfer even better than CLIP on pure image-to-image retrieval, especially for fine-grained distinctions. If your product is "find visually similar products" and you never need text query, DINOv2 is the pick.

## The ANN index

Once you have embeddings, you need to search them fast. Four tiers:

- **numpy dot product** — up to ~50K vectors. No index, just compute against all. Simplest.
- **FAISS** — up to ~100M on one box. HNSW for speed, IVF+PQ for scale.
- **pgvector** — if your stack is Postgres-centric. Slower than FAISS, simpler ops.
- **Managed vector DB (Qdrant, Weaviate, Pinecone, Milvus)** — multi-tenant, managed, scales to billions.

For most use cases, **FAISS** until you need multi-tenant. Then **pgvector** or **Qdrant**.

## When to pick something else

- **Duplicate / near-duplicate detection** → specialized hashes (pHash, aHash, dHash) are faster and designed for near-exact matches. Embedding models are overkill.
- **Exact object-level retrieval** (find this specific object in an image) → object detection first, then retrieval on the crop.
- **Face identity retrieval** → face-specific embeddings (ArcFace). Don't use CLIP for faces; it's not tuned for identity.
- **Reverse image search at web scale** (billions of images) → you need a specialized retrieval stack (locality-sensitive hashing, learned quantization, distributed systems). Probably buy, don't build.

## The three questions to narrow

1. **Text query, image query, or both?** Text → must use CLIP/SigLIP. Image only → DINOv2 is strong alternative.
2. **General concepts or domain-specific?** General → CLIP/SigLIP out of the box. Specific → fine-tune on your data.
3. **Scale?** < 50K → numpy. 50K–100M → FAISS. 100M+ → managed vector DB.

## The Dump

### Embedding models
- **CLIP (OpenAI, 2021)** — the grandfather. Still widely deployed.
- **OpenCLIP** — open re-implementation with LAION weights.
- **SigLIP (Google, 2023)** — improved CLIP. The recommended baseline.
- **DINOv2 (Meta, 2023)** — self-supervised ViT, image-only.
- **DINOv1** — earlier version.
- **Jina Embeddings** — commercial embedding API.
- **Cohere Embed** — commercial multimodal embeddings.
- **OpenAI text-embedding-3 + CLIP** — OpenAI's commercial embedding API (primarily text, CLIP for images).
- **BLIP-2 features** — intermediate activations used as embeddings. Uncommon.
- **MobileCLIP (Apple)** — mobile-friendly CLIP.

### ANN / vector search
- **FAISS (Meta)** — the standard. IndexFlatIP (brute), HNSW, IVF+PQ.
- **Annoy (Spotify)** — older tree-based, largely superseded.
- **ScaNN (Google)** — strong ANN.
- **hnswlib** — HNSW alone, the core data structure.
- **pgvector** — Postgres extension. SQL-native.
- **Qdrant** — open-source vector DB, Rust. Strong.
- **Weaviate** — open-source vector DB, knowledge-graph-flavored.
- **Pinecone** — managed vector DB, serverless.
- **Milvus** — open-source, scales huge.
- **Chroma** — Python-first, simple to deploy.
- **Vespa** — Yahoo! alumni vector + structured search engine.
- **LanceDB** — columnar vector DB, embedded.
- **Elasticsearch + vector search** — Elasticsearch's own vector support.
- **Redis Stack vector search** — Redis with vectors.

### Specialized retrieval
- **Perceptual hashes (pHash / aHash / dHash / wHash)** — near-duplicate detection.
- **VPR (Visual Place Recognition)** libraries — MapillarySLS, NetVLAD variants.
- **DOLG / SOLAR / etc.** — landmark retrieval research.
- **Swin + GeM pooling** — reference landmark retrieval baseline.

### Training libraries
- **open_clip** — train or fine-tune CLIP-family.
- **sentence-transformers** — library primarily for text, supports image encoders.
- **`transformers` (HF)** — many embedding models available.

## Graveyard

- **VGG features as a retrieval baseline** — retired.
- **SIFT + bag-of-words retrieval** — classical, retired for general retrieval. Still used in some SLAM/landmark pipelines.
- **Annoy as a default** — superseded by HNSW-based tools.

## Last reviewed

2026-04-22.
