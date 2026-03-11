# LilHag RAG

A comprehensive Retrieval-Augmented Generation (RAG) system built with Domain-Driven Design (DDD) principles.

## Architecture

```
src/
├── domain/              # Domain Layer (Business Logic)
│   ├── entities/        # Core business entities
│   ├── value_objects/   # Immutable value types
│   ├── repositories/    # Abstract repository interfaces
│   └── services/        # Domain services
│
├── application/         # Application Layer (Use Cases)
│   ├── use_cases/       # Application use cases
│   └── services/        # Application services (abstractions)
│
├── infrastructure/      # Infrastructure Layer (Implementations)
│   ├── repositories/    # Repository implementations
│   └── services/        # External service implementations
│
└── interface/           # Interface Layer (API)
    ├── routes/          # API endpoints
    └── dependencies.py  # Dependency injection
```

## Features

### Document Ingestion
- **Chunk Size & Overlap**: Configurable chunking with overlap for context preservation
- **Broken PDF Handling**: Fallback extraction for corrupted PDFs
- **Text Normalization**: Unicode normalization, whitespace cleanup
- **Metadata Extraction**: Document metadata preservation

### Retrieval
- **Similarity Metrics**: Cosine (recommended) vs Dot Product
  - Cosine: Best for normalized text embeddings
  - Dot Product: Faster but requires pre-normalized vectors
- **Hybrid Search**: Combines vector + keyword search
- **Reranking**: Cross-encoder models for improved precision
- **Top-K Tuning**: Configurable result counts

### Generation
- **Prompt Engineering**: Structured prompts with grounding
- **Context Limiting**: Token-aware context management
- **Source Citation**: Enforced source references

### Performance
- **Embedding Batching**: Efficient batch API calls
- **Caching**: Memory cache for embeddings and search results
- **Latency Optimization**: Async processing throughout

### Evaluation
- **Retrieval Metrics**: Recall@K, Precision@K, MRR, NDCG
- **Regression Detection**: Compare against baselines

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd hermes-retrival

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your AI API key
```

### Running the Server

```bash
# Development
python src/main.py --reload --debug

# Production
python src/main.py --host 0.0.0.0 --port 8000
```

### API Usage

```bash
# Health check
curl http://localhost:8000/health

# Ingest a document
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -F "file=@document.pdf" \
  -F "title=My Document"

# Search
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?", "top_k": 5}'

# Chat/QA
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain the main concepts in the documents"}'
```

## Configuration Guide

### Chunking

| Parameter | Default | Recommendation |
|-----------|---------|----------------|
| `chunk_size` | 512 | 256-512 for Q&A, 512-1000 for summarization |
| `chunk_overlap` | 50 | 10-20% of chunk size |
| `strategy` | recursive | recursive for general use, sentence for precision |

### Search

| Parameter | Default | Notes |
|-----------|---------|-------|
| `similarity_metric` | cosine | Cosine for text, dot_product if pre-normalized |
| `search_type` | hybrid | Hybrid recommended for best results |
| `vector_weight` | 0.7 | Tune based on use case |
| `enable_reranking` | true | Improves precision, adds latency |

### Cosine vs Dot Product

**Cosine Similarity**:
- Measures angle between vectors (ignores magnitude)
- Range: -1 to 1 (1 = identical)
- Best for: Text embeddings (most models normalize outputs)
- Formula: `cos(θ) = (A·B) / (||A|| × ||B||)`

**Dot Product**:
- Measures both angle and magnitude
- Faster computation (no normalization step)
- Only equivalent to cosine when vectors are L2 normalized
- Best for: Pre-normalized embeddings, speed-critical applications

## API Documentation

Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

```bash
# Run tests
pytest src/__tests__/ -v

# Type checking
mypy src/

# Format code
black src/
isort src/
```

## License

MIT
