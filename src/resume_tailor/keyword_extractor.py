"""
Keyword Extractor Module

Handles extraction of relevant keywords from job descriptions using AI
with fallback to regex-based extraction.
"""

import re
import json
from typing import List
from .api_providers import APIManager


class KeywordExtractor:
    """Extracts relevant keywords from job descriptions"""
    
    def __init__(self, api_manager: APIManager):
        self.api_manager = api_manager
    
    def _clean_ai_response(self, content: str) -> str:
        """Clean AI response by removing markdown formatting and extra whitespace"""
        if not content:
            return content
        
        # Remove markdown code blocks
        content = content.strip()
        
        # Remove ```json and ``` markers (case insensitive)
        import re
        
        # Remove starting code blocks
        content = re.sub(r'^```(?:json|JSON)?\s*', '', content, flags=re.IGNORECASE)
        
        # Remove ending code blocks
        content = re.sub(r'\s*```$', '', content)
        
        # Remove leading/trailing whitespace
        content = content.strip()
        
        # Normalize newlines - replace multiple newlines with single newlines
        content = re.sub(r'\n+', '\n', content)
        
        # Remove any remaining markdown artifacts
        content = re.sub(r'^`+', '', content)  # Remove leading backticks
        content = re.sub(r'`+$', '', content)  # Remove trailing backticks
        
        return content.strip()
    
    def extract_keywords(self, job_description: str) -> List[str]:
        """
        Extract relevant keywords from job description using AI or fallback
        """
        prompt = f"""
        Extract the most important keywords and phrases from this job description that a recruiter or ATS might expect in a resume.
        
        Focus on:
        - Technical skills (programming languages, frameworks, tools)
        - Soft skills (leadership, communication, etc.)
        - Responsibilities and duties
        - Industry-specific terms
        
        Job Description:
        {job_description}
        
        Return only a JSON array of 5-15 keywords sorted by relevance (most relevant first).
        Example: ["Python", "React", "AWS", "Agile", "Team Leadership"]
        
        CRITICAL: Return ONLY the JSON array. Do NOT wrap in markdown code blocks, do NOT add ```json or ``` markers, do NOT add any explanations or text outside the JSON.
        """
        
        # Check if any API provider is available
        if not self.api_manager.has_any_provider():
            # Fallback: basic keyword extraction
            return self._basic_keyword_extraction(job_description)
            
        try:
            messages = [{"role": "user", "content": prompt}]
            content = self.api_manager.call_with_fallback(messages, temperature=0.3)
            
            if not content:
                return self._basic_keyword_extraction(job_description)
            
            # Clean the AI response
            content = self._clean_ai_response(content)
            
            # Try to extract JSON array
            if content.startswith('[') and content.endswith(']'):
                keywords = json.loads(content)
            else:
                # Fallback: extract keywords from text
                keywords = re.findall(r'"([^"]+)"', content)
                if not keywords:
                    keywords = content.split(', ')
            
            return keywords[:15]  # Limit to 15 keywords
            
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            # Fallback: basic keyword extraction
            return self._basic_keyword_extraction(job_description)
    
    def _basic_keyword_extraction(self, job_description: str) -> List[str]:
        """Fallback keyword extraction using regex patterns"""
        keywords = []
        
        # Technical skills patterns
        tech_patterns = [
            r'\b(Python|Java|JavaScript|C\+\+|C#|Go|Rust|Swift|Kotlin|TypeScript)\b',
            r'\b(React|Angular|Vue|Node\.js|Express|Django|Flask|Spring|ASP\.NET)\b',
            r'\b(AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|GitHub|GitLab)\b',
            r'\b(SQL|MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch)\b',
            r'\b(HTML|CSS|Sass|Less|Bootstrap|Tailwind|Material-UI)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            keywords.extend(matches)
        
        # Soft skills patterns
        soft_patterns = [
            r'\b(Leadership|Communication|Teamwork|Problem Solving|Analytical)\b',
            r'\b(Agile|Scrum|Kanban|Waterfall|DevOps)\b',
            r'\b(Project Management|Product Management|User Experience|UX|UI)\b'
        ]
        
        for pattern in soft_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            keywords.extend(matches)
        
        return list(set(keywords))[:15] 