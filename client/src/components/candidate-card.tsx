import { useState } from "react";
import { MapPin, Briefcase, Phone, Bookmark } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";
import type { Candidate } from "@shared/schema";

interface CandidateCardProps {
  candidate: Candidate;
}

export default function CandidateCard({ candidate }: CandidateCardProps) {
  const [isBookmarked, setIsBookmarked] = useState(false);

  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
  };

  const handleUnlockProfile = () => {
    // TODO: Implement profile unlock functionality
    alert(`Unlocking profile for ${candidate.name}`);
  };

  return (
    <Card className="bg-white hover:shadow-md transition-all duration-300">
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-4 flex-1">
            <Avatar className="w-16 h-16">
              <AvatarImage src={candidate.avatar || undefined} alt={candidate.name} />
              <AvatarFallback className="text-lg font-semibold">
                {candidate.name.split(' ').map(n => n[0]).join('')}
              </AvatarFallback>
            </Avatar>
            
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-1">
                <h3 className="text-lg font-semibold text-foreground">
                  {candidate.name}
                </h3>
                {candidate.matchScore && candidate.matchScore >= 90 && (
                  <Badge className="bg-green-100 text-green-800 hover:bg-green-100">
                    TOP
                  </Badge>
                )}
              </div>
              
              <p className="text-muted-foreground mb-3">{candidate.title}</p>
              
              <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mb-4">
                <div className="flex items-center space-x-1">
                  <MapPin className="h-4 w-4" />
                  <span>{candidate.location}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Briefcase className="h-4 w-4" />
                  <span>{candidate.experience}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Phone className="h-4 w-4" />
                  <span>{candidate.phone}</span>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2 mb-4">
                {candidate.skills.map((skill) => (
                  <Badge key={skill} variant="secondary" className="text-xs">
                    {skill}
                  </Badge>
                ))}
              </div>
              
              <Button 
                onClick={handleUnlockProfile}
                className="bg-primary hover:bg-primary/90"
              >
                Unlock Full Profile & Resume
              </Button>
            </div>
          </div>
          
          <div className="flex flex-col items-end space-y-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleBookmark}
              className={isBookmarked ? "text-primary" : "text-muted-foreground hover:text-foreground"}
            >
              <Bookmark className={`h-5 w-5 ${isBookmarked ? "fill-current" : ""}`} />
            </Button>
            {candidate.matchScore && (
              <div className="flex items-center space-x-1">
                <span className="text-green-600 font-semibold">
                  {candidate.matchScore}%
                </span>
                <span className="text-xs text-muted-foreground">match</span>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
