# Qdrant Learning Guide for qdrant-fabric

## Hands-On Learning Path

This guide helps you learn Qdrant's capabilities by using the 30 tools in qdrant-fabric.

---

## Level 1: Foundations (Collections & Points)

### Lesson 1.1: Understanding Collections

**Concept**: Collections are named containers for vectors with a defined structure.

**Tools to use**:
- `qdrant_db_collections_create`
- `qdrant_db_collections_list`
- `qdrant_db_collections_get`
- `qdrant_db_collections_exists`

**Exercise**:
```
1. "Create a collection called 'learning_test' with 384-dimensional vectors using cosine similarity"
2. "List all collections in my database"
3. "Get detailed information about the learning_test collection"
4. "Check if a collection named 'nonexistent' exists"
```

**Key Concepts**:
- Vector dimensions must match your embedding model
- Distance metrics: Cosine (direction), Euclidean (distance), Dot Product (magnitude)
- Collections define the schema for all points within them

### Lesson 1.2: Working with Points

**Concept**: Points are individual vector entries with optional metadata (payload).

**Tools to use**:
- `qdrant_db_points_upsert`
- `qdrant_db_points_get`
- `qdrant_db_points_count`
- `qdrant_db_points_scroll`

**Exercise**:
```
1. "Add 5 sample points to learning_test collection with random vectors and metadata"
2. "Get points with IDs 1, 2, and 3 from learning_test"
3. "Count how many points are in learning_test"
4. "Scroll through the first 3 points in learning_test"
```

**Key Concepts**:
- Each point has: ID, vector, optional payload
- IDs can be integers or UUIDs
- Upsert = insert or update (idempotent operation)

---

## Level 2: Search & Discovery

### Lesson 2.1: Vector Similarity Search

**Concept**: Find points with vectors similar to a query vector.

**Tools to use**:
- `qdrant_db_points_search`
- `qdrant_db_points_search_batch`

**Exercise**:
```
1. "Search for the 3 most similar points to vector [0.1, 0.2, ..., 0.384] in learning_test"
2. "Perform batch search with 2 different query vectors"
3. "Search with a filter to only return points where payload.category = 'test'"
```

**Key Concepts**:
- Query vector dimensions must match collection
- Results ranked by similarity score
- Filters narrow search space
- Batch operations improve performance

### Lesson 2.2: Recommendations

**Concept**: Find similar items based on positive/negative examples.

**Tools to use**:
- `qdrant_db_points_recommend`
- `qdrant_db_points_recommend_batch`

**Exercise**:
```
1. "Recommend 5 points similar to point ID 1 in learning_test"
2. "Recommend points like IDs [1, 2] but not like ID 3"
3. "Batch recommend based on multiple example sets"
```

**Key Concepts**:
- Positive examples: "more like this"
- Negative examples: "but not like that"
- Centroid-based approach
- Great for "similar items" features

---

## Level 3: Data Management

### Lesson 3.1: Payload Operations

**Concept**: Metadata attached to vectors for filtering and display.

**Tools to use**:
- `qdrant_db_payload_set`
- `qdrant_db_payload_overwrite`
- `qdrant_db_payload_delete`
- `qdrant_db_payload_clear`

**Exercise**:
```
1. "Set payload field 'category' to 'updated' for points [1, 2, 3]"
2. "Overwrite all payload on point 4 with new data"
3. "Delete the 'category' field from point 1"
4. "Clear all payload from point 5"
```

**Key Concepts**:
- Set = merge with existing payload
- Overwrite = replace entire payload
- Delete = remove specific fields
- Clear = remove all fields

### Lesson 3.2: Vector Operations

**Concept**: Update or remove vector data from points.

**Tools to use**:
- `qdrant_db_vectors_update`
- `qdrant_db_vectors_delete`

**Exercise**:
```
1. "Update the vector for point ID 1 in learning_test"
2. "Delete vectors from points [2, 3] (keeping payload)"
```

**Key Concepts**:
- Update vectors without changing payload
- Delete vectors but keep point structure
- Useful for embeddings that change over time

---

## Level 4: Optimization

### Lesson 4.1: Indexing

**Concept**: Create indexes on payload fields for faster filtering.

**Tools to use**:
- `qdrant_db_index_create`
- `qdrant_db_index_delete`

**Exercise**:
```
1. "Create an index on the 'category' field in learning_test"
2. "Create an index on 'timestamp' field with integer type"
3. "Delete the category index"
```

**Key Concepts**:
- Indexes speed up payload filtering
- Required for large collections with complex filters
- Trade-off: faster queries, more memory

### Lesson 4.2: Batch Operations

**Concept**: Combine multiple operations into single request.

**Tools to use**:
- `qdrant_db_points_batch`

**Exercise**:
```
1. "Use batch operations to upsert 10 points and delete 2 points in one request"
2. "Batch update: upsert new points, set payload, and update vectors"
```

**Key Concepts**:
- Atomic operations
- Better performance than individual requests
- All-or-nothing execution

