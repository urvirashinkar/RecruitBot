import { Edit, Search, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useQuery } from "@tanstack/react-query";
import type { ChatSession } from "@shared/schema";
import { formatDistanceToNow } from "date-fns";

interface SidebarProps {
  onNewChat: () => void;
  onSessionSelect: (session: ChatSession) => void;
  currentSession: ChatSession | null;
}

export default function Sidebar({ onNewChat, onSessionSelect, currentSession }: SidebarProps) {
  const { data: sessions = [] } = useQuery<ChatSession[]>({
    queryKey: ["/api/chat/sessions"],
  });

  return (
    <aside className="w-full md:w-64 bg-white border-r border-gray-200 flex flex-col h-48 md:h-full">
      <div className="p-4 space-y-3">
        <Button
          onClick={onNewChat}
          className="w-full justify-start space-x-3 bg-accent hover:bg-gray-200 text-foreground"
          variant="secondary"
        >
          <Edit className="h-4 w-4" />
          <span>New Chat</span>
        </Button>
        
        <Button
          variant="ghost"
          className="w-full justify-start space-x-3 text-muted-foreground hover:text-foreground"
        >
          <Search className="h-4 w-4" />
          <span>Search Chat</span>
        </Button>
      </div>
      
      <div className="flex-1 overflow-hidden p-4">
        <h3 className="text-sm font-medium text-muted-foreground mb-3">Recent Searches</h3>
        <ScrollArea className="h-full">
          <div className="space-y-2">
            {sessions.map((session) => (
              <div
                key={session.id}
                className={`p-3 rounded-lg cursor-pointer transition-colors ${
                  currentSession?.id === session.id
                    ? "bg-accent"
                    : "hover:bg-accent"
                }`}
                onClick={() => onSessionSelect(session)}
              >
                <p className="text-sm font-medium text-foreground truncate">
                  {session.query}
                </p>
                <div className="flex items-center space-x-2 mt-1">
                  <p className="text-xs text-muted-foreground">
                    {session.resultCount} results
                  </p>
                  <span className="text-xs text-muted-foreground">•</span>
                  <p className="text-xs text-muted-foreground">
                    {session.createdAt 
                      ? formatDistanceToNow(new Date(session.createdAt), { addSuffix: true })
                      : "Unknown time"
                    }
                  </p>
                </div>
              </div>
            ))}
            {sessions.length === 0 && (
              <div className="text-center py-8">
                <Clock className="h-8 w-8 mx-auto text-muted-foreground mb-2" />
                <p className="text-sm text-muted-foreground">No chat history yet</p>
              </div>
            )}
          </div>
        </ScrollArea>
      </div>
    </aside>
  );
}
