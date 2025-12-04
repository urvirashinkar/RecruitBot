# Postman Examples for `/chatbot/query` Endpoint

## Endpoint Details

**Method:** `GET`  
**URL:** `http://localhost:8000/chatbot/query`

**Query Parameters:**

- `query` or `text` (required) - Your search query
- `top_k` (optional, default: 5) - Number of results to return

---

## Example 1: Basic Query

### Request

```
GET http://localhost:8000/chatbot/query?query=data scientist with machine learning
```

### Postman Setup:

1. **Method:** GET
2. **URL:** `http://localhost:8000/chatbot/query`
3. **Params Tab:**
   - Key: `query`, Value: `data scientist with machine learning`
   - Key: `top_k`, Value: `5` (optional)

### Expected Response:

```json
{
  "results": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Alice Smith",
      "summary": "Experienced data scientist with a passion for NLP and ML.",
      "skills": ["Python", "ML", "NLP", "SQL"],
      "experience": [
        {
          "job_title": "Data Scientist",
          "company": "DataCorp"
        }
      ]
    },
    {
      "id": "507f1f77bcf86cd799439012",
      "name": "Grace Kim",
      "summary": "AI researcher focused on computer vision and deep learning.",
      "skills": ["Python", "PyTorch", "TensorFlow", "OpenCV"],
      "experience": [
        {
          "job_title": "AI Research Scientist",
          "company": "VisionAI Labs"
        }
      ]
    }
  ]
}
```

---

## Example 2: Using `text` Parameter

### Request

```
GET http://localhost:8000/chatbot/query?text=Python developer&top_k=3
```

### Postman Setup:

1. **Method:** GET
2. **URL:** `http://localhost:8000/chatbot/query`
3. **Params Tab:**
   - Key: `text`, Value: `Python developer`
   - Key: `top_k`, Value: `3`

### Expected Response:

```json
{
  "results": [
    {
      "id": "507f1f77bcf86cd799439011",
      "name": "Alice Smith",
      "summary": "Experienced data scientist with a passion for NLP and ML.",
      "skills": ["Python", "ML", "NLP", "SQL"],
      "experience": [...]
    },
    {
      "id": "507f1f77bcf86cd799439013",
      "name": "Henry Wilson",
      "summary": "Full-stack developer experienced in building scalable SaaS applications.",
      "skills": ["Node.js", "React", "PostgreSQL", "AWS"],
      "experience": [...]
    }
  ]
}
```

---

## Example 3: Frontend Developer Search

### Request

```
GET http://localhost:8000/chatbot/query?query=frontend developer React TypeScript
```

### Postman Setup:

1. **Method:** GET
2. **URL:** `http://localhost:8000/chatbot/query`
3. **Params Tab:**
   - Key: `query`, Value: `frontend developer React TypeScript`
   - Key: `top_k`, Value: `5`

### Expected Response:

```json
{
  "results": [
    {
      "id": "507f1f77bcf86cd799439014",
      "name": "Bob Lee",
      "summary": "Frontend engineer specializing in React and UI/UX design.",
      "skills": ["JavaScript", "React", "TypeScript", "CSS"],
      "experience": [
        {
          "job_title": "Frontend Engineer",
          "company": "Webify"
        }
      ]
    }
  ]
}
```

---

## Example 4: Backend Developer Search

### Request

```
GET http://localhost:8000/chatbot/query?query=backend developer Java Spring Boot&top_k=3
```

### Postman Setup:

1. **Method:** GET
2. **URL:** `http://localhost:8000/chatbot/query`
3. **Params Tab:**
   - Key: `query`, Value: `backend developer Java Spring Boot`
   - Key: `top_k`, Value: `3`

---

## Example 5: DevOps Engineer Search

### Request

```
GET http://localhost:8000/chatbot/query?text=DevOps engineer AWS Docker Kubernetes
```

### Postman Setup:

