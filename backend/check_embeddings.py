#!/usr/bin/env python3
"""
Script to check embeddings in NeonDB (PostgreSQL with pgvector)
Shows how many embeddings exist, their dimensions, and sample data
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

POSTGRES_URI = os.getenv("POSTGRES_URI")

if not POSTGRES_URI:
    print("ERROR: POSTGRES_URI must be set in .env file")
    exit(1)

pg_engine = create_engine(POSTGRES_URI)

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def check_table_exists():
    """Check if the candidates table exists"""
    try:
        with pg_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'candidates'
                );
            """))
            exists = result.scalar()
            return exists
    except Exception as e:
        print(f"Error checking table: {e}")
        return False

def get_embedding_stats():
    """Get statistics about embeddings"""
    print_section("EMBEDDING STATISTICS")
    
    try:
        with pg_engine.connect() as conn:
            # Count total records
            count_result = conn.execute(text("SELECT COUNT(*) FROM candidates"))
            total_count = count_result.scalar()
            print(f"Total candidates with embeddings: {total_count}")
            
            if total_count == 0:
                print("\n⚠ No embeddings found in database!")
                print("Run: python dummy_candidate.py or python test_rag_and_data.py")
                return
            
            # Get embedding dimension - fetch embedding and check length in Python
            # (Can't cast vector to array in some pgvector versions like NeonDB)
            dim_result = conn.execute(text("""
                SELECT embedding 
                FROM candidates 
                LIMIT 1
            """))
            dim_row = dim_result.fetchone()
            if dim_row and dim_row[0] is not None:
                emb = dim_row[0]
                try:
                    embedding_dim = len(emb) if hasattr(emb, '__len__') else 768
                except:
                    embedding_dim = 768  # Default for all-mpnet-base-v2
            else:
                embedding_dim = None
            
            if embedding_dim:
                print(f"Embedding dimension: {embedding_dim}D")
            else:
                print("⚠ Could not determine embedding dimension")
            
            # Check for NULL embeddings
            null_result = conn.execute(text("""
                SELECT COUNT(*) FROM candidates WHERE embedding IS NULL
            """))
            null_count = null_result.scalar()
            
            if null_count > 0:
                print(f"⚠ Warning: {null_count} records have NULL embeddings")
            else:
                print("✓ All records have embeddings")
            
            return total_count, embedding_dim
            
    except Exception as e:
        print(f"✗ Error getting stats: {e}")
        return None, None