---

## Level 5: Monitoring & Health

### Lesson 5.1: Health Checks

**Concept**: Monitor database status and performance.

**Tools to use**:
- `qdrant_db_health_root`
- `qdrant_db_health_check`
- `qdrant_db_health_liveness`
- `qdrant_db_health_readiness`
- `qdrant_db_health_metrics`

**Exercise**:
```
1. "Get Qdrant version information"
2. "Check if Qdrant is healthy"
3. "Check if Qdrant is ready to serve requests"
4. "Get Prometheus metrics from Qdrant"
```

**Key Concepts**:
- Liveness = is it running?
- Readiness = can it serve requests?
- Metrics = performance data
- Important for production monitoring

### Lesson 5.2: Collection Management

**Concept**: Maintain and optimize collections.

**Tools to use**:
- `qdrant_db_collections_update`
- `qdrant_db_collections_delete`

**Exercise**:
```
1. "Update learning_test collection to change optimizer settings"
2. "Delete the learning_test collection when done"
```

**Key Concepts**:
- Update config without recreating
- Deletion is permanent
- Always backup before deletion

---

## Real-World Patterns

### Pattern 1: Semantic Search Application
```
1. Create collection with embedding dimensions
2. Index documents with embeddings + metadata
3. Search with query embeddings
4. Filter results by metadata
5. Return top matches with payloads
```

### Pattern 2: Recommendation Engine
```
1. Store item embeddings with metadata
2. User likes item → get item ID
3. Recommend similar items
4. Exclude already-seen items with negative examples
5. Filter by category/preferences
```

### Pattern 3: Duplicate Detection
```
1. Index all items with content embeddings
2. For each item, search for similar items
3. Items above similarity threshold = potential duplicates
4. Use payload to verify (timestamp, source, etc.)
```

### Pattern 4: Hybrid Search
```
1. Create index on text fields for keyword search
2. Generate embeddings for semantic search
3. Perform vector search with payload filters
4. Combine keyword + semantic relevance
5. Rerank results if needed
```

### Pattern 5: Continuous Learning
```
1. Start with initial embeddings
2. Monitor user interactions
3. Update vectors based on feedback
4. Batch update periodically
5. A/B test old vs new embeddings
```

---

## AIANA Integration Examples

### Query AIANA's Semantic Memory
```
1. "List collections" → find aiana_memories
2. "Get info about aiana_memories collection"
3. "Search aiana_memories for discussions about MCP"
4. "Get recommendations based on a specific memory"
```

### Build Cross-Tool Workflows
```
1. User asks question
2. AIANA searches semantic memory
3. Returns relevant context
4. Claude uses context to answer
5. Answer stored back via AIANA
```

---

## Advanced Topics to Explore

### 1. Quantization
- Reduce memory usage
- Trade accuracy for speed
- Binary, scalar, product quantization

### 2. Named Vectors
- Multiple embeddings per point
- Different models for different purposes
- Title embedding + content embedding

### 3. Sparse Vectors
- BM25-style scoring
- Hybrid dense + sparse
- Better keyword matching

### 4. Discovery Search
- Explore vector space
- Find clusters
- Anomaly detection

### 5. Multi-Vector Search
- ColBERT-style retrieval
- Token-level matching
- More precise results

---

## Learning Resources

### Official Tutorials
- [Qdrant Learn Portal](https://qdrant.tech/learn/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Technical Articles](https://qdrant.tech/articles/)

### Courses
- Qdrant Essentials (Free)
- Retrieval Optimization (Deep Learning AI)
- Multi-Vector Retrieval (Deep Learning AI)

### Community
- [Discord](https://qdrant.to/discord)
- [GitHub](https://github.com/qdrant/qdrant)
- [Twitter](https://twitter.com/qdrant_engine)

---

## Practice Projects

### Project 1: Personal Knowledge Base
- Store notes/documents as vectors
- Semantic search across notes
- Find related content
- Build with qdrant-fabric tools

### Project 2: Content Recommendation
- Index articles/videos/products
- Recommend similar items
- Track user preferences
- Personalize results

### Project 3: Code Search
- Index code repositories
- Search by semantic meaning
- Find similar functions
- Detect duplicates

### Project 4: Question Answering
- Store document embeddings
- Search for relevant context
- Feed to LLM for answers
- RAG pattern implementation

### Project 5: Image Similarity
- Store image embeddings
- Find similar images
- Cluster by visual features
- Build visual search

---

## Next Steps

1. **Complete Level 1-2** - Master basics with qdrant-fabric tools
2. **Build Sample Project** - Apply learnings to real use case
3. **Explore AIANA** - Understand existing semantic memory
4. **Read Articles** - Deep dive into advanced topics
5. **Take Courses** - Structured learning paths
6. **Join Community** - Learn from others
7. **Plan Phase 2** - Ready for Cloud Management API

---

**Status**: Ready to learn by doing with qdrant-fabric! 🎓
