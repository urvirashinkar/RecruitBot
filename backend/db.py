import os
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[os.getenv("MONGO_DB", "recruitbot")]  # DB name
candidates_collection = mongo_db[os.getenv("MONGO_CANDIDATES_COLLECTION", "resumes")]

# NeonDB (Postgres + pgvector)
POSTGRES_URI = os.getenv("POSTGRES_URI")
engine = create_engine(POSTGRES_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# pgvector extension setup (run once in DB):
# CREATE EXTENSION IF NOT EXISTS vector;
# CREATE TABLE IF NOT EXISTS candidates (
#     id SERIAL PRIMARY KEY,
#     candidate_id TEXT,
#     content TEXT,
#     embedding VECTOR(768)
# );
