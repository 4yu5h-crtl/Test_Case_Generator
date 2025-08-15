from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

try:
    from ..github_service import GitHubService
    from ..models import (
        FileTreeResponse, 
        FileContentRequest, 
        FileContentResponse,
        RepositoryInfo,
        FileNode,
        ErrorResponse
    )
except ImportError:
    from github_service import GitHubService
    from models import (
        FileTreeResponse, 
        FileContentRequest, 
        FileContentResponse,
        RepositoryInfo,
        FileNode,
        ErrorResponse
    )

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/repos", tags=["GitHub"])

def get_github_service() -> GitHubService:
    """Dependency to get GitHub service instance"""
    try:
        return GitHubService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{owner}/{repo}/files", response_model=FileTreeResponse)
async def get_repository_files(
    owner: str,
    repo: str,
    github_service: GitHubService = Depends(get_github_service)
):
    """
    Get file tree for a repository.
    
    Args:
        owner: Repository owner username
        repo: Repository name
        github_service: GitHub service instance
    
    Returns:
        FileTreeResponse with repository info and file tree
    """
    try:
        # Get repository information
        repo_info = github_service.get_repository_info(owner, repo)
        
        # Get file tree
        files = github_service.get_file_tree(owner, repo)
        
        # Count total files and directories
        total_count = len(files)
        
        return FileTreeResponse(
            repository=repo_info,
            files=files,
            total_count=total_count
        )
        
    except Exception as e:
        logger.error(f"Error getting repository files for {owner}/{repo}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get repository files: {str(e)}"
        )

@router.post("/file-contents", response_model=FileContentResponse)
async def get_file_contents(
    request: FileContentRequest,
    github_service: GitHubService = Depends(get_github_service)
):
    """
    Get contents of multiple files from a repository.
    
    Args:
        request: FileContentRequest with owner, repo, and file paths
        github_service: GitHub service instance
    
    Returns:
        FileContentResponse with file contents
    """
    try:
        # Get file contents
        file_contents = github_service.get_multiple_file_contents(
            request.owner,
            request.repo,
            request.file_paths
        )
        
        return FileContentResponse(
            files=file_contents,
            total_count=len(file_contents)
        )
        
    except Exception as e:
        logger.error(f"Error getting file contents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get file contents: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "GitHub API"}

@router.get("/test-connection")
async def test_github_connection(
    github_service: GitHubService = Depends(get_github_service)
):
    """
    Test GitHub API connection.
    
    Args:
        github_service: GitHub service instance
    
    Returns:
        Connection status
    """
    try:
        is_connected = github_service.test_connection()
        if is_connected:
            return {"status": "connected", "message": "GitHub API connection successful"}
        else:
            raise HTTPException(status_code=500, detail="GitHub API connection failed")
    except Exception as e:
        logger.error(f"Error testing GitHub connection: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to test GitHub connection: {str(e)}"
        )
