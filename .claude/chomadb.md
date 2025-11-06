---
name: chromadb
description: ChromaDB vector database for AI applications. Use for embeddings, RAG (Retrieval Augmented Generation), semantic search, and vector similarity search.
---

# ChromaDB Skill

Comprehensive assistance with ChromaDB development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- **Building RAG systems** - Implementing Retrieval Augmented Generation with LLMs
- **Vector similarity search** - Finding semantically similar content
- **Semantic search** - Searching by meaning rather than exact keywords
- **Working with embeddings** - Managing text, image, or multimodal embeddings
- **Creating AI knowledge bases** - Building persistent memory for AI applications
- **Debugging ChromaDB code** - Troubleshooting collection operations or queries
- **Deploying ChromaDB** - Setting up client-server, cloud, or distributed modes
- **Integrating with AI frameworks** - Using ChromaDB with LangChain, LlamaIndex, Haystack
- **Multimodal AI applications** - Working with text and image data together

## Key Concepts

### Core Abstractions
- **Collections** - Named groups of embeddings with associated documents and metadata
- **Embeddings** - Vector representations of data (text, images, etc.) for similarity search
- **Documents** - Original text/content associated with embeddings
- **Metadata** - Key-value pairs for filtering and organizing data
- **Distance Functions** - Methods for measuring similarity (L2, cosine, inner product)

### Deployment Modes
- **EphemeralClient** - In-memory storage (no persistence, for testing)
- **PersistentClient** - Local disk storage (Python only)
- **HttpClient** - Connect to remote ChromaDB server
- **CloudClient** - Managed ChromaDB Cloud service

### Querying Capabilities
- **Similarity Search** - Find nearest neighbors by vector distance
- **Metadata Filtering** - Filter results by metadata conditions
- **Full-Text Search** - Search documents using keywords and regex
- **Hybrid Search** - Combine vector similarity with metadata and text filters

## Quick Reference

### 1. Basic Setup and Collection Creation

**Python:**
```python
import chromadb

# Create client (in-memory)
client = chromadb.EphemeralClient()

# Create client (persistent)
client = chromadb.PersistentClient(path="/path/to/data")

# Create or get collection
collection = client.get_or_create_collection(
    name="my_collection",
    metadata={"description": "My first collection"}
)
```

**TypeScript:**
```typescript
import { ChromaClient } from 'chromadb';

// Create client
const client = new ChromaClient();

// Create or get collection
const collection = await client.getOrCreateCollection({
  name: "my_collection",
  metadata: { description: "My first collection" }
});
```

### 2. Adding Data to Collections

**Python:**
```python
# Add documents with auto-generated embeddings
collection.add(
    documents=["This is document 1", "This is document 2"],
    metadatas=[{"source": "web"}, {"source": "book"}],
    ids=["id1", "id2"]
)

# Add with custom embeddings
collection.add(
    embeddings=[[1.2, 2.3, 4.5], [6.7, 8.2, 9.2]],
    documents=["Document 1", "Document 2"],
    ids=["id1", "id2"]
)
```

**TypeScript:**
```typescript
// Add documents
await collection.add({
  ids: ["id1", "id2"],
  documents: ["This is document 1", "This is document 2"],
  metadatas: [{ source: "web" }, { source: "book" }]
});
```

### 3. Querying Collections

**Python:**
```python
# Query by text (semantic search)
results = collection.query(
    query_texts=["machine learning algorithms"],
    n_results=5
)

# Query by embedding
results = collection.query(
    query_embeddings=[[1.2, 3.4, 5.6]],
    n_results=10
)

# Query with metadata filtering
results = collection.query(
    query_texts=["python tutorial"],
    n_results=5,
    where={"source": "web"}
)
```

**TypeScript:**
```typescript
// Query by text
const results = await collection.query({
  queryTexts: ["machine learning algorithms"],
  nResults: 5
});

// Query with metadata filtering
const results = await collection.query({
  queryTexts: ["python tutorial"],
  nResults: 5,
  where: { source: "web" }
});
```

### 4. Metadata Filtering

