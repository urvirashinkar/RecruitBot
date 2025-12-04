# Testing Guide for RecruitBot

This guide explains how to test your dummy data and RAG model.

## Prerequisites

1. **Environment Setup**: Ensure your `.env` file in the `backend/` directory is configured:

   ```bash
   MONGO_URI=mongodb://localhost:27017/
   MONGO_DB=recruitbot
   MONGO_CANDIDATES_COLLECTION=candidates
   POSTGRES_URI=postgresql://user:password@localhost:5432/recruitbot
   EMBEDDING_MODEL=all-mpnet-base-v2
   ```

2. **Database Setup**: Make sure both MongoDB and PostgreSQL are running and accessible.

3. **Python Dependencies**: Install all requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Test Scripts Overview

### 1. `test_db_connections.py` - Database Connection Test

**Purpose**: Quick check if databases are accessible

**Usage**:

```bash
cd backend
python test_db_connections.py
```

**What it does**:

- Tests MongoDB connection
- Tests PostgreSQL connection
- Shows success/failure for each

**Expected Output**:

```
MongoDB connection: SUCCESS
Postgres connection: SUCCESS
```

---

### 2. `test_rag_and_data.py` - Comprehensive Data & RAG Test

**Purpose**: Load dummy data, verify it's present, and test RAG queries

**Usage**:

```bash
cd backend
python test_rag_and_data.py
```

**What it does**:

1. Loads all 9 dummy candidates into MongoDB and PostgreSQL
2. Verifies all candidates are present in MongoDB
3. Verifies all candidates are present in PostgreSQL with embeddings
4. Tests multiple RAG queries with different search terms
5. Displays ranked results for each query

**Expected Output**:

```
======================================================================
  LOADING DUMMY CANDIDATES
======================================================================
[1/9] ✓ Loaded: Alice Smith (ID: 507f1f77...)
[2/9] ✓ Loaded: Bob Lee (ID: 507f1f78...)
...

======================================================================
  VERIFYING MONGODB DATA
======================================================================
Total candidates in MongoDB: 9
Candidates in MongoDB:
  1. Alice Smith (alice@example.com) - ID: 507f1f77...
  2. Bob Lee (bob@example.com) - ID: 507f1f78...
  ...

======================================================================
  VERIFYING POSTGRESQL DATA
======================================================================
Total candidates in PostgreSQL: 9
Candidates in PostgreSQL:
  1. ID: 507f1f77... | Content: 1234 chars | Embedding: 768D
  ...

======================================================================
  TESTING RAG QUERIES
======================================================================
🔍 Query: 'data scientist with machine learning experience'
----------------------------------------------------------------------
  1. Alice Smith
     Role: Data Scientist
     Skills: Python, ML, NLP, SQL
     Summary: Experienced data scientist with a passion for NLP and ML...
```

**Features**:

- Skips candidates that already exist (by email)
- Shows detailed information for each candidate
- Tests semantic search with various queries
- Displays ranked results based on similarity

---

### 3. `test_api_endpoints.py` - API Endpoint Test

**Purpose**: Test the RAG model through FastAPI endpoints

**Prerequisites**: FastAPI server must be running

```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Usage**:

```bash
# Test all endpoints
cd backend
python test_api_endpoints.py

# Test specific candidate
python test_api_endpoints.py <candidate_id>
```

**What it does**:

1. Tests the `/health` endpoint
2. Tests multiple RAG queries via `/chatbot/query`
3. Optionally tests getting a specific candidate by ID

**Expected Output**:

```
======================================================================
  TESTING HEALTH ENDPOINT
======================================================================
✓ Health check passed
  Status: ok
  Model loaded: True

======================================================================
  TESTING RAG QUERIES
======================================================================
🔍 Testing RAG Query: 'data scientist with machine learning experience'
----------------------------------------------------------------------
  Found 3 results:

  1. Alice Smith
     Experience: Data Scientist at DataCorp
     Skills: Python, ML, NLP, SQL
     Summary: Experienced data scientist with a passion for NLP and ML...
