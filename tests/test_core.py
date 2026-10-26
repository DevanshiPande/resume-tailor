#!/usr/bin/env python3
"""
Test suite for Resume Tailor core functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.resume_tailor import ResumeTailor


def test_keyword_extraction():
    """Test keyword extraction functionality"""
    print("Testing keyword extraction...")
    
    tailor = ResumeTailor()
    
    # Test with sample job description
    job_description = """
    Senior Software Engineer - Frontend Development
    - Strong experience with React, TypeScript, and modern JavaScript
    - Experience with AWS cloud services (Lambda, S3, CloudFront)
    - Knowledge of Python for backend development
    - Experience with Docker and Kubernetes
    - Familiarity with CI/CD pipelines and testing frameworks
    """
    
    keywords = tailor.extract_keywords(job_description)
    print(f"Extracted keywords: {keywords}")
    
    # Basic validation
    assert len(keywords) > 0, "Should extract at least one keyword"
    assert len(keywords) <= 15, "Should not extract more than 15 keywords"
    
    # Check for expected keywords
    expected_keywords = ['React', 'TypeScript', 'JavaScript', 'AWS', 'Python', 'Docker']
    found_keywords = [kw for kw in expected_keywords if any(kw.lower() in k.lower() for k in keywords)]
    assert len(found_keywords) > 0, f"Should find some expected keywords. Found: {keywords}"
    
    print("✅ Keyword extraction test passed!")
    return keywords


def test_basic_keyword_extraction():
    """Test fallback keyword extraction when no API is available"""
    print("Testing basic keyword extraction...")
    
    # Create a tailor instance (will use fallback if no API keys)
    tailor = ResumeTailor()
    
    job_description = """
    Frontend Developer
    - React, JavaScript, HTML, CSS
    - AWS, Docker, Git
    - Agile methodology
    """
    
    keywords = tailor.extract_keywords(job_description)
    print(f"Basic extracted keywords: {keywords}")
    
    # Should extract some keywords even without API
    assert len(keywords) > 0, "Should extract keywords even without API"
    
    print("✅ Basic keyword extraction test passed!")
    return keywords


def test_latex_parsing():
    """Test LaTeX parsing functionality"""
    print("Testing LaTeX parsing...")
    
    tailor = ResumeTailor()
    
    # Sample LaTeX resume with markers
    sample_latex = r"""
\documentclass[letterpaper,10.5pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\usepackage{enumitem}

\geometry{margin=0.5in}

\begin{document}

\section*{Technical Skills}
%----START OF TECHNICAL SKILLS MARKER----
\begin{itemize}[leftmargin=0.15in, label={}]
  \small{\item{
    \textbf{Languages}{: Python, JavaScript} \\
    \textbf{Frameworks}{: React, Angular} \\
    \textbf{Tools}{: Git, Docker, AWS}
  }}
\end{itemize}
%----END OF TECHNICAL SKILLS MARKER----

\section*{Experience}

\resumeSubheading{Company A}{2023 - Present}
{Senior Developer}{Location}
%----START OF EXPERIENCE MARKER----
\resumeItemListStart
  \resumeItem{Developed web applications}
\resumeItemListEnd
%----END OF EXPERIENCE MARKER----

\resumeSubheading{Company B}{2022 - 2023}
{Junior Developer}{Location}
%----START OF EXPERIENCE MARKER----
\resumeItemListStart
  \resumeItem{Built APIs}
\resumeItemListEnd
%----END OF EXPERIENCE MARKER----

\section*{Projects}
%----START OF PROJECTS MARKER----
\resumeSubHeadingListStart
  \resumeProjectHeading{\textbf{Project 1} $|$ \emph{React, Node.js}}{Date}
  \resumeItemListStart
    \resumeItem{Built a web application}
  \resumeItemListEnd
  
  \resumeProjectHeading{\textbf{Project 2} $|$ \emph{Python, AWS}}{Date}
  \resumeItemListStart
    \resumeItem{Developed an API}
  \resumeItemListEnd
\resumeSubHeadingListEnd
%----END OF PROJECTS MARKER----

\end{document}
"""
    
    sections = tailor.latex_processor.parse_latex_sections(sample_latex)
    
    print(f"Parsed sections: {list(sections.keys())}")
    assert 'skills' in sections, "Should parse skills section"
    assert 'projects' in sections, "Should parse general projects marker"
    assert 'experiences' in sections, "Should parse a list of experience markers"
    assert isinstance(sections['experiences'], list), "Experiences should be a list"
    assert len(sections['experiences']) == 2, "Should find 2 experience markers"
    
    print("✅ LaTeX parsing test passed!")


def test_pdf_validation():
    """Test PDF validation functionality"""
    print("Testing PDF validation...")
    
    tailor = ResumeTailor()
    
    # Test with a simple LaTeX document
    simple_latex = r"""
\documentclass[letterpaper,10.5pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}

\geometry{margin=0.5in}

\begin{document}

\section*{Test Resume}

This is a test resume with minimal content to ensure it fits on one page.

\section*{Skills}
- Python
- JavaScript
- React

\section*{Experience}
- Software Engineer at Company A
- Junior Developer at Company B

\end{document}
"""
    
    # Test PDF page count functionality
    pdf_result = tailor.compile_latex(simple_latex)
    
    if pdf_result:
        print(f"PDF validation result: {pdf_result['is_single_page']}")
        assert pdf_result['page_count'] >= 1, "PDF should have at least 1 page"
        print("✅ PDF validation test passed!")
    else:
        print("⚠️ PDF compilation failed (this is expected if LaTeX is not installed)")


def test_project_modification():
    """Test project modification functionality"""
    print("Testing project modification...")
    
    tailor = ResumeTailor()
    
    # Sample projects data
    projects_data = [
        {
            "title": "E-commerce Platform",
            "technologies": "React, Node.js, MongoDB",
            "description": "Built a full-stack e-commerce platform with user authentication, product catalog, and payment integration"
        },
        {
            "title": "Machine Learning Model",
            "technologies": "Python, TensorFlow, AWS",
            "description": "Developed a sentiment analysis model achieving 95% accuracy using deep learning techniques"
        },
        {
            "title": "Mobile App",
            "technologies": "React Native, Firebase",
            "description": "Created a cross-platform mobile app for task management with real-time synchronization"
        }
    ]
    
    # Sample project content
    sample_project_content = r"""
\resumeSubHeadingListStart
  \resumeProjectHeading{\textbf{Sample Project} $|$ \emph{Technologies}}{Date}
  \resumeItemListStart
    \resumeItem{Sample project description}
  \resumeItemListEnd
\resumeSubHeadingListEnd
"""
    
    # Test project modification
    modified_projects = tailor.section_modifier.modify_projects_section(
        "Software Engineer", sample_project_content, ["React", "Python"], projects_data
    )
    
    print(f"Modified projects section length: {len(modified_projects)} characters")
    assert len(modified_projects) > 0, "Should return modified project content"
    
    print("✅ Project modification test passed!")


def run_all_tests():
    """Run all tests"""
    print("🧪 Running Resume Tailor tests...")
    print()
    
    try:
        # Run tests
        test_keyword_extraction()
        test_basic_keyword_extraction()
        test_project_modification()
        test_latex_parsing()
        test_pdf_validation()
        
        print("\n🎉 All tests passed!")
        print("\nTo run the application:")
        print("1. Set your OPENROUTER_API_KEY in a .env file")
        print("2. Install LaTeX (MiKTeX, TeX Live, or MacTeX)")
        print("3. Run: python app.py")
        print("4. Open http://localhost:5000 in your browser")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    run_all_tests() 