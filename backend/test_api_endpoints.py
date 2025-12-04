#!/usr/bin/env python3
"""
Test script for FastAPI endpoints
Tests the RAG model through the API endpoints
"""

import requests
import json
import sys
from typing import List, Dict

# Configuration
API_BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_health():
    """Test the health endpoint"""
    print_section("TESTING HEALTH ENDPOINT")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed")
            print(f"  Status: {data.get('status')}")
            print(f"  Model loaded: {data.get('model_loaded')}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to {API_BASE_URL}")
        print("  Make sure the FastAPI server is running: uvicorn main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_get_candidate(candidate_id: str):
    """Test getting a candidate by ID"""
    try:
        response = requests.get(f"{API_BASE_URL}/candidates/{candidate_id}")
        if response.status_code == 200:
            data = response.json()
            name = data.get("personal_info", {}).get("full_name", "Unknown")
            print(f"✓ Found candidate: {name}")
            return data
        else:
            print(f"✗ Candidate not found: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def test_rag_query(query: str, top_k: int = 5):
    """Test the RAG query endpoint"""
    print(f"\n🔍 Testing RAG Query: '{query}'")
    print("-" * 70)
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/chatbot/query",
            params={"query": query, "top_k": top_k}
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                print("  No results found")
                return []
            
            print(f"  Found {len(results)} results:\n")
            for i, candidate in enumerate(results, 1):
                name = candidate.get("name", "Unknown")
                summary = candidate.get("summary", "")[:100]
                skills = candidate.get("skills", [])
                experience = candidate.get("experience", [])
                
                print(f"  {i}. {name}")
                if experience:
                    exp_str = ", ".join([f"{e.get('job_title', 'N/A')} at {e.get('company', 'N/A')}" 
                                       for e in experience[:2]])
                    print(f"     Experience: {exp_str}")
                if skills:
                    print(f"     Skills: {', '.join(skills[:5])}")
                print(f"     Summary: {summary}...")
                print()
            
            return results
        else:
            print(f"✗ Query failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return []

def test_all_queries():
    """Test multiple RAG queries"""
    print_section("TESTING RAG QUERIES")
    
    test_queries = [
        ("data scientist with machine learning experience", 3),
        ("frontend developer React TypeScript", 3),
        ("backend developer Java Spring Boot", 3),
        ("product manager SaaS", 3),
        ("DevOps engineer AWS Docker", 3),
        ("Python developer", 3),
        ("full stack developer", 3),
        ("UX designer", 3),
        ("AI researcher deep learning", 3)
    ]
    
    all_results = {}
    for query, top_k in test_queries:
        results = test_rag_query(query, top_k)
        all_results[query] = results
    
    return all_results

def list_all_candidates():
    """List all candidates (requires iterating through MongoDB)"""
    print_section("LISTING ALL CANDIDATES")
    print("Note: This requires direct MongoDB access or a GET /candidates endpoint")
    print("For now, use the test_rag_and_data.py script to list candidates")

def main():
    """Main test function"""
    print("\n" + "="*70)
    print("  RECRUITBOT - API ENDPOINT TESTING")
    print("="*70)
    
    # Test health
    if not test_health():
        print("\n⚠ Cannot proceed without a healthy API connection")
        print("  Start the server with: cd backend && uvicorn main:app --reload --port 8000")
        return
    
    # Test RAG queries
    test_all_queries()
    
    print_section("TEST COMPLETE")
    print("✓ API endpoint tests finished")
    print("\nTo test with specific candidate IDs, use:")
    print("  python test_api_endpoints.py <candidate_id>")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test specific candidate
        candidate_id = sys.argv[1]
        print_section(f"TESTING CANDIDATE: {candidate_id}")
        test_get_candidate(candidate_id)
    else:
        main()

