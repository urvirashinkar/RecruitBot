import { type Candidate, type InsertCandidate, type ChatSession, type InsertChatSession, type Message, type InsertMessage } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  // Candidate methods
  getCandidates(): Promise<Candidate[]>;
  getCandidateById(id: string): Promise<Candidate | undefined>;
  createCandidate(candidate: InsertCandidate): Promise<Candidate>;
  searchCandidates(query: string): Promise<Candidate[]>;
  
  // Chat session methods
  getChatSessions(): Promise<ChatSession[]>;
  getChatSessionById(id: string): Promise<ChatSession | undefined>;
  createChatSession(session: InsertChatSession): Promise<ChatSession>;
  
  // Message methods
  getMessagesBySessionId(sessionId: string): Promise<Message[]>;
  createMessage(message: InsertMessage): Promise<Message>;
}

export class MemStorage implements IStorage {
  private candidates: Map<string, Candidate>;
  private chatSessions: Map<string, ChatSession>;
  private messages: Map<string, Message>;

  constructor() {
    this.candidates = new Map();
    this.chatSessions = new Map();
    this.messages = new Map();
    
    // Initialize with sample candidate data
    this.initializeCandidates();
  }

  private initializeCandidates() {
    const sampleCandidates: InsertCandidate[] = [
      {
        name: "Ananya Mehra",
        title: "Senior Java Developer",
        location: "Pune",
        experience: "5 years",
        phone: "+91 63547XXXX",
        email: "ananya.mehra@email.com",
        skills: ["Java", "Spring Boot", "Microservices", "AWS", "Hibernate", "REST APIs"],
        resume: "Experienced Java developer with 5 years in enterprise applications. Proficient in Spring Boot, microservices architecture, and cloud platforms. Led multiple projects involving scalable backend systems.",
        matchScore: 95,
        avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b890?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&h=150"
      },
      {
        name: "Rahul Sharma",
        title: "Java Full Stack Developer",
        location: "Bangalore",
        experience: "6 years",
        phone: "+91 98547XXXX",
        email: "rahul.sharma@email.com",
        skills: ["Java", "React", "Node.js", "MongoDB", "Spring", "JavaScript"],
        resume: "Full-stack developer specializing in Java backend and React frontend. 6 years of experience building end-to-end applications. Strong knowledge of modern web technologies and database design.",
        matchScore: 92,
        avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&h=150"
      },
      {
        name: "Priya Patel",
        title: "Backend Java Developer",
        location: "Mumbai",
        experience: "4 years",
        phone: "+91 88547XXXX",
        email: "priya.patel@email.com",
        skills: ["Java", "Spring", "MySQL", "Docker", "Kubernetes", "Jenkins"],
        resume: "Backend specialist with strong Java and Spring expertise. Experience with containerization and CI/CD pipelines. Focused on building robust, scalable server-side applications.",
        matchScore: 88,
        avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&h=150"
      },
      {
        name: "Arjun Singh",
        title: "Java Software Engineer",
        location: "Hyderabad",
        experience: "5 years",
        phone: "+91 77547XXXX",
        email: "arjun.singh@email.com",
        skills: ["Java", "Hibernate", "REST APIs", "Jenkins", "Maven", "Git"],
        resume: "Software engineer with extensive Java development experience. Proficient in ORM frameworks and API development. Strong background in software engineering practices and version control.",
        matchScore: 85,
        avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&h=150"
      },
      {
        name: "Sneha Reddy",
        title: "Java Developer",
        location: "Chennai",
        experience: "3 years",
        phone: "+91 99547XXXX",
        email: "sneha.reddy@email.com",
        skills: ["Java", "Spring Framework", "PostgreSQL", "JUnit", "Maven"],
        resume: "Java developer with 3 years of experience in web application development. Strong foundation in Spring framework and database technologies. Experience with unit testing and build tools.",
        matchScore: 82,
        avatar: "https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-4.0.3&auto=format&fit=crop&w=150&h=150"
      }
    ];

    sampleCandidates.forEach(candidate => {
      this.createCandidate(candidate);
    });
  }

  async getCandidates(): Promise<Candidate[]> {
    return Array.from(this.candidates.values());
  }

  async getCandidateById(id: string): Promise<Candidate | undefined> {
    return this.candidates.get(id);
  }

  async createCandidate(insertCandidate: InsertCandidate): Promise<Candidate> {
    const id = randomUUID();
    const candidate: Candidate = {
      ...insertCandidate,
      id,
      createdAt: new Date(),
      matchScore: insertCandidate.matchScore || null,
      avatar: insertCandidate.avatar || null,
    };
    this.candidates.set(id, candidate);
    return candidate;
  }

  async searchCandidates(query: string): Promise<Candidate[]> {
    const queryLower = query.toLowerCase();
    const candidates = Array.from(this.candidates.values());
    
    return candidates.filter(candidate => {
      const titleMatch = candidate.title.toLowerCase().includes(queryLower);
      const skillsMatch = candidate.skills.some(skill => 
        skill.toLowerCase().includes(queryLower)
      );
      const resumeMatch = candidate.resume.toLowerCase().includes(queryLower);
      const locationMatch = candidate.location.toLowerCase().includes(queryLower);
      
      return titleMatch || skillsMatch || resumeMatch || locationMatch;
    }).sort((a, b) => (b.matchScore || 0) - (a.matchScore || 0));
  }

  async getChatSessions(): Promise<ChatSession[]> {
    return Array.from(this.chatSessions.values()).sort(
      (a, b) => (b.createdAt?.getTime() || 0) - (a.createdAt?.getTime() || 0)
    );
  }

  async getChatSessionById(id: string): Promise<ChatSession | undefined> {
    return this.chatSessions.get(id);
  }

  async createChatSession(insertSession: InsertChatSession): Promise<ChatSession> {
    const id = randomUUID();
    const session: ChatSession = {
      ...insertSession,
      id,
      createdAt: new Date(),
    };
    this.chatSessions.set(id, session);
    return session;
  }

  async getMessagesBySessionId(sessionId: string): Promise<Message[]> {
    return Array.from(this.messages.values())
      .filter(message => message.sessionId === sessionId)
      .sort((a, b) => (a.createdAt?.getTime() || 0) - (b.createdAt?.getTime() || 0));
  }

  async createMessage(insertMessage: InsertMessage): Promise<Message> {
    const id = randomUUID();
    const message: Message = {
      ...insertMessage,
      id,
      createdAt: new Date(),
      sessionId: insertMessage.sessionId || null,
    };
    this.messages.set(id, message);
    return message;
  }
}

export const storage = new MemStorage();
