# Resume Tailor - AI-Powered Resume Customization

An intelligent Flask application that tailors LaTeX resumes based on job descriptions using AI. The application uses a **marker-based approach** for precise, targeted modifications with a **modular architecture** for better maintainability and extensibility.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

## ✨ Features

- **🔍 Smart Keyword Extraction**: Extracts 5-15 relevant keywords from job descriptions
- **🎯 Targeted Section Modification**: Uses LaTeX markers for precise content updates
- **📄 Single-Page Validation**: Ensures the final resume is exactly 1 page
- **🤖 AI-Powered Optimization**: Uses multiple AI providers with automatic fallback (OpenRouter, Cerebras, Gemini)
- **📊 Project Selection**: Automatically selects the 2 most relevant projects
- **🔧 Robust LaTeX Compilation**: Supports complex LaTeX templates with custom fonts
- **⚡ Parallel Processing**: Uses threading for concurrent section modifications
- **🏗️ Modular Architecture**: Clean separation of concerns with abstracted components

## 🏗️ Architecture

The application follows a **modular architecture** with clear separation of concerns:

```
resume_tailor/
├── src/
│   └── resume_tailor/
│       ├── __init__.py          # Package initialization
│       ├── core.py              # Main orchestrator
│       ├── api_providers.py     # AI provider abstractions
│       ├── keyword_extractor.py # Keyword extraction logic
│       ├── latex_processor.py   # LaTeX parsing and compilation
│       └── section_modifiers.py # Section modification logic
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_core.py            # Core functionality tests
│   └── test_markers.py         # Marker verification tests
├── templates/                   # Flask templates
├── app.py                      # Flask application entry point
├── requirements.txt            # Dependencies
├── setup.py                   # Package configuration
└── README.md                  # Documentation
```

### Component Overview

- **`core.py`**: Main orchestrator that coordinates all components
- **`api_providers.py`**: Abstract base classes for different AI providers with fallback logic
- **`keyword_extractor.py`**: Handles keyword extraction with AI and regex fallback
- **`latex_processor.py`**: Manages LaTeX parsing, modification, and compilation
- **`section_modifiers.py`**: Handles section modifications with threading support

## 🎯 Marker-Based Approach

The application uses **LaTeX comment markers** to identify and modify specific sections. This approach provides **granular control** over which experiences and projects get modified.

### Required Markers in Your LaTeX Resume

Add these markers around the sections you want to modify:

#### Main Section Markers
```latex
%----START OF TECHNICAL SKILLS MARKER----
\begin{itemize}[leftmargin=0.15in, label={}]
  \small{\item{
    \textbf{Languages}{: Python, Java, JavaScript} \\
    \textbf{Frameworks}{: React, Angular, .NET} \\
    % ... other skills
  }}
\end{itemize}
%----END OF TECHNICAL SKILLS MARKER----
```

#### Individual Experience Markers
```latex
\resumeSubheading{Company}{Date}
{Junior Software Engineer}{Location}
%----START OF EXPERIENCE MARKER----
\resumeItemListStart
  \resumeItem{Your experience bullet points}
\resumeItemListEnd
%----END OF EXPERIENCE MARKER----

\resumeSubheading{Company}{Date}
{Software Engineering Intern}{Location}
%----START OF EXPERIENCE MARKER----
\resumeItemListStart
  \resumeItem{Your experience bullet points}
\resumeItemListEnd
%----END OF EXPERIENCE MARKER----

\resumeSubheading{Company}{Date}
{Research Assistant}{Location}
%----START OF EXPERIENCE MARKER----
\resumeItemListStart
  \resumeItem{Your experience bullet points}
\resumeItemListEnd
%----END OF EXPERIENCE MARKER----
```

