#!/usr/bin/env python3
"""
Test suite for marker verification
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.resume_tailor import ResumeTailor


def test_marker_verification():
    """Test marker verification with the actual resume"""
    print("🧪 Testing New Marker Structure")
    print("=" * 40)
    print()
    
    # Initialize the resume tailor
    tailor = ResumeTailor()
    
    # Read the actual resume file
    try:
        with open('tadi_abhinav_resume.tex', 'r', encoding='utf-8') as f:
            actual_resume = f.read()
    except FileNotFoundError:
        print("⚠️ tadi_abhinav_resume.tex not found, using sample resume")
        actual_resume = r"""
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
    \textbf{Languages}{: Python, Java, JavaScript} \\
    \textbf{Frameworks}{: React, Angular, .NET} \\
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
    
    print("🔍 Parsing resume sections...")
    sections = tailor.latex_processor.parse_latex_sections(actual_resume)
    
    # Expected sections
    expected_sections = ['skills', 'experiences', 'projects']
    
    print("Found sections:", list(sections.keys()))
    
    # Check each expected section
    for section in expected_sections:
        if section in sections:
            print(f"  ✅ {section}: Found")
        else:
            print(f"  ❌ {section}: Not found")
    
    # Check that projects is a string for general marker
    if 'projects' in sections:
        if isinstance(sections['projects'], str):
            print(f"  ✅ projects: Found general projects marker")
            print(f"    Projects content: {len(sections['projects'])} characters")
        else:
            print(f"  ❌ projects: Should be a string for general marker")
    
    # Check that experiences is a list of individual experience markers
    if 'experiences' in sections:
        if isinstance(sections['experiences'], list):
            print(f"  ✅ experiences: Found {len(sections['experiences'])} individual experience markers")
            for i, experience in enumerate(sections['experiences']):
                print(f"    Experience {i+1}: {len(experience)} characters")
        else:
            print(f"  ❌ experiences: Should be a list of individual markers")
    
    print("\n✅ Marker structure test completed!")


if __name__ == "__main__":
    test_marker_verification() 