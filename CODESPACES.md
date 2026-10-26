# Deploying Resume Tailor on GitHub Codespaces

This guide will help you deploy the Resume Tailor application on GitHub Codespaces.

## Prerequisites

1. A GitHub account
2. API keys for the AI services:
   - OpenRouter API key
   - Cerebras API key (optional)
   - Gemini API key (optional)

## Setup Instructions

### Step 1: Fork or Clone the Repository

1. Fork this repository to your GitHub account, or
2. Clone it to your local machine and push to your GitHub account

### Step 2: Open in Codespaces

1. Go to your repository on GitHub
2. Click the green "Code" button
3. Select "Codespaces" tab
4. Click "Create codespace on main"

### Step 3: Wait for Setup

The Codespace will automatically:
- Install TeX Live (full installation)
- Install Python dependencies
- Create necessary directories
- Set up environment variables

### Step 4: Configure API Keys

1. In the Codespace, open the `.env` file
2. Replace the placeholder values with your actual API keys:

```env
OPENROUTER_API_KEY=your_actual_openrouter_api_key
CEREBRAS_API_KEY=your_actual_cerebras_api_key
GEMINI_API_KEY=your_actual_gemini_api_key
SECRET_KEY=your_secret_key_here
```

### Step 5: Run the Application

In the Codespace terminal:

```bash
python app.py
```

### Step 6: Access the Application

1. The application will start on port 5000
2. GitHub Codespaces will automatically forward the port
3. You'll see a notification with a link to access the application
4. Click the link or go to: `http://localhost:5000`

## Features

- ✅ Automatic TeX Live installation
- ✅ Python dependencies installation
- ✅ Port forwarding (port 5000)
- ✅ Environment variable setup
- ✅ Debug mode enabled for development
- ✅ Hot reloading for code changes

## Troubleshooting

### If TeX Live installation fails:
```bash
sudo apt-get update
sudo apt-get install -y texlive-full
```

### If Python dependencies fail:
```bash
pip install -r requirements.txt
```

### If the application doesn't start:
1. Check the `.env` file has valid API keys
2. Ensure port 5000 is forwarded
3. Check the terminal output for errors

## Cost

GitHub Codespaces offers:
- 60 hours/month free for personal accounts
- Additional hours available for purchase
- Much cheaper than AWS for development and testing

## Security

- API keys are stored in the `.env` file (not committed to git)
- The application runs in an isolated container
- Port forwarding is secure and temporary 