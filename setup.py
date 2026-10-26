"""
Setup script for Resume Tailor
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="resume-tailor",
    version="1.0.0",
    author="Resume Tailor Team",
    description="AI-Powered Resume Customization Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/resume-tailor",
    project_urls={
        "Bug Reports": "https://github.com/your-username/resume-tailor/issues",
        "Source": "https://github.com/your-username/resume-tailor",
        "Documentation": "https://github.com/your-username/resume-tailor#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "resume-tailor=src.resume_tailor.core:main",
        ],
    },
    license="MIT",
    keywords="resume, latex, ai, job-application, career, flask",
) 