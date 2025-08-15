# 🧪 Test Case Generator

> **AI-Powered Test Case Generation for GitHub Repositories**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.1.0-black.svg)](https://nextjs.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.1-38B2AC.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A full-stack application that automatically generates comprehensive test cases for any GitHub repository using AI. Simply connect your repository, and let our intelligent system analyze your code and create robust test suites.

## ✨ Features

- 🔗 **GitHub Integration** - Seamlessly connect to any public or private repository
- 🤖 **AI-Powered Analysis** - Advanced AI models analyze your codebase for optimal test coverage
- 📁 **Smart File Tree** - Interactive file browser with hierarchical repository structure
- 🧪 **Multi-Framework Support** - Generate tests for pytest, Jest, and more
- 🚀 **Real-time Generation** - Instant test case creation with live AI processing
- 📱 **Modern UI/UX** - Beautiful, responsive interface built with Next.js and Tailwind CSS
- 🔒 **Secure Authentication** - GitHub OAuth integration with secure token management
- 📊 **Comprehensive Coverage** - Generate unit tests, integration tests, and edge case scenarios

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   APIs         │
│                 │    │                 │    │                 │
│ • File Tree     │    │ • GitHub API    │    │ • GitHub API   │
│ • Test Gen UI   │    │ • AI Service    │    │ • OpenRouter   │
│ • Responsive    │    │ • File Analysis │    │ • AI Models    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+**
- **GitHub Personal Access Token**
- **OpenRouter API Key** (for AI features)

### 1. Clone the Repository

```bash
git clone https://github.com/4yu5h-crtl/test-case-generator.git
cd Test_Case_Generator
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env_template.txt .env
# Edit .env with your GitHub token and OpenRouter API key

# Run the backend server
python run.py
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set backend URL (optional, defaults to localhost:8000)
# Create .env.local file:
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000/api/v1" > .env.local

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token_here

# AI Service Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Application Settings
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### GitHub Token Setup

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Generate a new token with scopes:
   - `repo` (Full control of private repositories)
   - `read:user` (Read user profile data)
3. Copy the token to your `.env` file

## 📚 API Endpoints

### GitHub Routes (`/api/v1/repos`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/repos/{owner}/{repo}/files` | GET | Get repository file tree |
| `/api/v1/repos/file-contents` | POST | Retrieve file contents |
| `/api/v1/repos/health` | GET | Service health check |
| `/api/v1/repos/test-connection` | GET | Test GitHub API connection |

### AI Routes (`/api/v1/ai`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/ai/summarize-tests-with-content` | POST | Generate test case summaries |
| `/api/v1/ai/generate-code` | POST | Generate complete test code |
| `/api/v1/ai/test-connection` | GET | Test AI service connection |
| `/api/v1/ai/supported-frameworks` | GET | List supported frameworks |

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **PyGithub** - GitHub API integration
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server for production deployment
- **Python-dotenv** - Environment variable management

### Frontend
- **Next.js 14** - React framework with App Router
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests
- **Jest** - Testing framework
- **React Testing Library** - Component testing utilities

### AI & External Services
- **OpenRouter** - AI model orchestration
- **GitHub API** - Repository access and file management

## 📁 Project Structure

```
test_case_generator/
├── 📁 backend/                 # FastAPI backend
│   ├── 📁 app/
│   │   ├── 📁 routes/         # API endpoints
│   │   ├── ai_service.py      # AI integration
│   │   ├── github_service.py  # GitHub API service
│   │   ├── models.py          # Data models
│   │   └── main.py            # Application entry point
│   ├── requirements.txt       # Python dependencies
│   └── run.py                 # Development server
├── 📁 frontend/               # Next.js frontend
│   ├── 📁 app/                # App Router pages
│   ├── 📁 components/         # React components
│   ├── 📁 lib/                # Utility functions
│   ├── package.json           # Node.js dependencies
│   └── tailwind.config.js     # Tailwind configuration
└── 📄 README.md               # This file
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend Deployment

```bash
# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# With Gunicorn (recommended for production)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment

```bash
cd frontend
npm run build
npm start
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.