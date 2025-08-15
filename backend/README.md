# Test Case Generator - Backend

FastAPI backend for the Test Case Generator application that integrates with GitHub API to fetch repository files and prepare for AI-powered test case generation.

## Features

- **GitHub Integration**: Authenticate and fetch repository files using PyGithub
- **File Tree API**: Get hierarchical file structure of any GitHub repository
- **File Content API**: Retrieve contents of multiple files for analysis
- **RESTful API**: Clean, documented API endpoints with automatic OpenAPI documentation
- **Error Handling**: Comprehensive error handling with detailed logging

## Tech Stack

- **Framework**: FastAPI
- **GitHub API**: PyGithub
- **Data Validation**: Pydantic
- **Documentation**: Automatic OpenAPI/Swagger docs
- **CORS**: Cross-origin resource sharing enabled

## Setup

### Prerequisites

- Python 3.8+
- GitHub Personal Access Token

### Installation

1. **Clone the repository** (if not already done)
2. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

3. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   Create a `.env` file in the `backend/` directory:
   ```bash
   # Copy the template
   cp env_template.txt .env
   # Then edit .env with your actual values
   ```
   
   Or manually create `.env` with:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token_here
   DEBUG=True
   ```

### GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with the following scopes:
   - `repo` (Full control of private repositories)
   - `read:user` (Read user profile data)
3. Copy the token and add it to your `.env` file

## Running the Application

### Development Mode

```bash
# From the backend directory
python run.py
```

Or using the module approach:
```bash
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### GitHub Routes (`/api/v1/repos`)

#### Get Repository Files
```
GET /api/v1/repos/{owner}/{repo}/files
```
Returns a hierarchical file tree for the specified repository.

**Parameters:**
- `owner`: Repository owner username
- `repo`: Repository name

**Response:** `FileTreeResponse` with repository info and file tree

#### Get File Contents
```
POST /api/v1/repos/file-contents
```
Retrieves contents of multiple files from a repository.

**Request Body:** `FileContentRequest` with owner, repo, and file paths
**Response:** `FileContentResponse` with file contents

#### Health Check
```
GET /api/v1/repos/health
```
Returns service health status.

#### Test Connection
```
GET /api/v1/repos/test-connection
```
Tests GitHub API connection and authentication.

### AI Routes (`/api/v1/ai`)

#### Generate Test Case Summaries
```
POST /api/v1/ai/summarize-tests-with-content
```
Generates test case summaries for given file contents using AI.

**Request Body:** List of `FileContent` objects
**Query Parameters:** `framework` (default: pytest)
**Response:** Test case summaries with id and summary

#### Generate Test Case Code
```
POST /api/v1/ai/generate-code
```
Generates complete test case code for a given summary.

**Request Body:** `FileContent` + `summary` string
**Query Parameters:** `framework` (default: pytest)
**Response:** Generated test case code

#### Test AI Connection
```
GET /api/v1/ai/test-connection
```
Tests AI service connection and shows current mode (mock/live).

#### Supported Frameworks
```
GET /api/v1/ai/supported-frameworks
```
Returns list of supported testing frameworks.

### Root Endpoints

#### Application Info
```
GET /
```
Returns application information and available endpoints.

#### Health Check
```
GET /health
```
Returns application health status.

## Data Models

### FileNode
Represents a file or directory in the repository tree:
- `name`: File/directory name
- `path`: Full path from repository root
- `type`: File type (file, dir, symlink, submodule)
- `size`: File size in bytes (for files)
- `sha`: Git SHA of the object
- `url`: GitHub API URL
- `children`: Child files/directories (for directories)

### RepositoryInfo
Repository metadata:
- `owner`: Repository owner
- `name`: Repository name
- `full_name`: Full repository name (owner/name)
- `description`: Repository description
- `default_branch`: Default branch name

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Invalid input parameters
- **404 Not Found**: Repository or file not found
- **500 Internal Server Error**: Server-side errors with detailed logging

All errors return structured `ErrorResponse` objects with:
- `error`: Error message
- `detail`: Additional error details
- `status_code`: HTTP status code

## Logging

The application logs all operations with different levels:
- **INFO**: Normal operations and successful requests
- **WARNING**: Non-critical issues (e.g., failed directory access)
- **ERROR**: Critical errors and exceptions

## Development

### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── models.py            # Pydantic data models
│   ├── github_service.py    # GitHub API integration service
│   ├── ai_service.py        # OpenRouter AI integration service
│   ├── utils.py             # Utility functions
│   └── routes/
│       ├── __init__.py
│       ├── github_routes.py # GitHub API endpoints
│       └── ai_routes.py     # AI test case generation endpoints
├── requirements.txt          # Python dependencies
├── test_setup.py            # Backend setup verification
├── test_ai_service.py       # AI service verification
└── README.md               # This file
```

### Adding New Routes

1. Create a new route file in `app/routes/`
2. Define your router with `APIRouter()`
3. Import and include it in `main.py`

### Testing

The API can be tested using:
- **Swagger UI**: http://localhost:8000/docs
- **curl**: Command-line HTTP client
- **Postman**: API testing tool
- **Any HTTP client**: The API is RESTful and stateless

## Next Steps

This backend implements **Phase 1: GitHub Integration** and **Phase 2: AI Test Case Summaries**. Future phases will include:
- **Phase 3**: Enhanced test case code generation and optimization
- **Phase 4**: Pull request creation and automated testing

## Troubleshooting

### Common Issues

1. **GitHub Token Error**: Ensure your token has the correct scopes and is valid
2. **Repository Access**: Verify the repository exists and is accessible with your token
3. **Rate Limiting**: GitHub API has rate limits; check the response headers for remaining requests

### Debug Mode

Set `DEBUG=True` in your `.env` file for detailed logging and auto-reload during development.

## License

This project is part of the Test Case Generator application.
