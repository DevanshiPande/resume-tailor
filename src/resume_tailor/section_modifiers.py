"""
Section Modifiers Module

Handles modification of different resume sections (experience, skills, projects)
using AI with threading support.
"""

import time
import threading
from typing import List, Dict
from .api_providers import APIManager


class SectionModifier:
    """Base class for section modifiers"""
    
    def __init__(self, api_manager: APIManager):
        self.api_manager = api_manager
    
    def _clean_ai_response(self, content: str) -> str:
        """Clean AI response by removing markdown formatting and extra whitespace"""
        if not content:
            return content
        
        original_content = content
        print(f"🔍 Cleaning AI response - Original length: {len(content)}")
        print(f"🔍 Original content preview: {content[:100]}...")
        
        # Remove markdown code blocks
        content = content.strip()
        
        # Remove ```latex and ``` markers (case insensitive)
        import re
        
        # Remove starting code blocks
        content = re.sub(r'^```(?:latex|LaTeX|LATEX)?\s*', '', content, flags=re.IGNORECASE)
        
        # Remove ending code blocks
        content = re.sub(r'\s*```$', '', content)
        
        # Remove leading/trailing whitespace
        content = content.strip()
        
        # Normalize newlines - replace multiple newlines with single newlines
        content = re.sub(r'\n+', '\n', content)
        
        # Remove any remaining markdown artifacts
        content = re.sub(r'^`+', '', content)  # Remove leading backticks
        content = re.sub(r'`+$', '', content)  # Remove trailing backticks
        
        cleaned_content = content.strip()
        print(f"✅ Cleaned content length: {len(cleaned_content)}")
        print(f"✅ Cleaned content preview: {cleaned_content[:100]}...")
        
        return cleaned_content
    
    def modify_experience_sections(self, experience_content: List[str], keywords: List[str]) -> List[str]:
        """Modify experience sections to include keywords using general experience markers"""
        start_time = time.time()
        
        # Check if any API provider is available
        if not self.api_manager.has_any_provider():
            return experience_content
        
        modified_experiences = []
        
        # Process each experience marker
        for i, experience_text in enumerate(experience_content):
            
            prompt = f"""
You are a resume optimization expert. Modify ONLY the experience content in the LATEX code below to subtly incorporate these keywords: {keywords}
YOU DONT HAVE TO ADD ALL THE KEYWORDS, YOU CAN ADD SOME OF THEM THAT ARE RELEVANT TO THE EXPERIENCE.

RULES:
1. ONLY modify the text in the LATEX code that is under this experience
2. YOU ARE STRICTLY NOT ALLOWED TO ADD NEW resumeItems, YOU ARE ONLY ALLOWED TO MODIFY THE EXISTING ONES.
3. Prioritize semantic relevance and fluency over keyword stuffing
4. Maintain the original LaTeX formatting and structure exactly
5. Keep the same tone and professional style
6. ENSURE THE CONTENT ON EACH ITEM IS LESS THAN 180 CHARACTERS. IT IS VERY IMPORTANT YOU DO NOT RETURN ANYTHING ELSE APART FROM THE LATEX CODE.
7. Focus on the most relevant keywords for this specific role

IT IS VERY VERY IMPORTANT YOU DO NOT MODIFY THE STRUCTURE OF THE LATEX CODE, YOU ARE ONLY ALLOWED TO MODIFY THE CONTENT OF THE EXISTING //resumeItem

EXPERIENCE SECTION CONTENT TO MODIFY:
{experience_text}

Return ONLY the modified experience section content (without the markers). Maintain exact LaTeX formatting.
Example of good modification:
- Original: "\\resumeItem{{Developed computer vision solutions for image preprocessing and segmentation using \\textbf{{OpenCV}} and \\textbf{{PyTorch}}.}}"
- Modified: "\\resumeItem{{Developed computer vision solutions for image preprocessing and segmentation using \\textbf{{OpenCV}} and \\textbf{{PyTorch}} and \\textbf{{PyTorch Lightning}}.}}"

IT IS VERY VERY IMPORTANT YOU DONT ADD NEW /resumeItem, YOU ARE ONLY ALLOWED TO MODIFY THE EXISTING ONES. AFTER MODIFICATION RECHECK TO MAKE SURE YOU DIDNT ADD ANY NEW /resumeItem.
Return the complete modified experience section content, IT IS VERY IMPORTANT YOU DO NOT RETURN ANYTHING ELSE APART FROM THE LATEX CODE.
"""
            
            try:
                messages = [{"role": "user", "content": prompt}]
                content = self.api_manager.call_with_fallback(messages, temperature=0.3)
                
                if not content:
                    modified_experiences.append(experience_text) # Keep original if no modification
                    continue
                
                # Clean the AI response and replace the specific experience section content
                modified_content = self._clean_ai_response(content)
                modified_experiences.append(modified_content)
                
            except Exception as e:
                print(f"Error modifying experience {i+1}: {e}")
                modified_experiences.append(experience_text) # Keep original on error
        
        end_time = time.time()
        print(f"  📝 Experience modification: {end_time - start_time:.2f}s")
        return modified_experiences
    
    def modify_skills_section(self, skills_content: str, keywords: List[str]) -> str:
        """Modify skills section to include relevant technical keywords using marker-based approach"""
        start_time = time.time()
        
        prompt = f"""
You are a resume optimization expert. Modify ONLY the technical skills section content in the LATEX code below to include relevant keywords from: {keywords}

RULES:
1. ONLY add technical keywords (tools, languages, frameworks, platforms)
2. Sort into appropriate existing categories (Languages, Frameworks, Databases, Cloud & DevOps, AI/ML, Testing & Tools, Certifications)
3. Maintain the exact LaTeX formatting and structure
4. Do NOT add new categories
5. Ensure the content fits within 1 page
6. Keep the same professional tone

TECHNICAL SKILLS SECTION CONTENT TO MODIFY:
{skills_content}

Return ONLY the modified technical skills section content (without the markers). Maintain exact LaTeX formatting.
Example of good addition:
- Add "React" to Frameworks category
- Add "AWS Lambda" to Cloud & DevOps category

Return the complete modified technical skills section content, IT IS VERY IMPORTANT YOU DO NOT RETURN ANYTHING ELSE APART FROM THE LATEX CODE. DO NOT ADD ANYTHING ELSE.
"""
        
        # Check if any API provider is available
        if not self.api_manager.has_any_provider():
            return skills_content
            
        try:
            messages = [{"role": "user", "content": prompt}]
            content = self.api_manager.call_with_fallback(messages, temperature=0.3)
            
            if not content:
                return skills_content
            
            # Clean the AI response and return the modified skills content
            modified_content = self._clean_ai_response(content)
            return modified_content
            
        except Exception as e:
            print(f"Error modifying skills section: {e}")
            return skills_content
        
        end_time = time.time()
        print(f"  🔧 Skills modification: {end_time - start_time:.2f}s")
        return modified_content
    
    def modify_projects_section(self, job_description: str, project_content: str, keywords: List[str], projects_data: List[Dict]) -> str:
        """Modify projects section to include the 2 most relevant projects using general PROJECTS marker"""
        start_time = time.time()
        
        if not projects_data:
            return project_content

        prompt = f"""
You are a resume optimization expert. Analyze the below job description and figure out from the list of projects below which 2 are the most relevant to the job description, then replace the content in the LATEX code below with the content of the two projects.

PROJECTS LIST:
{projects_data}

JOB DESCRIPTION:
{job_description}

LATEX CODE TO MODIFY:
{project_content}

KEYWORDS:
{keywords}

RULES:
1. You are not allowed to modify the structure of the LATEX code, you are only allowed to replace the content of the projects with the content of the two most relevant projects.
2. Adjust phrasing slightly to align with the job keywords
3. ENSURE THE CONTENT ON EACH ITEM IS LESS THAN 100 CHARACTERS. IT IS VERY IMPORTANT YOU DO NOT RETURN ANYTHING ELSE APART FROM THE LATEX CODE.
4. Keep professional tone and style
5. Make the project description relevant to the job keywords
6. YOU ARE STRICTLY NOT ALLOWED TO ADD NEW \\resumeItem, YOU ARE ONLY ALLOWED TO MODIFY THE EXISTING ONES.
7. IT IS VERY IMPORTANT YOU DO NOT RETURN ANYTHING ELSE APART FROM THE LATEX CODE.

IT IS VERY VERY IMPORTANT YOU DONT ADD NEW /resumeItem, YOU ARE ONLY ALLOWED TO MODIFY THE EXISTING ONES. AFTER MODIFICATION RECHECK TO MAKE SURE YOU DIDNT ADD ANY NEW /resumeItem.
Return the complete modified projects section content, IT IS VERY IMPORTANT YOU DO NOT RETURN ANYTHING ELSE APART FROM THE LATEX CODE.
"""
        
        try:
            messages = [{"role": "user", "content": prompt}]
            content = self.api_manager.call_with_fallback(messages, temperature=0.3)
            
            if not content:
                return project_content
            
            # Clean the AI response and add the new project content
            modified_content = self._clean_ai_response(content)
            return modified_content
            
        except Exception as e:
            print(f"Error creating project content: {e}")
            return project_content
        
        end_time = time.time()
        print(f"  📊 Projects modification: {end_time - start_time:.2f}s")
        return modified_content


