import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { z } from "zod";

// Hugging Face API configuration
const HF_API_KEY = process.env.HUGGING_FACE_API_KEY || process.env.HF_API_KEY || "";
const HF_API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2";

// Schemas for request validation
const searchQuerySchema = z.object({
  query: z.string().min(1),
});

const createSessionSchema = z.object({
  query: z.string().min(1),
  resultCount: z.number().min(0),
  results: z.array(z.string()),
});

const createMessageSchema = z.object({
  sessionId: z.string().optional(),
  type: z.enum(['user', 'bot']),
  content: z.string().min(1),
});

// Helper function to calculate cosine similarity
function cosineSimilarity(vecA: number[], vecB: number[]): number {
  const dotProduct = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);
  const magnitudeA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
  const magnitudeB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

// Helper function to get embeddings from Hugging Face
async function getEmbeddings(text: string): Promise<number[] | null> {
  if (!HF_API_KEY) {
    console.warn("No Hugging Face API key provided, using fallback similarity");
    return null;
  }

  try {
    const response = await fetch(HF_API_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${HF_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        inputs: text,
        options: { wait_for_model: true }
      }),
    });

    if (!response.ok) {
      throw new Error(`Hugging Face API error: ${response.status}`);
    }

    const embeddings = await response.json();
    return Array.isArray(embeddings) && Array.isArray(embeddings[0]) ? embeddings[0] : embeddings;
  } catch (error) {
    console.error("Error getting embeddings:", error);
    return null;
  }
}

// Fallback similarity calculation using keyword matching
function calculateKeywordSimilarity(query: string, candidate: any): number {
  const queryWords = query.toLowerCase().split(' ');
  const candidateText = `${candidate.title} ${candidate.skills.join(' ')} ${candidate.resume}`.toLowerCase();
  
  let matches = 0;
  queryWords.forEach(word => {
    if (candidateText.includes(word)) {
      matches++;
    }
  });
  
  return Math.min((matches / queryWords.length) * 100, 100);
}

export async function registerRoutes(app: Express): Promise<Server> {
  
  // Get all candidates
  app.get("/api/candidates", async (req, res) => {
    try {
      const candidates = await storage.getCandidates();
      res.json(candidates);
    } catch (error) {
      console.error("Error fetching candidates:", error);
      res.status(500).json({ error: "Failed to fetch candidates" });
    }
  });

  // Search candidates with AI-powered matching
  app.post("/api/candidates/search", async (req, res) => {
    try {
      const { query } = searchQuerySchema.parse(req.body);
      
      // Get all candidates
      const allCandidates = await storage.getCandidates();
      
      // Try to get embeddings for the query
      const queryEmbeddings = await getEmbeddings(query);
      
      let rankedCandidates;
      
      if (queryEmbeddings) {
        // Use AI embeddings for similarity calculation
        const candidatesWithScores = await Promise.all(
          allCandidates.map(async (candidate) => {
            const candidateText = `${candidate.title} ${candidate.skills.join(' ')} ${candidate.resume}`;
            const candidateEmbeddings = await getEmbeddings(candidateText);
            
            let similarity = 0;
            if (candidateEmbeddings) {
              similarity = cosineSimilarity(queryEmbeddings, candidateEmbeddings);
            } else {
              // Fallback to keyword matching
              similarity = calculateKeywordSimilarity(query, candidate) / 100;
            }
            
            return {
              ...candidate,
              matchScore: Math.round(similarity * 100)
            };
          })
        );
        
        rankedCandidates = candidatesWithScores
          .filter(candidate => candidate.matchScore > 20) // Only show candidates with >20% match
          .sort((a, b) => b.matchScore - a.matchScore)
          .slice(0, 10); // Top 10 results
      } else {
        // Fallback to keyword-based search
        rankedCandidates = allCandidates
          .map(candidate => ({
            ...candidate,
            matchScore: Math.round(calculateKeywordSimilarity(query, candidate))
          }))
          .filter(candidate => candidate.matchScore > 20)
          .sort((a, b) => b.matchScore - a.matchScore)
          .slice(0, 10);
      }
      
      res.json({
        candidates: rankedCandidates,
        total: rankedCandidates.length,
        query
      });
    } catch (error) {
      console.error("Error searching candidates:", error);
      res.status(500).json({ error: "Failed to search candidates" });
    }
  });

  // Get chat sessions (history)
  app.get("/api/chat/sessions", async (req, res) => {
    try {
      const sessions = await storage.getChatSessions();
      res.json(sessions);
    } catch (error) {
      console.error("Error fetching chat sessions:", error);
      res.status(500).json({ error: "Failed to fetch chat sessions" });
    }
  });

  // Create a new chat session
  app.post("/api/chat/sessions", async (req, res) => {
    try {
      const sessionData = createSessionSchema.parse(req.body);
      const session = await storage.createChatSession(sessionData);
      res.json(session);
    } catch (error) {
      console.error("Error creating chat session:", error);
      res.status(500).json({ error: "Failed to create chat session" });
    }
  });

  // Get messages for a session
  app.get("/api/chat/sessions/:sessionId/messages", async (req, res) => {
    try {
      const { sessionId } = req.params;
      const messages = await storage.getMessagesBySessionId(sessionId);
      res.json(messages);
    } catch (error) {
      console.error("Error fetching messages:", error);
      res.status(500).json({ error: "Failed to fetch messages" });
    }
  });

  // Create a new message
  app.post("/api/chat/messages", async (req, res) => {
    try {
      const messageData = createMessageSchema.parse(req.body);
      const message = await storage.createMessage(messageData);
      res.json(message);
    } catch (error) {
      console.error("Error creating message:", error);
      res.status(500).json({ error: "Failed to create message" });
    }
  });

  // Get candidate by ID
  app.get("/api/candidates/:id", async (req, res) => {
    try {
      const { id } = req.params;
      const candidate = await storage.getCandidateById(id);
      
      if (!candidate) {
        return res.status(404).json({ error: "Candidate not found" });
      }
      
      res.json(candidate);
    } catch (error) {
      console.error("Error fetching candidate:", error);
      res.status(500).json({ error: "Failed to fetch candidate" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