**Python:**
```python
# Comparison operators
results = collection.get(
    where={"year": {"$gte": 2020}}  # Greater than or equal
)

# Logical operators (AND)
results = collection.get(
    where={
        "$and": [
            {"category": "tech"},
            {"year": {"$gte": 2020}}
        ]
    }
)

# Logical operators (OR)
results = collection.get(
    where={
        "$or": [
            {"category": "tech"},
            {"category": "science"}
        ]
    }
)

# Inclusion operator
results = collection.get(
    where={"category": {"$in": ["tech", "science", "math"]}}
)
```

### 5. Full-Text Search and Regex

**Python:**
```python
# Full-text search
results = collection.get(
    where_document={"$contains": "machine learning"}
)

# Regex search
results = collection.get(
    where_document={"$regex": "python.*tutorial"}
)

# Combine with metadata filtering
results = collection.query(
    query_texts=["AI tutorial"],
    where={"source": "web"},
    where_document={"$contains": "beginner"}
)
```

### 6. Updating and Upserting Data

**Python:**
```python
# Update existing documents
collection.update(
    ids=["id1"],
    documents=["Updated document text"],
    metadatas=[{"source": "updated"}]
)

# Upsert (update if exists, insert if not)
collection.upsert(
    ids=["id1", "id2"],
    documents=["Doc 1", "Doc 2"],
    metadatas=[{"status": "current"}, {"status": "current"}]
)
```

**TypeScript:**
```typescript
// Update documents
await collection.update({
  ids: ["id1"],
  documents: ["Updated document text"],
  metadatas: [{ source: "updated" }]
});

// Upsert
await collection.upsert({
  ids: ["id1", "id2"],
  documents: ["Doc 1", "Doc 2"],
  metadatas: [{ status: "current" }, { status: "current" }]
});
```

### 7. Client-Server Mode

**Python Server:**
```bash
# Install and run ChromaDB server
pip install chromadb
chroma run --host 0.0.0.0 --port 8000
```

**Python Client:**
```python
import chromadb

# Connect to remote server
client = chromadb.HttpClient(
    host="localhost",
    port=8000
)

# Use collections as normal
collection = client.get_or_create_collection("my_collection")
```

**TypeScript Client:**
```typescript
import { ChromaClient } from 'chromadb';

const client = new ChromaClient({
  path: "http://localhost:8000"
});
```

### 8. Custom Embedding Functions

**Python:**
```python
from chromadb.utils import embedding_functions

# OpenAI embeddings
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-api-key",
    model_name="text-embedding-3-small"
)

collection = client.create_collection(
    name="openai_collection",
    embedding_function=openai_ef
)

# Sentence Transformers (Hugging Face)
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.create_collection(
    name="st_collection",
    embedding_function=sentence_transformer_ef
)
```

### 9. ChromaDB Cloud Client

**Python:**
```python
import chromadb

# Connect to Chroma Cloud
client = chromadb.CloudClient(
    tenant="my-tenant",
    database="my-database",
    api_key="your-api-key"
)

# Or use environment variables
# export CHROMA_API_KEY="your-api-key"
client = chromadb.CloudClient(
    tenant="my-tenant",
    database="my-database"
)
```

**TypeScript:**
```typescript
import { CloudClient } from 'chromadb';

const client = new CloudClient({
  tenant: "my-tenant",
  database: "my-database",
  apiKey: "your-api-key"
});
```

### 10. Managing Collections

