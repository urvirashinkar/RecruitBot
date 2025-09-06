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
      <CardContent className="p-4 md:p-6">
        <div className="flex flex-col sm:flex-row items-start justify-between gap-4">
          <div className="flex items-start space-x-4 flex-1 w-full">
            <Avatar className="w-12 h-12 md:w-16 md:h-16 flex-shrink-0">
              <AvatarImage src={candidate.avatar || undefined} alt={candidate.name} />
              <AvatarFallback className="text-sm md:text-lg font-semibold">
                {candidate.name.split(' ').map(n => n[0]).join('')}
              </AvatarFallback>
            </Avatar>
            
            <div className="flex-1 min-w-0">
              <div className="flex flex-wrap items-center gap-2 mb-1">
                <h3 className="text-base md:text-lg font-semibold text-foreground truncate">
                  {candidate.name}
                </h3>
                {candidate.matchScore && candidate.matchScore >= 90 && (
                  <Badge className="bg-green-100 text-green-800 hover:bg-green-100 text-xs">
                    TOP
                  </Badge>
                )}
              </div>
              
              <p className="text-sm text-muted-foreground mb-3 truncate">{candidate.title}</p>
              
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs md:text-sm text-muted-foreground mb-3">
                <div className="flex items-center space-x-1">
                  <MapPin className="h-3 w-3 md:h-4 md:w-4 flex-shrink-0" />
                  <span className="truncate">{candidate.location}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Briefcase className="h-3 w-3 md:h-4 md:w-4 flex-shrink-0" />
                  <span className="truncate">{candidate.experience}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Phone className="h-3 w-3 md:h-4 md:w-4 flex-shrink-0" />
                  <span className="truncate">{candidate.phone}</span>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-1 md:gap-2 mb-4">
                {candidate.skills.slice(0, 4).map((skill) => (
                  <Badge key={skill} variant="secondary" className="text-xs">
                    {skill}
                  </Badge>
                ))}
                {candidate.skills.length > 4 && (
                  <Badge variant="outline" className="text-xs">
                    +{candidate.skills.length - 4} more
                  </Badge>
                )}
              </div>
              
              <Button 
                onClick={handleUnlockProfile}
                className="bg-primary hover:bg-primary/90 w-full sm:w-auto text-sm"
                size="sm"
              >
                Unlock Full Profile & Resume
              </Button>
            </div>
          </div>
          
          <div className="flex sm:flex-col items-center sm:items-end space-x-2 sm:space-x-0 sm:space-y-2 w-full sm:w-auto justify-between sm:justify-start">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleBookmark}
              className={`${isBookmarked ? "text-primary" : "text-muted-foreground hover:text-foreground"} h-8 w-8`}
            >
              <Bookmark className={`h-4 w-4 ${isBookmarked ? "fill-current" : ""}`} />
            </Button>
            {candidate.matchScore && (
              <div className="flex items-center space-x-1">
                <span className="text-green-600 font-semibold text-sm md:text-base">
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
