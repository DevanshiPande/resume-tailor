"""
LaTeX Processor Module

Handles parsing, modification, and compilation of LaTeX resume content.
"""

import re
import os
import subprocess
import tempfile
import shutil
import logging
from typing import Dict, List, Optional
from .api_providers import APIManager, GeminiProvider

logger = logging.getLogger(__name__)


class LaTeXProcessor:
    """Handles LaTeX content processing and compilation"""
    
    def __init__(self, api_manager: APIManager, gemini_provider: GeminiProvider):
        self.api_manager = api_manager
        self.gemini_provider = GeminiProvider()
    
    def parse_latex_sections(self, latex_resume: str) -> Dict[str, any]:
        """Parse LaTeX resume into sections using marker comments"""
        sections = {}
        
        # Define marker patterns for main sections
        main_marker_patterns = {
            'skills': (r'%----START OF TECHNICAL SKILLS MARKER----(.*?)%----END OF TECHNICAL SKILLS MARKER----', re.DOTALL)
        }
        
        # Parse main sections
        for section_name, (pattern, flags) in main_marker_patterns.items():
            match = re.search(pattern, latex_resume, flags)
            if match:
                sections[section_name] = match.group(1).strip()
            else:
                print(f"Warning: {section_name} marker not found in resume")
        
        # Parse individual experience markers
        experience_matches = re.findall(r'%----START OF EXPERIENCE MARKER----(.*?)%----END OF EXPERIENCE MARKER----', latex_resume, re.DOTALL)
        if experience_matches:
            sections['experiences'] = experience_matches
        else:
            print("Warning: No experience markers found in resume")
        
        # Parse general projects marker
        project_match = re.search(r'%----START OF PROJECTS MARKER----(.*?)%----END OF PROJECTS MARKER----', latex_resume, re.DOTALL)
        if project_match:
            sections['projects'] = project_match.group(1).strip()
        else:
            print("Warning: No projects marker found in resume")
        
        return sections
    
    def replace_sections_in_resume(self, latex_resume: str, sections: Dict[str, any]) -> str:
        """Replace modified sections back into the original LaTeX resume and remove markers"""
        modified_resume = latex_resume
        
        # Replace skills section
        if 'skills' in sections:
            # Use string replacement instead of regex to avoid escaping issues
            start_marker = '%----START OF TECHNICAL SKILLS MARKER----'
            end_marker = '%----END OF TECHNICAL SKILLS MARKER----'
            
            start_pos = modified_resume.find(start_marker)
            end_pos = modified_resume.find(end_marker)
            
            if start_pos != -1 and end_pos != -1 and end_pos > start_pos:
                # Replace the content between markers and remove the markers
                modified_resume = (
                    modified_resume[:start_pos] + sections['skills'] + 
                    modified_resume[end_pos + len(end_marker):]
                )
        
        # Replace experience sections
        if 'experiences' in sections:
            # Find all experience markers and replace them one by one
            experience_pattern = r'%----START OF EXPERIENCE MARKER----.*?%----END OF EXPERIENCE MARKER----'
            experience_matches = list(re.finditer(experience_pattern, modified_resume, re.DOTALL))
            
            # Replace from last to first to avoid index shifting issues
            for i in range(len(experience_matches) - 1, -1, -1):
                if i < len(sections['experiences']):
                    match = experience_matches[i]
                    start, end = match.span()
                    # Replace the entire marker block with just the content (no markers)
                    modified_resume = (
                        modified_resume[:start] + sections['experiences'][i] + 
                        modified_resume[end:]
                    )
        
        # Replace projects section
        if 'projects' in sections:
            # Use string replacement instead of regex to avoid escaping issues
            start_marker = '%----START OF PROJECTS MARKER----'
            end_marker = '%----END OF PROJECTS MARKER----'
            
            start_pos = modified_resume.find(start_marker)
            end_pos = modified_resume.find(end_marker)
            
            if start_pos != -1 and end_pos != -1 and end_pos > start_pos:
                # Replace the content between markers and remove the markers
                modified_resume = (
                    modified_resume[:start_pos] + sections['projects'] + 
                    modified_resume[end_pos + len(end_marker):]
                )
        
        return modified_resume
    
    def compile_latex(self, latex_content: str) -> Optional[Dict]:
        """
        Compile LaTeX to PDF and validate it's 1 page
        """
        logger.info("🔧 Starting LaTeX compilation...")
        logger.info(f"📄 LaTeX content length: {len(latex_content)}")
        logger.info(f"📄 LaTeX content preview: {latex_content[:200]}...")
        
        try:
            # Create temporary directory
            logger.info("📁 Creating temporary directory...")
            with tempfile.TemporaryDirectory() as temp_dir:
                logger.info(f"📁 Temp directory created: {temp_dir}")
                
                # Write LaTeX content to file
                tex_file = os.path.join(temp_dir, 'resume.tex')
                logger.info(f"📝 Writing LaTeX to file: {tex_file}")
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)
                logger.info("✅ LaTeX file written successfully")
                
                # Check if pdflatex exists
                logger.info("🔍 Checking if pdflatex is available...")
                try:
                    result = subprocess.run(['pdflatex', '--version'], capture_output=True, text=True, timeout=10)
                    logger.info(f"✅ pdflatex found: {result.stdout[:100]}...")
                except Exception as e:
                    logger.exception("❌ pdflatex not found:")
                    return None
                                
                # Try to compile with different approaches
                compilation_success = False
                
                # First attempt: Standard compilation
                print("🔄 Attempting first compilation (pdflatex)...")
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                    capture_output=True,
                    text=True,
                    cwd=temp_dir
                )
                
                print(f"📊 First compilation result: returncode={result.returncode}")
                print(f"📊 First compilation stdout: {result.stdout[:200]}...")
                print(f"📊 First compilation stderr: {result.stderr[:200]}...")
                
                if result.returncode == 0:
                    compilation_success = True
                    print("✅ First compilation successful!")
                else:
                    print(f"❌ First compilation failed: {result.stderr}")
                    
                    # Second attempt: Try with lualatex (better font support)
                    print("🔄 Attempting second compilation (lualatex)...")
                    result = subprocess.run(
                        ['lualatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                        capture_output=True,
                        text=True,
                        cwd=temp_dir
                    )
                    
                    print(f"📊 Second compilation result: returncode={result.returncode}")
                    print(f"📊 Second compilation stderr: {result.stderr[:200]}...")
                    
                    if result.returncode == 0:
                        compilation_success = True
                        print("✅ Second compilation successful!")
                    else:
                        print(f"❌ Second compilation failed: {result.stderr}")
                        
                        # Third attempt: Remove problematic packages and try again
                        print("🔄 Attempting third compilation (simplified content)...")
                        simplified_content = self._simplify_latex_content(latex_content)
                        print(f"📄 Simplified content length: {len(simplified_content)}")
                        with open(tex_file, 'w', encoding='utf-8') as f:
                            f.write(simplified_content)
                        
                        result = subprocess.run(
                            ['pdflatex', '-interaction=nonstopmode', '-output-directory', temp_dir, tex_file],
                            capture_output=True,
                            text=True,
                            cwd=temp_dir
                        )
                        
                        print(f"📊 Third compilation result: returncode={result.returncode}")
                        print(f"📊 Third compilation stderr: {result.stderr[:200]}...")
                        
                        if result.returncode == 0:
                            compilation_success = True
                            print("✅ Third compilation successful!")
                        else:
                            print(f"❌ Third compilation failed: {result.stderr}")
                
                if not compilation_success:
                    print("❌ All compilation attempts failed")
                    return None
                
                # Check if PDF was created
                pdf_file = os.path.join(temp_dir, 'resume.pdf')
                print(f"📄 Checking for PDF file: {pdf_file}")
                if not os.path.exists(pdf_file):
                    print("❌ PDF file not found")
                    return None
                
                print(f"✅ PDF file created: {pdf_file}")
                
                # Validate PDF page count and return result with status
                page_count = self._get_pdf_page_count(pdf_file)
                is_single_page = page_count == 1
                print(f"📊 PDF page count: {page_count}, is_single_page: {is_single_page}")
                
                # Copy PDF to temp directory for download
                temp_dir = os.environ.get('TEMP_DIR', 'temp')
                output_pdf = os.path.join(temp_dir, 'tailored_resume.pdf')
                print(f"📋 Copying PDF to: {output_pdf}")
                shutil.copy2(pdf_file, output_pdf)
                
                result = {
                    'filename': 'tailored_resume.pdf',
                    'is_single_page': is_single_page,
                    'page_count': page_count
                }
                print(f"✅ LaTeX compilation completed successfully: {result}")
                return result
                    
        except Exception as e:
            print(f"❌ Error compiling LaTeX: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _simplify_latex_content(self, latex_content: str) -> str:
        """Simplify LaTeX content by removing problematic packages and commands"""
        # Remove problematic packages
        problematic_packages = [
            r'\\usepackage\{CormorantGaramond\}',
            r'\\usepackage\{charter\}',
            r'\\usepackage\{FiraSans\}',
            r'\\usepackage\{roboto\}',
            r'\\usepackage\{noto-sans\}',
            r'\\usepackage\{sourcesanspro\}',
            r'\\usepackage\{helvet\}',
            r'\\renewcommand\{\\rmdefault\}\{phv\}',
            r'\\input\{glyphtounicode\}'
        ]
        
        for package in problematic_packages:
            latex_content = re.sub(package, '', latex_content)
        
        # Replace custom commands with standard LaTeX
        command_replacements = {
            r'\\resumeItem\{([^}]*)\}': r'\\item \1',
            r'\\resumeSubheading\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}': r'\\textbf{\1} \hfill \2 \\\\ \textit{\3} \hfill \textit{\4}',
            r'\\resumeSubSubheading\{([^}]*)\}\{([^}]*)\}': r'\\textit{\1} \hfill \textit{\2}',
            r'\\resumeProjectHeading\{([^}]*)\}\{([^}]*)\}': r'\\textbf{\1} \hfill \textit{\2}',
            r'\\resumeSubItem\{([^}]*)\}': r'\\item \1',
            r'\\resumeSubHeadingListStart': r'\\begin{itemize}',
            r'\\resumeSubHeadingListEnd': r'\\end{itemize}',
            r'\\resumeItemListStart': r'\\begin{itemize}',
            r'\\resumeItemListEnd': r'\\end{itemize}'
        }
        
        for old_cmd, new_cmd in command_replacements.items():
            latex_content = re.sub(old_cmd, new_cmd, latex_content)
        
        return latex_content
    
    def _get_pdf_page_count(self, pdf_path: str) -> int:
        """Get the number of pages in a PDF"""
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception as e:
            print(f"Error getting PDF page count: {e}")
            return 0
    
    def _validate_pdf_pages(self, pdf_path: str) -> bool:
        """Check if PDF has exactly 1 page"""
        return self._get_pdf_page_count(pdf_path) == 1
    
    