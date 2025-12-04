# Quick Test Guide

## 🚀 Quick Start Testing

### 1. Test Database Connections (30 seconds)

```bash
cd backend
python test_db_connections.py
```

✅ Should show: `MongoDB connection: SUCCESS` and `Postgres connection: SUCCESS`

### 2. Load Data & Test RAG (2-5 minutes)

```bash
cd backend
python test_rag_and_data.py
```

✅ This will:

- Load all 9 dummy candidates
- Verify they're in both databases
- Test RAG queries and show results

### 3. Test via API (Optional)

```bash
# Terminal 1: Start server
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Test API
cd backend
python test_api_endpoints.py
```

## 📋 What Gets Tested

✅ **Database Connections**: MongoDB & PostgreSQL  
✅ **Data Loading**: 9 dummy candidates  
✅ **Data Verification**: All candidates in both DBs  
✅ **Embeddings**: Vector embeddings created (768D)  
✅ **RAG Queries**: Semantic search with 9 test queries  
✅ **API Endpoints**: FastAPI health & query endpoints

## 🔍 Sample RAG Test Queries

The test script automatically runs these queries:

- "data scientist with machine learning experience"
- "frontend developer React TypeScript"
- "backend developer Java Spring Boot"
- "product manager SaaS"
- "DevOps engineer AWS Docker"
- "Python developer"
- "full stack developer"
- "UX designer"
- "AI researcher deep learning"

## 📊 Expected Results

After running `test_rag_and_data.py`, you should see:

- ✅ 9 candidates loaded (or skipped if already exist)
- ✅ 9 candidates in MongoDB
- ✅ 9 candidates in PostgreSQL with embeddings
- ✅ Relevant search results for each query

## ⚠️ Common Issues

**"No candidates found"** → Run `test_rag_and_data.py` to load data

**"Connection failed"** → Check `.env` file and database status

**"Model loading fails"** → First run downloads model (~400MB), be patient

**"API connection refused"** → Start server: `uvicorn main:app --reload --port 8000`

## 📚 Full Documentation

See `TESTING_GUIDE.md` for detailed information.