#### General Projects Marker
```latex
\section{Projects}
%----START OF PROJECTS MARKER----
\resumeSubHeadingListStart
  \resumeProjectHeading{\textbf{Project Title} $|$ \emph{Technologies}}{Date}
  \resumeItemListStart
    \resumeItem{Project description}
  \resumeItemListEnd
  
  \resumeProjectHeading{\textbf{Another Project} $|$ \emph{More Technologies}}{Date}
  \resumeItemListStart
    \resumeItem{Another project description}
  \resumeItemListEnd
\resumeSubHeadingListEnd
%----END OF PROJECTS MARKER----
```

### Benefits of This Marker Structure

- **🎯 General Experience Control**: Each experience uses the same general marker, making it easy for anyone to use their resume
- **⚡ Universal Compatibility**: The general experience markers work with any job title or role
- **🛡️ Selective Modification**: Only relevant experiences are modified based on job requirements
- **📊 Priority-Based**: Recent experiences get higher priority for modifications
- **🔧 Flexible Projects**: General projects marker allows for complete project section replacement
- **📝 Clean Structure**: Each experience and project stands alone with its own marker

### How the Marker System Works

1. **Experience Modification**: Each individual experience is modified independently with role-specific prompts based on content analysis
2. **Project Selection**: The 2 most relevant projects replace the entire projects section
3. **Priority System**: Recent experiences get more attention from the AI model
4. **Context-Aware**: Each marker receives specific instructions for that role/project type

## 🤖 AI Provider Configuration

The application supports **three AI providers** with automatic fallback:

### 1. OpenRouter (Primary)
- **Model**: `qwen/qwen3-coder:free`
- **API Key**: `OPENROUTER_API_KEY`
- **Best for**: General resume optimization

### 2. Cerebras (Secondary)
- **Model**: `qwen-3-coder-480b`
- **API Key**: `CEREBRAS_API_KEY`
- **SDK**: Requires `cerebras-cloud-sdk` package
- **Best for**: Technical content optimization

### 3. Gemini 2.5 Flash Lite (Tertiary)
- **Model**: `gemini-2.0-flash-exp`
- **API Key**: `GEMINI_API_KEY`
- **Best for**: Creative content generation

### Fallback Logic
1. **First**: Try OpenRouter API
2. **Second**: If OpenRouter fails, try Cerebras API
3. **Third**: If Cerebras fails, try Gemini API
4. **Fallback**: If all APIs fail, use basic keyword extraction

### Environment Variables
Create a `.env` file with your API keys:
```env
OPENROUTER_API_KEY=your_openrouter_key_here
CEREBRAS_API_KEY=your_cerebras_key_here
GEMINI_API_KEY=your_gemini_key_here
```

## 🚀 Installation

### Prerequisites

