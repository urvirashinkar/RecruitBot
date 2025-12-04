import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query as FastAPIQuery
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from sqlalchemy import create_engine, text as sql_text
from sqlalchemy.exc import SQLAlchemyError
from embedding_utils import flatten_candidate, get_embedding, get_model
from bson import ObjectId
from bson.errors import InvalidId
from typing import List

from models import CandidateIn, CandidateShort, ExperienceShort

# --- Setup ---
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
logging.basicConfig(level=logging.INFO)

# --- FastAPI App Initialization ---
app = FastAPI()

@app.on_event("startup")
def startup_event():
    """Load the embedding model at startup."""
    logging.info("Loading embedding model...")
    try:
        get_model()
        logging.info("Embedding model loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load embedding model: {e}", exc_info=True)
        # Depending on the use case, you might want to exit the app if the model fails to load
        # raise RuntimeError("Failed to load embedding model") from e

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB Connections ---
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_CANDIDATES_COLLECTION = os.getenv("MONGO_CANDIDATES_COLLECTION", "resumes")
POSTGRES_URI = os.getenv("POSTGRES_URI")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]
candidates_col = mongo_db[MONGO_CANDIDATES_COLLECTION]
pg_engine = create_engine(POSTGRES_URI, pool_pre_ping=True)

# --- API Endpoints ---
@app.get("/")
def root():
    return {"message": "RAG Chatbot Backend is running"}

@app.get("/health")
def health_check():
    """Check if the embedding model is loaded."""
    model = get_model()
    if model is not None:
        return {"status": "ok", "model_loaded": True}
    else:
        return {"status": "error", "model_loaded": False}

@app.post("/candidates")
def add_candidate(payload: CandidateIn):
    try:
        candidate_dict = payload.candidate.model_dump()
        result = candidates_col.insert_one(candidate_dict)
        mongo_id = str(result.inserted_id)

        flat = flatten_candidate(candidate_dict)
        emb = get_embedding(flat)

        with pg_engine.begin() as conn:
            conn.execute(sql_text("""
                INSERT INTO candidates (candidate_id, content, embedding)
                VALUES (:cid, :content, :embedding)
            """), {"cid": mongo_id, "content": flat, "embedding": emb})
        return {"id": mongo_id}
    except Exception as e:
        logging.error(f"Failed to add candidate: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to add candidate: {str(e)}")

@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: str):
    try:
        doc = None
        try:
            doc = candidates_col.find_one({"_id": ObjectId(candidate_id)})
        except InvalidId:
            pass  # Not a valid ObjectId, proceed to check as a string

        if not doc:
            doc = candidates_col.find_one({"_id": candidate_id})

        if not doc:
            doc = candidates_col.find_one({"candidate_id": candidate_id})

        if not doc:
            raise HTTPException(status_code=404, detail="Candidate not found")

        doc["id"] = str(doc.get("_id") or doc.get("candidate_id"))
        doc.pop("_id", None)
        return doc
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logging.error(f"Failed to fetch candidate '{candidate_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/chatbot/query")
def chatbot_query(text: str = FastAPIQuery(None, alias="text"),
                  query: str = FastAPIQuery(None, alias="query"),
                  top_k: int = 5):
    user_query = text or query
    if not user_query:
        raise HTTPException(status_code=422, detail="A query string is required.")

    try:
        query_emb = get_embedding(user_query)

        with pg_engine.connect() as conn:
            res = conn.execute(sql_text("""
                SELECT candidate_id, content
                FROM candidates
                ORDER BY embedding <-> :query_emb
                LIMIT :top_k
            """), {"query_emb": str(query_emb), "top_k": top_k})
            rows = res.fetchall()

        candidate_ids = [str(row[0]) for row in rows]
        doc_map = _fetch_candidates_from_mongo(candidate_ids)

        results = []
        for row in rows:
            cid = str(row[0])
            doc = doc_map.get(cid)
            content = row[1]

            if not doc:
                results.append(CandidateShort(
                    id=cid,
                    name="Unknown Candidate",
                    summary=content[:400] + "..." if len(content) > 400 else content,
                    skills=[],
                    experience=[]
                ))
                continue

            pi = doc.get("personal_info", {})
            exp = doc.get("experience", [])
            results.append(CandidateShort(
                id=doc["id"],
                name=pi.get("full_name", "N/A"),
                summary=pi.get("summary", ""),
                skills=doc.get("skills", {}).get("technical", []),
                experience=[ExperienceShort(job_title=e.get("job_title", "N/A"), company=e.get("company", "N/A")) for e in exp]
            ))

        return {"results": results}
    except SQLAlchemyError as e:
        logging.error(f"Database error during chatbot query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logging.error(f"Failed to run RAG pipeline: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to run RAG pipeline: {str(e)}")

def _fetch_candidates_from_mongo(candidate_ids: List[str]) -> dict:
    doc_map = {}
    if not candidate_ids:
        return doc_map

    try:
        object_ids = [ObjectId(cid) for cid in candidate_ids if ObjectId.is_valid(cid)]
        string_ids = [cid for cid in candidate_ids if not ObjectId.is_valid(cid)]

        query = {
            "$or": [
                {"_id": {"$in": object_ids}},
                {"_id": {"$in": string_ids}},
                {"candidate_id": {"$in": candidate_ids}}
            ]
        }
        
        for doc in candidates_col.find(query):
            doc_id = str(doc['_id'])
            doc['id'] = doc_id
            doc.pop('_id', None)
            doc_map[doc_id] = doc

    except Exception as e:
        logging.error(f"An error occurred while fetching candidates from MongoDB: {e}", exc_info=True)

    return doc_map
