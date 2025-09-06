import { useState } from "react";
import { Send, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import CandidateCard from "./candidate-card";
import type { ChatSession, Candidate } from "@shared/schema";

interface SearchResponse {
  candidates: Candidate[];
  total: number;
  query: string;
}

interface ChatInterfaceProps {
  currentSession: ChatSession | null;
  onSessionCreated: (session: ChatSession) => void;
}

interface Message {
  id: string;
  type: "user" | "bot";
  content: string;
  timestamp: Date;
}

export default function ChatInterface({ currentSession, onSessionCreated }: ChatInterfaceProps) {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const queryClient = useQueryClient();

  const searchMutation = useMutation({
    mutationFn: async (searchQuery: string) => {
      const response = await apiRequest("POST", "/api/candidates/search", { query: searchQuery });
      return response.json() as Promise<SearchResponse>;
    },
    onSuccess: async (data) => {
      // Add bot response message
      const botMessage: Message = {
        id: Date.now().toString() + "_bot",
        type: "bot",
        content: `I found ${data.total} potential matches for your requirements. Here are the top candidates:`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMessage]);
      
      // Set candidates
      setCandidates(data.candidates);
      
      // Create chat session
      try {
        const sessionResponse = await apiRequest("POST", "/api/chat/sessions", {
          query: data.query,
          resultCount: data.total,
          results: data.candidates.map(c => c.id),
        });
        const newSession = await sessionResponse.json();
        onSessionCreated(newSession);
        queryClient.invalidateQueries({ queryKey: ["/api/chat/sessions"] });
      } catch (error) {
        console.error("Error creating session:", error);
      }
      
      setIsLoading(false);
    },
    onError: (error) => {
      console.error("Search error:", error);
      const errorMessage: Message = {
        id: Date.now().toString() + "_error",
        type: "bot",
        content: "I'm sorry, there was an error processing your request. Please try again.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
    },
  });

  const handleSendMessage = () => {
    if (!query.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString() + "_user",
      type: "user",
      content: query,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    
    // Start search
    setIsLoading(true);
    searchMutation.mutate(query);
    setQuery("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const hasContent = messages.length > 0 || candidates.length > 0;

  return (
    <main className="flex-1 flex flex-col bg-accent">
      <ScrollArea className="flex-1 p-6">
        <div className="max-w-4xl mx-auto">
          {!hasContent && (
            <div className="text-center py-10 md:py-20">
              <h2 className="text-2xl md:text-3xl font-bold text-foreground mb-4">
                Candidate Smart Search
              </h2>
              <p className="text-muted-foreground mb-8 px-4">
                Type your requirements and we'll narrow down the best profiles for you
              </p>
            </div>
          )}

          {/* Messages */}
          <div className="space-y-6 mb-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-3 rounded-xl ${
                    message.type === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-white text-foreground border border-border"
                  }`}
                >
                  <p className="text-sm">{message.content}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Loading State */}
          {isLoading && (
            <div className="text-center py-4">
              <div className="inline-flex items-center space-x-2 text-primary">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-sm">Analyzing requirements and searching candidates...</span>
              </div>
            </div>
          )}

          {/* Results */}
          {candidates.length > 0 && (
            <div className="space-y-4">
              <p className="text-foreground font-medium">
                We found {candidates.length} potential matches for your query.
              </p>
              {candidates.map((candidate) => (
                <CandidateCard key={candidate.id} candidate={candidate} />
              ))}
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input Area */}
      <div className="border-t border-border bg-white p-6">
        <div className="max-w-4xl mx-auto">
          <div className="relative">
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your requirements and we'll narrow down the best profiles for you"
              className="pr-12 py-4 rounded-xl"
              disabled={isLoading}
            />
            <Button
              size="icon"
              onClick={handleSendMessage}
              disabled={!query.trim() || isLoading}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 h-8 w-8"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </main>
  );
}
