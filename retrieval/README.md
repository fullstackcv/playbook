# Image Retrieval / Embeddings

> "Find similar images to this query." The general version of face-search. Image embedding models + ANN (approximate nearest-neighbor) index.

Retrieval is the subtask of "given a database of images and a query image (or text), find the most similar ones." The default stack in 2026 is **CLIP-family embeddings + FAISS (or a vector DB)**. It's simple, strong, and scales to tens of millions of images on one box.

This page is the *general* retrieval case. For *face identity search specifically*, see the [`face/` section](../face/README.md) — it uses face-specific embeddings (ArcFace) with the same ANN infrastructure.

## Recommended picks

| Component | Pick | When to use |
|-----------|------|-------------|
| **Embedding model (text + image)** | **[SigLIP](https://github.com/google-research/big_vision)** or **[OpenCLIP ViT-L/14](https://github.com/mlfoundations/open_clip)** | Cross-modal retrieval, zero-shot classification doubling as retrieval |
| Embedding model (image only, strong transfer) | **[DINOv3](https://github.com/facebookresearch/dinov3)** | No text side; pure image-to-image. |

> [!WARNING]
> **Embedding model licenses:**
> - **DINOv3**: commercial-friendly Meta license (first DINO generation that's commercial-safe).
> - **DINOv2 / DINOv1**: CC-BY-NC 4.0 — **non-commercial**. Still widely deployed but check if your product is commercial before relying on DINOv2.
> - **CLIP** (MIT), **OpenCLIP** (MIT), **SigLIP** (Apache-2.0): all commercial-safe.
> - **Jina / Cohere / OpenAI embeddings**: commercial APIs, licensed via vendor T&C.
| Fine-tuned for retrieval | **train a SigLIP LoRA** or a model from the **[`sentence-transformers`](https://github.com/UKPLab/sentence-transformers)** image family | Domain-specific retrieval. |
| ANN index (self-hosted, one machine) | **[FAISS](https://github.com/facebookresearch/faiss)** | < 100M vectors, you control the infra. |
| Managed vector DB | **[pgvector](https://github.com/pgvector/pgvector)** (Postgres ext), **[Qdrant](https://qdrant.tech/)**, **[Weaviate](https://weaviate.io/)**, **[Pinecone](https://www.pinecone.io/)** | Multi-tenant, SQL integration, managed ops. |

## Why SigLIP/CLIP for most retrieval

Two reasons.

First, they're multimodal: you can query with text ("orange cat on a windowsill") or with an image. That's useful even if your current product is image-to-image — future product features might want text-driven search.

Second, they're pretrained at massive scale on web image-text pairs, which makes them strong at general-purpose "what is this about." Domain-specific fine-tuning improves them further but you often don't need it.

**SigLIP beats CLIP on the same compute budget.** Google's SigLIP replaced CLIP's contrastive softmax with a pairwise sigmoid loss, which trains better on large batches. SigLIP-L/14 is the current recommended baseline.

**OpenCLIP** is an open re-implementation of CLIP that's released many model variants (including on LAION-2B). Use it when you need weights CLIP didn't release (B/32, H/14, etc.).

## DINOv3 — when you don't need text

DINOv3 embeddings don't have a text side but they transfer even better than CLIP on pure image-to-image retrieval, especially for fine-grained distinctions. If your product is "find visually similar products" and you never need text query, DINOv3 is the pick.

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

1. **Text query, image query, or both?** Text → must use CLIP/SigLIP. Image only → DINOv3 is strong alternative.
2. **General concepts or domain-specific?** General → CLIP/SigLIP out of the box. Specific → fine-tune on your data.
3. **Scale?** < 50K → numpy. 50K–100M → FAISS. 100M+ → managed vector DB.

## The Dump

### Embedding models
- **[CLIP (OpenAI, 2021)](https://github.com/openai/CLIP)** — the grandfather. Still widely deployed.
- **[OpenCLIP](https://github.com/mlfoundations/open_clip)** — open re-implementation with LAION weights.
- **[SigLIP (Google, 2023)](https://github.com/google-research/big_vision)** — improved CLIP. The recommended baseline.
- **[DINOv3 (Meta, Aug 2025)](https://github.com/facebookresearch/dinov3)** — self-supervised ViT, image-only. 7B params, 1.7B training images. Current default for image-to-image retrieval. *License: commercial-friendly.*
- **[DINOv2 (Meta, 2023)](https://github.com/facebookresearch/dinov2)** — predecessor. Still widely deployed; comparable recipe, smaller compute. *License: **CC-BY-NC 4.0 — non-commercial**.*
- **[DINOv1 (Meta, 2021)](https://github.com/facebookresearch/dino)** — original. Historical. *License: **CC-BY-NC 4.0 — non-commercial**.*
- **[Jina Embeddings](https://jina.ai/embeddings/)** — commercial embedding API.
- **[Cohere Embed](https://cohere.com/embeddings)** — commercial multimodal embeddings.
- **[OpenAI text-embedding-3 + CLIP](https://platform.openai.com/docs/guides/embeddings)** — OpenAI's commercial embedding API (primarily text, CLIP for images).
- **[BLIP-2 features](https://github.com/salesforce/LAVIS/tree/main/projects/blip2)** — intermediate activations used as embeddings. Uncommon.
- **[MobileCLIP (Apple)](https://github.com/apple/ml-mobileclip)** — mobile-friendly CLIP.

### ANN / vector search
- **[FAISS (Meta)](https://github.com/facebookresearch/faiss)** — the standard. IndexFlatIP (brute), HNSW, IVF+PQ.
- **[Annoy (Spotify)](https://github.com/spotify/annoy)** — older tree-based, largely superseded.
- **[ScaNN (Google)](https://github.com/google-research/google-research/tree/master/scann)** — strong ANN.
- **[hnswlib](https://github.com/nmslib/hnswlib)** — HNSW alone, the core data structure.
- **[pgvector](https://github.com/pgvector/pgvector)** — Postgres extension. SQL-native.
- **[Qdrant](https://qdrant.tech/)** — open-source vector DB, Rust. Strong.
- **[Weaviate](https://weaviate.io/)** — open-source vector DB, knowledge-graph-flavored.
- **[Pinecone](https://www.pinecone.io/)** — managed vector DB, serverless.
- **[Milvus](https://milvus.io/)** — open-source, scales huge.
- **[Chroma](https://www.trychroma.com/)** — Python-first, simple to deploy.
- **[Vespa](https://vespa.ai/)** — Yahoo! alumni vector + structured search engine.
- **[LanceDB](https://lancedb.com/)** — columnar vector DB, embedded.
- **[Elasticsearch + vector search](https://www.elastic.co/elasticsearch/vector-database)** — Elasticsearch's own vector support.
- **[Redis Stack vector search](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/)** — Redis with vectors.

### Specialized retrieval
- **[Perceptual hashes (pHash / aHash / dHash / wHash)](https://github.com/JohannesBuchner/imagehash)** — near-duplicate detection.
- **VPR (Visual Place Recognition)** libraries — [MapillarySLS](https://github.com/mapillary/mapillary_sls), [NetVLAD variants](https://github.com/Nanne/pytorch-NetVlad).
- **DOLG / SOLAR / etc.** — landmark retrieval research.
- **Swin + GeM pooling** — reference landmark retrieval baseline.

### Training libraries
- **[open_clip](https://github.com/mlfoundations/open_clip)** — train or fine-tune CLIP-family.
- **[sentence-transformers](https://github.com/UKPLab/sentence-transformers)** — library primarily for text, supports image encoders.
- **[`transformers` (HF)](https://github.com/huggingface/transformers)** — many embedding models available.

## Graveyard

- **VGG features as a retrieval baseline** — retired.
- **SIFT + bag-of-words retrieval** — classical, retired for general retrieval. Still used in some SLAM/landmark pipelines.
- **Annoy as a default** — superseded by HNSW-based tools.

## Last reviewed

2026-04-22.