class ThreadedSectionModifier(SectionModifier):
    """Threaded version of section modifier for parallel processing"""
    
    def modify_sections_parallel(self, sections: Dict[str, any], keywords: List[str], 
                                job_description: str = "", projects_data: List[Dict] = None) -> Dict[str, any]:
        """Modify all sections in parallel using threading"""
        start_time = time.time()
        
        # Thread-safe storage for results
        results = {}
        threads = []
        
        # Function to run modification in thread
        def run_modification(mod_type, func, *args):
            try:
                result = func(*args)
                results[mod_type] = result
            except Exception as e:
                print(f"Error in {mod_type} modification: {e}")
                # Keep original content on error
                if mod_type == 'experiences':
                    results[mod_type] = args[0]  # original experiences
                elif mod_type == 'skills':
                    results[mod_type] = args[0]  # original skills
                elif mod_type == 'projects':
                    results[mod_type] = args[1]  # original projects
        
        # Start threads for each modification type
        if 'experiences' in sections:
            thread = threading.Thread(
                target=run_modification,
                args=('experiences', self.modify_experience_sections, sections['experiences'], keywords)
            )
            threads.append(thread)
            thread.start()
        
        if 'skills' in sections:
            thread = threading.Thread(
                target=run_modification,
                args=('skills', self.modify_skills_section, sections['skills'], keywords)
            )
            threads.append(thread)
            thread.start()
        
        if 'projects' in sections:
            thread = threading.Thread(
                target=run_modification,
                args=('projects', self.modify_projects_section, job_description, sections['projects'], keywords, projects_data or [])
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        print(f"⏱️ Resume modification completed in {end_time - start_time:.2f} seconds using {len(threads)} threads")
        
        return results 