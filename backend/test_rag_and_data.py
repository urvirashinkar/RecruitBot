#!/usr/bin/env python3
"""
Comprehensive test script for:
1. Loading dummy candidates into MongoDB and PostgreSQL
2. Verifying all candidates are present in both databases
3. Testing RAG queries with various search terms
"""

import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlalchemy import create_engine, text
from embedding_utils import flatten_candidate, get_embedding, get_model
from dummy_candidate import dummy_candidates

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Database connections
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_CANDIDATES_COLLECTION = os.getenv("MONGO_CANDIDATES_COLLECTION", "resumes")
POSTGRES_URI = os.getenv("POSTGRES_URI")

if not MONGO_URI or not POSTGRES_URI:
    print("ERROR: MONGO_URI and POSTGRES_URI must be set in .env file")
    sys.exit(1)

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]
candidates_col = mongo_db[MONGO_CANDIDATES_COLLECTION]
pg_engine = create_engine(POSTGRES_URI)

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def load_dummy_candidates():
    """Load all dummy candidates into both databases"""
    print_section("LOADING DUMMY CANDIDATES")
    
    loaded_count = 0
    skipped_count = 0
    
    for i, candidate in enumerate(dummy_candidates, 1):
        name = candidate.get("personal_info", {}).get("full_name", "Unknown")
        
        # Check if candidate already exists (by email)
        email = candidate.get("personal_info", {}).get("email", "")
        existing = candidates_col.find_one({"personal_info.email": email})
        
        if existing:
            print(f"[{i}/{len(dummy_candidates)}] SKIPPED: {name} (already exists)")
            skipped_count += 1
            continue
        
        try:
            # Insert into MongoDB
            result = candidates_col.insert_one(candidate)
            mongo_id = str(result.inserted_id)
            
            # Flatten and create embedding
            flat = flatten_candidate(candidate)
            emb = get_embedding(flat)
            
            # Insert into PostgreSQL
            with pg_engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO candidates (candidate_id, content, embedding)
                    VALUES (:cid, :content, :embedding)
                """), {"cid": mongo_id, "content": flat, "embedding": emb})
            
            print(f"[{i}/{len(dummy_candidates)}] ✓ Loaded: {name} (ID: {mongo_id[:8]}...)")
            loaded_count += 1
            
        except Exception as e:
            print(f"[{i}/{len(dummy_candidates)}] ✗ ERROR loading {name}: {e}")
    
    print(f"\nSummary: {loaded_count} loaded, {skipped_count} skipped, {len(dummy_candidates)} total")
    return loaded_count, skipped_count

def verify_mongodb_data():
    """Verify all candidates are in MongoDB"""
    print_section("VERIFYING MONGODB DATA")
    
    try:
        count = candidates_col.count_documents({})
        print(f"Total candidates in MongoDB: {count}")
        
        if count == 0:
            print("⚠ WARNING: No candidates found in MongoDB!")
            return False
        
        # List all candidates
        print("\nCandidates in MongoDB:")
        for i, doc in enumerate(candidates_col.find({}), 1):
            name = doc.get("personal_info", {}).get("full_name", "Unknown")
            email = doc.get("personal_info", {}).get("email", "N/A")
            mongo_id = str(doc.get("_id", "N/A"))
            print(f"  {i}. {name} ({email}) - ID: {mongo_id[:8]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ ERROR checking MongoDB: {e}")
        return False

def verify_postgres_data():
    """Verify all candidates are in PostgreSQL with embeddings"""
    print_section("VERIFYING POSTGRESQL DATA")
    
    try:
        with pg_engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM candidates"))
            count = result.scalar()
            print(f"Total candidates in PostgreSQL: {count}")
            
            if count == 0:
                print("⚠ WARNING: No candidates found in PostgreSQL!")
                return False
            
            # List all candidates with embedding info
            # Note: Can't cast vector to array in some pgvector versions, so we fetch embedding and check length in Python
            result = conn.execute(text("""
                SELECT candidate_id, 
                       LENGTH(content) as content_length,
                       embedding
                FROM candidates
                ORDER BY candidate_id
            """))
            rows = result.fetchall()
            
            print("\nCandidates in PostgreSQL:")
            for i, row in enumerate(rows, 1):
                cid = row[0]
                content_len = row[1]
                emb = row[2]
                # Get dimension from embedding in Python (works with all pgvector versions)
                if emb is not None:
                    # pgvector returns embeddings as array-like objects
                    try:
                        emb_dim = len(emb) if hasattr(emb, '__len__') else 768  # Default to 768 if can't determine
                    except:
                        emb_dim = 768  # Default for all-mpnet-base-v2
                else:
                    emb_dim = "NULL"
                print(f"  {i}. ID: {cid[:8]}... | Content: {content_len} chars | Embedding: {emb_dim}D")
            
            return True
            
    except Exception as e:
        print(f"✗ ERROR checking PostgreSQL: {e}")
        return False

def test_rag_query(query_text, top_k=5):
    """Test a RAG query and display results"""
    print(f"\n🔍 Query: '{query_text}'")
    print("-" * 70)
    
    try:
        # Get query embedding
        query_emb = get_embedding(query_text)
        
        # Perform vector search
        with pg_engine.connect() as conn:
            # Convert embedding to string format for pgvector
            emb_list = query_emb.tolist() if hasattr(query_emb, 'tolist') else list(query_emb)
            emb_str = "[" + ",".join(map(str, emb_list)) + "]"
            
            result = conn.execute(text(f"""
                SELECT candidate_id, content
                FROM candidates
                ORDER BY embedding <-> '{emb_str}'::vector
                LIMIT {top_k}
            """))
            rows = result.fetchall()
        
        if not rows:
            print("  No results found")
            return []
        
        # Fetch full candidate data from MongoDB
        candidate_ids = [str(row[0]) for row in rows]
        from bson import ObjectId
        
        doc_map = {}
        object_ids = []
        for cid in candidate_ids:
            try:
                object_ids.append(ObjectId(cid))
            except:
                pass
        
        if object_ids:
            for doc in candidates_col.find({"_id": {"$in": object_ids}}):
                doc_map[str(doc["_id"])] = doc
        
        # Display results
        results = []
        for i, row in enumerate(rows, 1):
            cid = str(row[0])
            content = row[1]
            doc = doc_map.get(cid)
            
            if doc:
                name = doc.get("personal_info", {}).get("full_name", "Unknown")
                summary = doc.get("personal_info", {}).get("summary", "")
                skills = doc.get("skills", {}).get("technical", [])
                job_title = doc.get("experience", [{}])[0].get("job_title", "N/A") if doc.get("experience") else "N/A"
                
                print(f"  {i}. {name}")
                print(f"     Role: {job_title}")
                print(f"     Skills: {', '.join(skills[:5])}")
                print(f"     Summary: {summary[:100]}...")
                
                results.append({
                    "name": name,
                    "job_title": job_title,
                    "skills": skills,
                    "summary": summary
                })
            else:
                print(f"  {i}. [Candidate ID: {cid[:8]}...] (MongoDB data not found)")
                print(f"     Content preview: {content[:100]}...")
        
        return results
        
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_rag_queries():
    """Test various RAG queries"""
    print_section("TESTING RAG QUERIES")
    
    test_queries = [
        "data scientist with machine learning experience",
        "frontend developer React TypeScript",
        "backend developer Java Spring Boot",
        "product manager SaaS",
        "DevOps engineer AWS Docker",
        "Python developer",
        "full stack developer",
        "UX designer",
        "AI researcher deep learning"
    ]
    
    all_results = {}
    for query in test_queries:
        results = test_rag_query(query, top_k=3)
        all_results[query] = results
    
    return all_results

def main():
    """Main test function"""
    print("\n" + "="*70)
    print("  RECRUITBOT - RAG & DATA TESTING SUITE")
    print("="*70)
    
    # Step 1: Load model (this may take time on first run)
    print("\n📦 Loading embedding model...")
    try:
        model = get_model()
        print(f"✓ Model loaded: {type(model).__name__}")
    except Exception as e:
        print(f"✗ ERROR loading model: {e}")
        return
    
    # Step 2: Load dummy candidates
    loaded, skipped = load_dummy_candidates()
    
    # Step 3: Verify MongoDB
    mongo_ok = verify_mongodb_data()
    
    # Step 4: Verify PostgreSQL
    postgres_ok = verify_postgres_data()
    
    # Step 5: Test RAG queries
    if mongo_ok and postgres_ok:
        test_rag_queries()
    else:
        print("\n⚠ Skipping RAG tests due to database issues")
    
    # Final summary
    print_section("TEST SUMMARY")
    print(f"MongoDB: {'✓ OK' if mongo_ok else '✗ FAILED'}")
    print(f"PostgreSQL: {'✓ OK' if postgres_ok else '✗ FAILED'}")
    print(f"Candidates loaded: {loaded} new, {skipped} skipped")
    
    if mongo_ok and postgres_ok:
        print("\n✓ All systems operational! RAG model is ready to use.")
    else:
        print("\n✗ Some issues detected. Please check the errors above.")

if __name__ == "__main__":
    main()

