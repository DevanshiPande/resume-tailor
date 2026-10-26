"""
Resume Tailor - AI-Powered Resume Customization

A Flask application that tailors LaTeX resumes based on job descriptions using AI.
"""

from .core import ResumeTailor
from .api_providers import APIManager
from .latex_processor import LaTeXProcessor
from .keyword_extractor import KeywordExtractor

__version__ = "1.0.0"
__author__ = "Resume Tailor Team"

__all__ = [
    "ResumeTailor",
    "APIManager", 
    "LaTeXProcessor",
    "KeywordExtractor"
] 