**Python:**
```python
# List all collections
collections = client.list_collections()

# Count collections
count = client.count_collections()

# Get collection
collection = client.get_collection(name="my_collection")

# Delete collection
client.delete_collection(name="my_collection")

# Get collection items count
count = collection.count()

# Peek at first items
items = collection.peek(limit=5)
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### collections.md
Contains detailed information about:
- **Client APIs** - Python and JavaScript ChromaClient documentation
- **Collection Class** - Methods for managing collections (add, query, update, delete, upsert)
- **Reference Links** - Links to official Python and JS client API documentation
- When working with collection operations, CRUD operations, or data management

### other.md
Contains information about:
- **Chroma Cloud** - Managed service, pricing, quotas, and limits
- **CLI Tools** - Commands for browsing, copying, database management, authentication
- **Integrations** - Embedding model providers (OpenAI, Cohere, Hugging Face, etc.)
- **Frameworks** - Integration with LangChain, LlamaIndex, Haystack, Streamlit
- **Deployment** - AWS, Azure, GCP deployment guides, Docker, observability
- **Development** - FastAPI and Next.js integration patterns
- When deploying, integrating with other tools, or setting up cloud infrastructure

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start by:
1. Understanding the data model (Collections, Documents, Embeddings, Metadata)
2. Learning basic client setup (EphemeralClient for testing, PersistentClient for local storage)
3. Practicing CRUD operations (add, get, query, update, delete)
4. Experimenting with simple semantic search queries
5. Review the "Getting Started" section in the official docs (linked in references)

### For Intermediate Users
Focus on:
1. Metadata filtering and full-text search for precise queries
2. Custom embedding functions for domain-specific use cases
3. Client-server mode for production deployments
4. Integration with AI frameworks (LangChain, LlamaIndex)
5. Performance optimization with index configuration (HNSW parameters)

### For Advanced Users
Explore:
1. Distributed ChromaDB deployment for large-scale applications
2. Multimodal collections (text + images)
3. Custom embedding functions with specialized models
4. Observability and monitoring with OpenTelemetry
5. Database and tenant management in ChromaDB Cloud
6. Advanced metadata filtering with complex logical operators

### Navigation Tips
- **Quick setup?** → See Quick Reference examples 1-2
- **Searching data?** → See Quick Reference examples 3-5
- **Filtering results?** → See Quick Reference examples 4-5
- **Production deployment?** → See Quick Reference example 7, check `other.md` for deployment guides
- **Using with LangChain/LlamaIndex?** → Check integrations in `other.md`
- **Cloud setup?** → See Quick Reference example 9, review Cloud section in `other.md`

## Common Patterns

### RAG (Retrieval Augmented Generation)
```python
# 1. Add documents to collection
collection.add(
    documents=["Document content..."],
    ids=["doc1"]
)

# 2. Query for relevant context
results = collection.query(
    query_texts=["User question"],
    n_results=3
)

# 3. Pass results to LLM
context = "\n".join(results['documents'][0])
# Use context with your LLM...
```

### Incremental Updates
```python
# Use upsert for safe incremental updates
collection.upsert(
    ids=["id1", "id2"],
    documents=["New or updated doc 1", "New or updated doc 2"],
    metadatas=[{"timestamp": "2025-01-15"}, {"timestamp": "2025-01-15"}]
)
```

### Filtered Semantic Search
```python
# Combine semantic search with metadata filtering
results = collection.query(
    query_texts=["machine learning"],
    n_results=5,
    where={"category": "tutorial", "year": {"$gte": 2023}},
    where_document={"$contains": "python"}
)
```

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations of all API methods
- Code examples with language annotations
- Links to original documentation
- Coverage of all deployment modes and integrations

### scripts/
Add helper scripts here for common automation tasks like:
- Batch document ingestion
- Collection backup/restore
- Embedding migration scripts

### assets/
Add templates, boilerplate, or example projects here like:
- Sample RAG application templates
- Configuration files for different deployment modes
- Example collection schemas

## Important Notes

- **IDs must be unique** - Adding duplicate IDs will raise an error unless using `upsert`
- **Embeddings dimension must match** - All embeddings in a collection must have the same dimensionality
- **Rate limits** - ChromaDB Cloud has quotas for reads, writes, and storage (see `other.md`)
- **Default embedding function** - Collections use `all-MiniLM-L6-v2` by default (384 dimensions)
- **Distance metrics** - Collections support L2 (default), cosine, and inner product distance
- **Metadata types** - Supports string, int, float, and bool values only
- **Delete is irreversible** - No undo for `.delete()` operations

## Troubleshooting

### Common Issues
1. **"Embedding dimension mismatch"** - Ensure all embeddings have the same dimension
2. **"Duplicate ID"** - Use `.upsert()` instead of `.add()` for updates
3. **Empty query results** - Check embedding function matches between add and query
4. **Connection errors** - Verify server is running and host/port are correct
5. **HNSW index errors** - See troubleshooting guide in `other.md`

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information

---

**Generated from official ChromaDB documentation**
