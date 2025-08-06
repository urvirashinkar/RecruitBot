import { Bell, Search, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 h-20">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <h1 className="text-2xl font-bold text-primary">PreHire</h1>
          <nav className="hidden md:flex space-x-6">
            <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
              About Us
            </a>
            <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
              Clients
            </a>
            <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
              Pricing
            </a>
            <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
              FAQ
            </a>
            <a href="#" className="text-muted-foreground hover:text-foreground transition-colors">
              Contact Us
            </a>
          </nav>
        </div>
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon">
            <Search className="h-5 w-5" />
          </Button>
          <Avatar className="h-8 w-8">
            <AvatarImage src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=32&h=32" />
            <AvatarFallback>
              <User className="h-4 w-4" />
            </AvatarFallback>
          </Avatar>
        </div>
      </div>
    </header>
  );
}
