# NeonDB Embedding Queries Guide

This guide shows you how to check embeddings in NeonDB (PostgreSQL with pgvector) using SQL queries.

## Prerequisites

1. **Connection String**: Your `POSTGRES_URI` from `.env` file
2. **Database Client**:
   - Neon Console (web interface)
   - psql command line
   - DBeaver / pgAdmin
   - Python script (see `check_embeddings.py`)

---

## Quick Check Script

**Easiest way:** Run the Python script:

```bash
cd backend
python check_embeddings.py
```

This will show:

- Total number of embeddings
- Embedding dimensions
- List of all embeddings
- Sample embedding details

---

## SQL Queries

### 1. Check if Table Exists

```sql
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_name = 'candidates'
);
```

### 2. Count Total Embeddings

```sql
SELECT COUNT(*) as total_embeddings
FROM candidates;
```

### 3. Check Embedding Dimensions

```sql
SELECT
    array_length(embedding, 1) as embedding_dimension,
    COUNT(*) as count
FROM candidates
GROUP BY array_length(embedding, 1);
```

**Expected:** Should show `768` for all-mpnet-base-v2 model

### 4. List All Embeddings with Basic Info

```sql
SELECT
    candidate_id,
    LENGTH(content) as content_length,
    array_length(embedding, 1) as embedding_dim,
    LEFT(content, 100) as content_preview
FROM candidates
ORDER BY candidate_id;
```

### 5. View Specific Embedding Details

```sql
SELECT
    candidate_id,
    content,
    array_length(embedding, 1) as embedding_dim,
    embedding[1:10] as first_10_values
FROM candidates
WHERE candidate_id = 'your_candidate_id_here';
```

### 6. Check for NULL Embeddings

```sql
SELECT COUNT(*) as null_embeddings
FROM candidates
WHERE embedding IS NULL;
```

**Should return:** `0` (all should have embeddings)

### 7. View Full Embedding Vector (First 20 Values)

```sql
SELECT
    candidate_id,
    embedding[1:20] as embedding_preview
FROM candidates
LIMIT 5;
```

### 8. Test Vector Similarity Between Two Embeddings

```sql
-- Get two candidate IDs first
SELECT candidate_id FROM candidates LIMIT 2;

-- Then calculate similarity
SELECT
    c1.candidate_id as candidate_1,
    c2.candidate_id as candidate_2,
    c1.embedding <-> c2.embedding as cosine_distance,
    1 - (c1.embedding <-> c2.embedding) as cosine_similarity
FROM candidates c1, candidates c2
WHERE c1.candidate_id = 'first_id_here'
  AND c2.candidate_id = 'second_id_here';
```

**Note:**

- Lower `cosine_distance` = more similar
- Higher `cosine_similarity` = more similar

### 9. Find Most Similar Candidates to a Query

```sql
-- First, you need the query embedding (from Python or API)
-- Then use this query:
SELECT
    candidate_id,
    content,
    embedding <-> '[your_query_embedding_vector]'::vector as distance,
    1 - (embedding <-> '[your_query_embedding_vector]'::vector) as similarity
FROM candidates
ORDER BY embedding <-> '[your_query_embedding_vector]'::vector
LIMIT 5;
```

### 10. Get Statistics Summary

```sql
SELECT
    COUNT(*) as total_candidates,
    AVG(array_length(embedding, 1)) as avg_dimension,
    MIN(array_length(embedding, 1)) as min_dimension,
    MAX(array_length(embedding, 1)) as max_dimension,
    AVG(LENGTH(content)) as avg_content_length
FROM candidates;
```

---

## Using Neon Console (Web Interface)

1. **Go to Neon Console**: https://console.neon.tech
2. **Select your project**
3. **Open SQL Editor**
4. **Run queries** from above

### Example Workflow:

1. **Check connection:**

   ```sql
   SELECT version();
   ```

2. **Check table exists:**

   ```sql
   SELECT * FROM candidates LIMIT 1;
   ```

3. **Count embeddings:**

   ```sql
   SELECT COUNT(*) FROM candidates;
   ```

4. **View sample:**
   ```sql
   SELECT
       candidate_id,
       LEFT(content, 200) as preview,
       array_length(embedding, 1) as dim
   FROM candidates
   LIMIT 5;
   ```

---

## Using psql Command Line

```bash
# Connect to NeonDB
psql "your_postgres_uri_here"

# Then run SQL queries
SELECT COUNT(*) FROM candidates;
SELECT candidate_id, array_length(embedding, 1) FROM candidates;
```

---

## Using Python Script

### Quick Check:

```bash
cd backend
python check_embeddings.py
```

### Check Specific Candidate:

```bash
python check_embeddings.py <candidate_id>
```

### Programmatic Check:

```python
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("POSTGRES_URI"))

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM candidates"))
    count = result.scalar()
    print(f"Total embeddings: {count}")
```

---

## Common Issues & Solutions

### Issue: "relation 'candidates' does not exist"

**Solution:** Create the table:

```sql
CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    candidate_id TEXT,
    content TEXT,
    embedding VECTOR(768)
);
```

### Issue: "operator does not exist: vector"

**Solution:** Enable pgvector extension:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Issue: "No embeddings found"

**Solution:** Load dummy data:

```bash
python dummy_candidate.py
```

### Issue: "Embedding dimension mismatch"

**Solution:** Check your embedding model. For `all-mpnet-base-v2`, dimension should be 768.

---

## Expected Results

After loading dummy data, you should see:

- **Total embeddings:** 9 (or however many candidates you loaded)
- **Embedding dimension:** 768 (for all-mpnet-base-v2)
- **Content length:** Varies (typically 500-2000 characters)
- **NULL embeddings:** 0

---

## Verification Checklist

- [ ] Table `candidates` exists
- [ ] pgvector extension is enabled
- [ ] Embeddings have correct dimension (768)
- [ ] No NULL embeddings
- [ ] Vector similarity search works
- [ ] Content matches candidate data

---

## Advanced Queries

### Check Embedding Quality

```sql
-- Check if embeddings are normalized (should be close to 1.0)
SELECT
    candidate_id,
    sqrt(sum(power(unnest(embedding), 2))) as magnitude
FROM candidates
GROUP BY candidate_id;
```

### Find Duplicate Embeddings

```sql
SELECT
    c1.candidate_id as id1,
    c2.candidate_id as id2,
    c1.embedding <-> c2.embedding as distance
FROM candidates c1, candidates c2
WHERE c1.candidate_id < c2.candidate_id
  AND c1.embedding <-> c2.embedding < 0.01  -- Very similar
ORDER BY distance;
```

### Get Embedding Statistics

```sql
SELECT
    COUNT(*) as total,
    COUNT(DISTINCT array_length(embedding, 1)) as unique_dimensions,
    AVG(LENGTH(content)) as avg_content_length,
    MIN(LENGTH(content)) as min_content_length,
    MAX(LENGTH(content)) as max_content_length
FROM candidates;
```

---

For more information, see `check_embeddings.py` script.