```

---

## Step-by-Step Testing Workflow

### Step 1: Test Database Connections

```bash
cd backend
python test_db_connections.py
```

✅ **Expected**: Both connections succeed

### Step 2: Load and Verify Dummy Data

```bash
cd backend
python test_rag_and_data.py
```

✅ **Expected**:

- All 9 candidates loaded
- All candidates verified in both databases
- RAG queries return relevant results

### Step 3: Test via API (Optional)

```bash
# Terminal 1: Start FastAPI server
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Test API endpoints
cd backend
python test_api_endpoints.py
```

✅ **Expected**: API responds correctly with RAG results

---

## Understanding the Test Results

### RAG Query Results

When testing RAG queries, results are ranked by semantic similarity:

- **Higher similarity** = More relevant to your query
- Results are ordered from most to least relevant
- The embedding model converts text to vectors and finds similar candidates

### Example Query Analysis

**Query**: "data scientist with machine learning experience"

**Expected Top Results**:

1. **Alice Smith** - Data Scientist with ML/NLP experience
2. **Grace Kim** - AI Research Scientist (related field)
3. **Henry Wilson** - Full-stack developer (less relevant)

The RAG model should rank Alice first because her profile most closely matches the query semantically.

---

## Troubleshooting

### Issue: "No candidates found in MongoDB"

**Solution**: Run `test_rag_and_data.py` to load dummy candidates

### Issue: "PostgreSQL connection failed"

**Solution**:

- Check your `POSTGRES_URI` in `.env`
- Ensure PostgreSQL is running
- Verify pgvector extension is installed: `CREATE EXTENSION vector;`

### Issue: "Model loading fails"

**Solution**:

- First run downloads the model (~400MB) - be patient
- Check internet connection
- Ensure enough disk space

### Issue: "RAG queries return no results"

**Solution**:

- Verify candidates are in PostgreSQL with embeddings
- Check that embeddings were created (should be 768D for all-mpnet-base-v2)
- Ensure the candidates table exists with proper schema

### Issue: "API connection refused"

**Solution**:

- Start the FastAPI server: `uvicorn main:app --reload --port 8000`
- Check the port matches (default: 8000)

---

## Dummy Candidates Overview

The test suite includes 9 dummy candidates:

1. **Alice Smith** - Data Scientist (Python, ML, NLP)
2. **Bob Lee** - Frontend Engineer (React, TypeScript)
3. **Carol Zhang** - Product Manager (SaaS, Agile)
4. **David Johnson** - Backend Developer (Java, Spring Boot, Microservices)
5. **Emma Davis** - UX/UI Designer (Figma, Adobe XD)
6. **Frank Miller** - DevOps Engineer (Terraform, AWS, Kubernetes)
7. **Grace Kim** - AI Research Scientist (PyTorch, Computer Vision)
8. **Henry Wilson** - Full-stack Developer (Node.js, React, PostgreSQL)

Each candidate has:

- Complete personal information
- Education history
- Work experience
- Projects
- Skills (technical, soft, languages)
- Certifications
- Achievements
- Publications (where applicable)

---

## Advanced Testing

### Test Specific Query Types

You can modify `test_rag_and_data.py` to test specific queries:

```python
# Add to test_rag_queries() function
custom_queries = [
    "Java developer with Spring Boot experience",
    "React frontend developer with 5 years experience",
    "DevOps engineer with Kubernetes and AWS"
]
```

### Test Embedding Quality

Check embedding dimensions:

```python
# In test_rag_and_data.py, verify_postgres_data() shows:
# Embedding: 768D (for all-mpnet-base-v2)
```

### Test with Different Top-K Values

Modify the `top_k` parameter:

```python
test_rag_query("your query", top_k=10)  # Get top 10 results
```

---

## Next Steps

After successful testing:

1. ✅ All dummy data loaded and verified
2. ✅ RAG model working correctly
3. ✅ API endpoints functional (if tested)

You're ready to:

- Use the frontend to search candidates
- Add real candidate data via the API
- Customize the embedding model if needed
- Deploy to production

---

## Quick Reference

| Script                   | Purpose              | Command                         |
| ------------------------ | -------------------- | ------------------------------- |
| `test_db_connections.py` | Test DB connections  | `python test_db_connections.py` |
| `test_rag_and_data.py`   | Load data & test RAG | `python test_rag_and_data.py`   |
| `test_api_endpoints.py`  | Test API endpoints   | `python test_api_endpoints.py`  |
| `dummy_candidate.py`     | Load dummy data only | `python dummy_candidate.py`     |

---

For more information, see the main README.md in the project root.