def list_all_embeddings(limit=10):
    """List all embeddings with basic info"""
    print_section(f"LISTING EMBEDDINGS (showing first {limit})")
    
    try:
        with pg_engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT 
                    candidate_id,
                    LENGTH(content) as content_length,
                    embedding,
                    LEFT(content, 100) as content_preview
                FROM candidates
                ORDER BY candidate_id
                LIMIT {limit}
            """))
            rows = result.fetchall()
            
            if not rows:
                print("No embeddings found")
                return
            
            print(f"{'ID':<30} {'Content Len':<15} {'Dim':<10} {'Preview'}")
            print("-" * 80)
            for row in rows:
                cid = str(row[0])[:28] + "..." if len(str(row[0])) > 28 else str(row[0])
                content_len = row[1] or 0
                emb = row[2]
                preview = (row[3] or "")[:40] + "..." if row[3] and len(row[3]) > 40 else (row[3] or "")
                # Get dimension from embedding in Python
                if emb is not None:
                    try:
                        dim = len(emb) if hasattr(emb, '__len__') else 768
                    except:
                        dim = 768
                else:
                    dim = "NULL"
                print(f"{cid:<30} {content_len:<15} {dim:<10} {preview}")
            
            if len(rows) == limit:
                print(f"\n... (showing first {limit} of total)")
                
    except Exception as e:
        print(f"✗ Error listing embeddings: {e}")

def show_embedding_details(candidate_id=None):
    """Show detailed information about a specific embedding"""
    print_section("EMBEDDING DETAILS")
    
    try:
        with pg_engine.connect() as conn:
            if candidate_id:
                query = text("""
                    SELECT 
                        candidate_id,
                        content,
                        embedding
                    FROM candidates
                    WHERE candidate_id = :cid
                """)
                result = conn.execute(query, {"cid": candidate_id})
            else:
                # Get first candidate
                query = text("""
                    SELECT 
                        candidate_id,
                        content,
                        embedding
                    FROM candidates
                    LIMIT 1
                """)
                result = conn.execute(query)
            
            row = result.fetchone()
            
            if not row:
                print("No embedding found")
                return
            
            cid, content, emb = row
            
            # Get dimension and preview from embedding in Python
            if emb is not None:
                try:
                    dim = len(emb) if hasattr(emb, '__len__') else 768
                    # Get first 10 values for preview
                    if hasattr(emb, '__getitem__'):
                        preview = [emb[i] for i in range(min(10, len(emb)))]
                    else:
                        preview = list(emb)[:10] if hasattr(emb, '__iter__') else []
                except:
                    dim = 768
                    preview = []
            else:
                dim = "NULL"
                preview = []
            
            print(f"Candidate ID: {cid}")
            print(f"Embedding Dimension: {dim}D")
            print(f"\nContent Preview:")
            print("-" * 70)
            print(content[:500] + "..." if len(content) > 500 else content)
            print("-" * 70)
            if preview:
                print(f"\nEmbedding Vector (first 10 values):")
                print(f"[{', '.join(map(str, preview[:10]))}...]")
                print(f"\nTotal embedding values: {dim}")
            else:
                print(f"\nEmbedding: NULL or could not extract")
            
    except Exception as e:
        print(f"✗ Error showing details: {e}")

def test_vector_similarity():
    """Test vector similarity search"""
    print_section("TESTING VECTOR SIMILARITY")
    
    try:
        with pg_engine.connect() as conn:
            # Get two random embeddings
            result = conn.execute(text("""
                SELECT candidate_id, embedding
                FROM candidates
                LIMIT 2
            """))
            rows = result.fetchall()
            
            if len(rows) < 2:
                print("Need at least 2 embeddings to test similarity")
                return
            
            cid1, emb1 = rows[0]
            cid2, emb2 = rows[1]
            
            # Calculate cosine distance
            result = conn.execute(text("""
                SELECT 
                    :emb1::vector <-> :emb2::vector as cosine_distance,
                    1 - (:emb1::vector <-> :emb2::vector) as cosine_similarity
            """), {
                "emb1": str(list(emb1)),
                "emb2": str(list(emb2))
            })
            
            row = result.fetchone()
            if row:
                distance, similarity = row
                print(f"Comparing embeddings:")
                print(f"  Candidate 1: {cid1[:20]}...")
                print(f"  Candidate 2: {cid2[:20]}...")
                print(f"\nCosine Distance: {distance:.6f}")
                print(f"Cosine Similarity: {similarity:.6f}")
                print(f"\nNote: Lower distance = more similar")
                print(f"      Higher similarity = more similar")
            
    except Exception as e:
        print(f"✗ Error testing similarity: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    print("\n" + "="*70)
    print("  NEONDB EMBEDDING CHECKER")
    print("="*70)
    
    # Check connection
    try:
        with pg_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Connected to NeonDB")
    except Exception as e:
        print(f"✗ Cannot connect to NeonDB: {e}")
        print("\nCheck your POSTGRES_URI in .env file")
        return
    
    # Check if table exists
    if not check_table_exists():
        print("\n⚠ Table 'candidates' does not exist!")
        print("Create it with:")
        print("""
CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    candidate_id TEXT,
    content TEXT,
    embedding VECTOR(768)
);
        """)
        return
    
    print("✓ Table 'candidates' exists")
    
    # Get stats
    total_count, embedding_dim = get_embedding_stats()
    
    if total_count and total_count > 0:
        # List embeddings
        list_all_embeddings(limit=10)
        
        # Show details
        show_embedding_details()
        
        # Test similarity
        if total_count >= 2:
            test_vector_similarity()
    
    print_section("SUMMARY")
    if total_count:
        print(f"✓ Found {total_count} embeddings")
        if embedding_dim:
            print(f"✓ Embedding dimension: {embedding_dim}D")
        print("\nTo view a specific embedding, use:")
        print("  python check_embeddings.py <candidate_id>")
    else:
        print("⚠ No embeddings found")
        print("Load data with: python dummy_candidate.py")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        candidate_id = sys.argv[1]
        print_section(f"EMBEDDING DETAILS FOR: {candidate_id}")
        show_embedding_details(candidate_id)
    else:
        main()