1. **Method:** GET
2. **URL:** `http://localhost:8000/chatbot/query`
3. **Params Tab:**
   - Key: `text`, Value: `DevOps engineer AWS Docker Kubernetes`
   - Key: `top_k`, Value: `5` (default)

---

## Example 6: Product Manager Search

### Request

```
GET http://localhost:8000/chatbot/query?query=product manager SaaS agile
```

---

## Visual Guide for Postman

### Step-by-Step in Postman:

1. **Create New Request**

   - Click "New" → "HTTP Request"
   - Name it: "RAG Query - Data Scientist"

2. **Set Method**

   - Select `GET` from dropdown

3. **Enter URL**

   - `http://localhost:8000/chatbot/query`

4. **Add Query Parameters**

   - Click on "Params" tab
   - Add parameter:
     - **Key:** `query`
     - **Value:** `data scientist with machine learning`
   - Add parameter (optional):
     - **Key:** `top_k`
     - **Value:** `5`

5. **Send Request**
   - Click "Send" button
   - View response in bottom panel

### Screenshot Reference:

```
┌─────────────────────────────────────────────────┐
│ GET  http://localhost:8000/chatbot/query       │
├─────────────────────────────────────────────────┤
│ Params | Authorization | Headers | Body | ...   │
├─────────────────────────────────────────────────┤
│ Query Params:                                    │
│ ☑ query: data scientist with machine learning  │
│ ☑ top_k: 5                                      │
└─────────────────────────────────────────────────┘
```

---

## Complete URL Examples

Copy and paste these directly into Postman:

```
http://localhost:8000/chatbot/query?query=data%20scientist%20with%20machine%20learning

http://localhost:8000/chatbot/query?query=Python%20developer&top_k=3

http://localhost:8000/chatbot/query?text=frontend%20developer%20React%20TypeScript&top_k=5

http://localhost:8000/chatbot/query?query=backend%20developer%20Java%20Spring%20Boot&top_k=3

http://localhost:8000/chatbot/query?query=DevOps%20engineer%20AWS%20Docker

http://localhost:8000/chatbot/query?query=product%20manager%20SaaS

http://localhost:8000/chatbot/query?query=UX%20designer&top_k=3

http://localhost:8000/chatbot/query?query=AI%20researcher%20deep%20learning&top_k=5
```

---

## Response Structure

All responses follow this format:

```json
{
  "results": [
    {
      "id": "string", // Candidate ID
      "name": "string", // Full name
      "summary": "string", // Professional summary
      "skills": ["string"], // Array of technical skills
      "experience": [
        // Array of work experience
        {
          "job_title": "string",
          "company": "string"
        }
      ]
    }
  ]
}
```

---

## Testing Tips

1. **Start with Health Check:**

   ```
   GET http://localhost:8000/health
   ```

   Should return: `{"status": "ok", "model_loaded": true}`

2. **Check Stats:**

   ```
   GET http://localhost:8000/stats
   ```

   Verify candidates exist in database

3. **Test Simple Query:**

   ```
   GET http://localhost:8000/chatbot/query?query=Python
   ```

4. **Test Complex Query:**
   ```
   GET http://localhost:8000/chatbot/query?query=data scientist with 5 years experience in machine learning
   ```

---

## Common Errors

### Error: 422 Unprocessable Entity

**Cause:** Missing `query` or `text` parameter  
**Solution:** Add `query` or `text` parameter to your request

### Error: 500 Internal Server Error

**Cause:** Database connection issue or model not loaded  
**Solution:**

- Check if server is running
- Check database connections
- Verify model is loaded (check `/health` endpoint)

### Error: Empty Results

**Cause:** No candidates in database or query doesn't match  
**Solution:**

- Run `python test_rag_and_data.py` to load dummy data
- Try a different query

---

## Quick Test Checklist

- [ ] Server running on port 8000
- [ ] Health check passes
- [ ] Stats show candidates exist
- [ ] Query returns results
- [ ] Results are relevant to query

---

**Note:** Make sure your FastAPI server is running:

```bash
cd backend
uvicorn main:app --reload --port 8000
```
