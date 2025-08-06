// AI service utilities for candidate matching
export interface EmbeddingResponse {
  embeddings: number[];
}

export interface SearchFilters {
  skills?: string[];
  experience?: string;
  location?: string;
  title?: string;
}

// Parse natural language query into structured filters using simple keyword matching
// In production, this would use a proper NLP model
export function parseQueryToFilters(query: string): SearchFilters {
  const queryLower = query.toLowerCase();
  const filters: SearchFilters = {};
  
  // Extract common skills
  const skillKeywords = {
    'java': 'Java',
    'javascript': 'JavaScript',
    'react': 'React',
    'node': 'Node.js',
    'python': 'Python',
    'spring': 'Spring',
    'aws': 'AWS',
    'docker': 'Docker',
    'kubernetes': 'Kubernetes',
    'microservices': 'Microservices'
  };
  
  const detectedSkills: string[] = [];
  Object.entries(skillKeywords).forEach(([keyword, skill]) => {
    if (queryLower.includes(keyword)) {
      detectedSkills.push(skill);
    }
  });
  
  if (detectedSkills.length > 0) {
    filters.skills = detectedSkills;
  }
  
  // Extract experience requirements
  const experienceMatch = queryLower.match(/(\d+)\s*\+?\s*years?/);
  if (experienceMatch) {
    filters.experience = `${experienceMatch[1]}+ years`;
  }
  
  // Extract location preferences
  const locationKeywords = ['bangalore', 'mumbai', 'pune', 'delhi', 'hyderabad', 'chennai'];
  locationKeywords.forEach(location => {
    if (queryLower.includes(location)) {
      filters.location = location.charAt(0).toUpperCase() + location.slice(1);
    }
  });
  
  // Extract job titles
  const titleKeywords = ['developer', 'engineer', 'architect', 'lead', 'senior', 'junior'];
  titleKeywords.forEach(title => {
    if (queryLower.includes(title)) {
      filters.title = title;
    }
  });
  
  return filters;
}

// Calculate similarity score between query and candidate
export function calculateSimilarity(query: string, candidateText: string): number {
  const queryWords = query.toLowerCase().split(' ').filter(word => word.length > 2);
  const candidateWords = candidateText.toLowerCase().split(' ');
  
  let matches = 0;
  let totalWeight = 0;
  
  queryWords.forEach(word => {
    totalWeight += 1;
    if (candidateWords.some(cWord => cWord.includes(word) || word.includes(cWord))) {
      matches += 1;
    }
  });
  
  return totalWeight > 0 ? (matches / totalWeight) * 100 : 0;
}
