import os
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Explicitly load .env from backend directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

def test_mongo():
    try:
        mongo_uri = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DB")
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        db = client[mongo_db]
        db.command("ping")
        print("MongoDB connection: SUCCESS")
    except Exception as e:
        print(f"MongoDB connection: FAILED - {e}")

def test_postgres():
    try:
        pg_uri = os.getenv("POSTGRES_URI")
        engine = create_engine(pg_uri, connect_args={"connect_timeout": 3})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        print("Postgres connection: SUCCESS")
    except OperationalError as e:
        print(f"Postgres connection: FAILED - {e}")
    except Exception as e:
        print(f"Postgres connection: FAILED - {e}")

if __name__ == "__main__":
    test_mongo()
    test_postgres()
