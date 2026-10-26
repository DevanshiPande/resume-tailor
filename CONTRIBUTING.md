# Contributing to Resume Tailor

Thank you for your interest in contributing to Resume Tailor! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome contributions of all kinds:

- **🐛 Bug Reports**: Help us identify and fix issues
- **✨ Feature Requests**: Suggest new features or improvements
- **📝 Documentation**: Improve README, docstrings, or add examples
- **🧪 Tests**: Add test cases or improve test coverage
- **🔧 Code Improvements**: Refactor, optimize, or enhance existing code
- **🌐 UI/UX**: Improve the web interface or user experience

### Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/resume-tailor.git
   cd resume-tailor
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Development Guidelines

#### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and single-purpose

#### Testing

- Write tests for new functionality
- Ensure all existing tests pass
- Aim for good test coverage
- Run tests before submitting:
  ```bash
   python tests/test_core.py
   python tests/test_markers.py
   ```

#### Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for new AI provider
fix: resolve LaTeX compilation issue
docs: update installation instructions
test: add tests for keyword extraction
```

### Project Structure

```
resume_tailor/
├── src/resume_tailor/     # Main application code
│   ├── core.py           # Main orchestrator
│   ├── api_providers.py  # AI provider abstractions
│   ├── keyword_extractor.py
│   ├── latex_processor.py
│   └── section_modifiers.py
├── tests/                # Test suite
├── templates/            # Flask templates
├── app.py               # Flask entry point
└── requirements.txt     # Dependencies
```

### Adding New Features

1. **Plan Your Feature**
   - Create an issue describing the feature
   - Discuss implementation approach
   - Consider impact on existing functionality

2. **Implement**
   - Follow the modular architecture
   - Add appropriate tests
   - Update documentation

3. **Test Thoroughly**
   - Test with different LaTeX templates
   - Verify AI provider integration
   - Check edge cases

### AI Provider Integration

To add a new AI provider:

1. **Create Provider Class**
   ```python
   class NewProvider(APIProvider):
       def __init__(self):
           self.api_key = os.getenv('NEW_PROVIDER_API_KEY')
           
       def is_available(self) -> bool:
           return bool(self.api_key)
           
       def call_api(self, messages: List[Dict], temperature: float = 0.3) -> Optional[str]:
           # Implementation here
           pass
   ```

2. **Add to APIManager**
   ```python
   self.providers = [
       OpenRouterProvider(),
       CerebrasProvider(),
       GeminiProvider(),
       NewProvider()  # Add here
   ]
   ```

3. **Update Documentation**
   - Add to README.md
   - Update env_example.txt
   - Add to requirements.txt if needed

### LaTeX Template Support

To support new LaTeX templates:

1. **Identify Required Markers**
   - Technical Skills marker
   - Experience markers (individual)
   - Projects marker (general)

2. **Test Compatibility**
   - Verify marker parsing
   - Test compilation
   - Check output formatting

3. **Document Template**
   - Add to README.md
   - Provide example template

### Submitting Changes

1. **Prepare Your Changes**
   ```bash
   git add .
   git commit -m "descriptive commit message"
   ```

2. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Provide clear description of changes
   - Reference related issues
   - Include test results
   - Add screenshots if UI changes

### Review Process

1. **Automated Checks**
   - All tests must pass
   - Code style compliance
   - Documentation updates

2. **Manual Review**
   - Code quality review
   - Functionality testing
   - Security considerations

3. **Merge**
   - Squash commits if needed
   - Update version if necessary
   - Release notes

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce
- **Expected vs Actual**: What you expected vs what happened
- **Environment**: OS, Python version, dependencies
- **Error Messages**: Full error traceback if applicable

### Feature Requests

For feature requests:

- **Use Case**: Describe the problem you're solving
- **Proposed Solution**: Your suggested approach
- **Alternatives**: Other approaches you've considered
- **Impact**: How this benefits the project

## 📚 Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [LaTeX Documentation](https://www.latex-project.org/help/documentation/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to Resume Tailor! 🚀 