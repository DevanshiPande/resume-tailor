"""
Core Resume Tailor Module

Main orchestrator that coordinates all components for resume tailoring.
"""

from typing import List, Dict, Optional
from .api_providers import APIManager, GeminiProvider
from .keyword_extractor import KeywordExtractor
from .latex_processor import LaTeXProcessor
from .section_modifiers import ThreadedSectionModifier


class ResumeTailor:
    """Main class that orchestrates resume tailoring process"""
    
    def __init__(self):
        """Initialize all components"""
        self.api_manager = APIManager()
        self.gemini_provider = GeminiProvider()
        self.keyword_extractor = KeywordExtractor(self.api_manager)
        self.latex_processor = LaTeXProcessor(self.api_manager, self.gemini_provider)
        self.section_modifier = ThreadedSectionModifier(self.api_manager)
    
    def extract_keywords(self, job_description: str) -> List[str]:
        """
        Step 1: Extract relevant keywords from job description
        """
        return self.keyword_extractor.extract_keywords(job_description)
    
    def modify_resume_sections(self, latex_resume: str, keywords: List[str], 
                              projects_data: List[Dict], job_description: str = "") -> str:
        """
        Step 2: Modify resume sections to include keywords using parallel processing
        """
        # Parse the LaTeX resume to identify sections
        sections = self.latex_processor.parse_latex_sections(latex_resume)
        
        # Modify sections in parallel
        modified_sections = self.section_modifier.modify_sections_parallel(
            sections, keywords, job_description, projects_data
        )
        
        # Update sections with results
        if 'experiences' in modified_sections:
            sections['experiences'] = modified_sections['experiences']
        if 'skills' in modified_sections:
            sections['skills'] = modified_sections['skills']
        if 'projects' in modified_sections:
            sections['projects'] = modified_sections['projects']
        
        # Replace all modified sections in the original LaTeX resume
        modified_resume = self.latex_processor.replace_sections_in_resume(latex_resume, sections)

        return modified_resume

    def compile_latex(self, latex_content: str) -> Optional[Dict]:
        """
        Step 3: Compile LaTeX to PDF and validate it's 1 page
        """
        return self.latex_processor.compile_latex(latex_content)
    
    def tailor_resume(self, job_description: str, latex_resume: str, 
                      projects_data: List[Dict] = None) -> Dict:
        """
        Complete resume tailoring process
        
        Returns:
            Dict with keys: 'keywords', 'modified_resume', 'pdf_result'
        """
        # Step 1: Extract keywords
        keywords = self.extract_keywords(job_description)
        
        # Step 2: Modify resume sections
        modified_resume = self.modify_resume_sections(
            latex_resume, keywords, projects_data or [], job_description
        )
        
        # Step 3: Compile to PDF
        pdf_result = self.compile_latex(modified_resume)
        
        return {
            'keywords': keywords,
            'modified_resume': modified_resume,
            'pdf_result': pdf_result
        } 