1. **Python 3.8+**
2. **LaTeX Distribution** (TeX Live, MiKTeX, or MacTeX)
3. **API Keys** (optional but recommended):
   - **OpenRouter**: Get from [openrouter.ai](https://openrouter.ai/keys)
   - **Cerebras**: Get from [cerebras.ai](https://cerebras.ai/)
   - **Gemini**: Get from [Google AI Studio](https://aistudio.google.com/)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd resume_tailor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: The Cerebras SDK will be installed automatically. If you encounter issues, install it manually:
   ```bash
   pip install cerebras-cloud-sdk
   ```

3. **Set up environment variables** (optional):
   ```bash
   cp env_example.txt .env
   # Edit .env and add your API keys
   # The application works without API keys but with limited functionality
   ```

4. **Prepare your LaTeX resume**:
   - Add the required markers to your `.tex` file
   - Ensure it compiles to exactly 1 page

## 🎮 Usage

### Web Interface

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your browser**:
   Navigate to `http://localhost:5000`

3. **Input your data**:
   - Paste your job description
   - Upload your LaTeX resume (with markers)
   - Add your projects (optional)

4. **Get your tailored resume**:
   - Click "Tailor Resume"
   - Download the generated PDF

### Programmatic Usage

```python
from src.resume_tailor import ResumeTailor

# Initialize
tailor = ResumeTailor()

# Complete resume tailoring process
result = tailor.tailor_resume(job_description, latex_resume, projects_data)

# Access results
keywords = result['keywords']
modified_resume = result['modified_resume']
pdf_result = result['pdf_result']
```

### Individual Component Usage

```python
from src.resume_tailor import ResumeTailor

# Initialize
tailor = ResumeTailor()

# Extract keywords
keywords = tailor.extract_keywords(job_description)

# Modify resume sections
modified_resume = tailor.modify_resume_sections(
    latex_resume, keywords, projects_data, job_description
)

# Compile to PDF
pdf_result = tailor.compile_latex(modified_resume)
```

## 📋 How It Works

### Step 1: Keyword Extraction
- Analyzes job description for technical skills, tools, and requirements
- Extracts 5-15 most relevant keywords
- Sorts by relevance for optimal matching

### Step 2: Section Modification (Parallel Processing)
- **Experience**: Subtly incorporates keywords into existing bullet points
- **Skills**: Adds relevant technical keywords to appropriate categories
- **Projects**: Replaces with 2 most relevant projects, adjusting phrasing
- **Performance**: All three modifications run concurrently using threading for faster processing

### Step 3: PDF Generation
- Compiles modified LaTeX to PDF
- Validates single-page requirement
- Handles complex LaTeX packages and fonts

## ⚡ Performance Optimization

The application uses **parallel processing** to optimize performance:

### Threading Implementation
- **Concurrent Modifications**: Experience, Skills, and Projects sections are modified simultaneously
- **Independent Operations**: Each modification runs in its own thread
- **Faster Response Times**: Significant time savings, especially when API calls are involved
- **Error Handling**: If one thread fails, others continue and original content is preserved

### Performance Benefits
- **~3x Faster**: When all three sections need modification
- **Better UX**: Users experience faster response times
- **Scalable**: Performance scales with available CPU cores
- **Reliable**: Thread-safe error handling ensures stability

## 🧪 Testing

### Run All Tests
```bash
python tests/test_core.py
```

### Run Marker Verification
```bash
python tests/test_markers.py
```

### Run with Coverage
```bash
pytest tests/ --cov=src/ --cov-report=html
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENROUTER_API_KEY=your_api_key_here

# Optional
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### LaTeX Requirements

The application supports:
- Custom fonts (CormorantGaramond, Charter, etc.)
- Unicode support (glyphtounicode)
- Complex LaTeX packages
- Custom commands and environments

## 🐛 Troubleshooting

### Common Issues

1. **"Failed to compile LaTeX"**:
   - Ensure TexLive is properly installed
   - Check that all required packages are available
   - Verify LaTeX syntax in your resume

2. **"Markers not found"**:
   - Add the required markers to your LaTeX resume
   - Ensure markers are exactly as shown above

3. **"PDF not exactly 1 page"**:
   - Reduce content or adjust formatting
   - Check for excessive whitespace

4. **"API key not found"**:
   - Set your API keys in the `.env` file
   - Restart the application after setting the keys

5. **"Cerebras SDK not installed"**:
   - Install the Cerebras SDK: `pip install cerebras-cloud-sdk`
   - Or reinstall requirements: `pip install -r requirements.txt`

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Example

### Input Job Description
```
Senior Software Engineer - Frontend Development
- Strong experience with React, TypeScript, and modern JavaScript
- Experience with AWS cloud services (Lambda, S3, CloudFront)
- Knowledge of Python for backend development
- Experience with Docker and Kubernetes
```

### Output Modifications
- **Experience**: Enhanced bullet points with React, AWS, Docker keywords
- **Skills**: Added TypeScript, AWS Lambda, Kubernetes to appropriate categories
- **Projects**: Selected most relevant projects and adjusted descriptions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenRouter** for AI model access
- **TeX Live** for LaTeX compilation
- **Flask** for the web framework
- **DeepSeek** for the AI model powering the optimizations 