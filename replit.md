# Overview

PreHire is a modern AI-powered candidate search and recruitment platform built with React and Express. The application allows recruiters to search for candidates using natural language queries and provides an intelligent chat interface for finding the best matches. The system features real-time candidate matching with semantic search capabilities, chat session management, and a clean, responsive user interface built with shadcn/ui components.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The frontend is built with React and TypeScript using a modern component-based architecture:

- **Framework**: React 18 with TypeScript for type safety and better developer experience
- **Routing**: Wouter for lightweight client-side routing
- **State Management**: TanStack React Query for server state management and caching
- **UI Components**: shadcn/ui component library built on Radix UI primitives for accessibility and consistency
- **Styling**: Tailwind CSS with CSS variables for theming support
- **Build Tool**: Vite for fast development and optimized production builds

## Backend Architecture
The backend follows a RESTful API design with Express.js:

- **Framework**: Express.js with TypeScript for type-safe server development
- **API Design**: RESTful endpoints for candidate search, chat sessions, and message management
- **Request Validation**: Zod schemas for runtime type validation and API contract enforcement
- **Storage Interface**: Abstract storage interface allowing for flexible data persistence strategies
- **Error Handling**: Centralized error handling middleware for consistent API responses

## Data Storage Solutions
The application uses a flexible storage architecture:

- **ORM**: Drizzle ORM for type-safe database operations and schema management
- **Database**: PostgreSQL with Neon serverless database for production scalability
- **Schema**: Well-defined database schema with tables for candidates, chat sessions, and messages
- **Migration**: Drizzle Kit for database migrations and schema evolution
- **Fallback Storage**: In-memory storage implementation for development and testing

## Authentication and Authorization
Currently implements a basic session-based approach:

- **Session Management**: Express sessions with PostgreSQL session store
- **Cookie Configuration**: Secure cookie handling for session persistence
- **Development Mode**: Basic authentication structure ready for extension

## AI and Search Integration
The system incorporates AI-powered semantic search:

- **Embedding Service**: Hugging Face API integration for text embeddings using sentence-transformers
- **Similarity Matching**: Cosine similarity calculations for semantic candidate matching
- **Query Processing**: Natural language query parsing to extract skills, experience, and location filters
- **Fallback Search**: Simple text-based search when AI services are unavailable

# External Dependencies

## Core Framework Dependencies
- **@neondatabase/serverless**: Serverless PostgreSQL database connection for Neon
- **drizzle-orm**: Modern TypeScript ORM for database operations
- **express**: Web application framework for the backend API
- **react**: Frontend UI library for building user interfaces
- **@tanstack/react-query**: Data fetching and caching library for React

## UI and Styling
- **@radix-ui/react-***: Comprehensive set of accessible UI primitives
- **tailwindcss**: Utility-first CSS framework for styling
- **class-variance-authority**: Utility for creating type-safe component variants
- **lucide-react**: Icon library for consistent iconography

## Development and Build Tools
- **vite**: Fast build tool and development server
- **typescript**: Static type checking for JavaScript
- **drizzle-kit**: CLI tools for database schema management
- **zod**: Runtime type validation and schema definition

## AI and Machine Learning
- **Hugging Face API**: External service for generating text embeddings using sentence-transformers/all-MiniLM-L6-v2 model

## Optional Services
- **Replit Integration**: Development environment specific plugins and tools for Replit compatibility