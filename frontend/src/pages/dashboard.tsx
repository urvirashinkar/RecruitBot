import { useState } from "react";
import Header from "@/components/header";
import Sidebar from "@/components/sidebar";
import ChatInterface from "@/components/chat-interface";
import type { ChatSession } from "@shared/schema";

export default function Dashboard() {
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);

  const handleNewChat = () => {
    setCurrentSession(null);
  };

  const handleSessionSelect = (session: ChatSession) => {
    setCurrentSession(session);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="flex flex-col md:flex-row h-[calc(100vh-80px)]">
        <Sidebar 
          onNewChat={handleNewChat}
          onSessionSelect={handleSessionSelect}
          currentSession={currentSession}
        />
        <ChatInterface 
          currentSession={currentSession}
          onSessionCreated={setCurrentSession}
        />
      </div>
    </div>
  );
}
