from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class FileType(str, Enum):
    """File type enumeration"""
    FILE = "file"
    DIR = "dir"
    SYMLINK = "symlink"
    SUBMODULE = "submodule"

class FileNode(BaseModel):
    """Represents a file or directory in the repository tree"""
    name: str = Field(..., description="Name of the file or directory")
    path: str = Field(..., description="Full path from repository root")
    type: FileType = Field(..., description="Type of the node")
    size: Optional[int] = Field(None, description="Size in bytes (for files)")
    sha: str = Field(..., description="Git SHA of the object")
    url: str = Field(..., description="GitHub API URL for the object")
    
    # For directories, we'll populate children
    children: Optional[List['FileNode']] = Field(None, description="Child files/directories")

class RepositoryInfo(BaseModel):
    """Repository information"""
    owner: str = Field(..., description="Repository owner")
    name: str = Field(..., description="Repository name")
    full_name: str = Field(..., description="Full repository name (owner/name)")
    description: Optional[str] = Field(None, description="Repository description")
    default_branch: str = Field(..., description="Default branch name")

class FileTreeResponse(BaseModel):
    """Response model for file tree endpoint"""
    repository: RepositoryInfo = Field(..., description="Repository information")
    files: List[FileNode] = Field(..., description="List of files and directories")
    total_count: int = Field(..., description="Total number of files and directories")

class FileContentRequest(BaseModel):
    """Request model for getting file contents"""
    owner: str = Field(..., description="Repository owner")
    repo: str = Field(..., description="Repository name")
    file_paths: List[str] = Field(..., description="List of file paths to fetch")

class FileContent(BaseModel):
    """File content information"""
    path: str = Field(..., description="File path")
    content: str = Field(..., description="File content (decoded)")
    encoding: str = Field(..., description="File encoding")
    size: int = Field(..., description="File size in bytes")
    sha: str = Field(..., description="Git SHA of the file")

class FileContentResponse(BaseModel):
    """Response model for file content endpoint"""
    files: List[FileContent] = Field(..., description="List of file contents")
    total_count: int = Field(..., description="Total number of files")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    status_code: int = Field(..., description="HTTP status code")

class GenerateTestRequest(BaseModel):
    """Request model for improved test generation"""
    file_name: str = Field(..., description="Name of the file to generate test for")
    file_content: str = Field(..., description="Content of the file")
    scenario: str = Field(..., description="Test case scenario to implement")

class GenerateTestResponse(BaseModel):
    """Response model for improved test generation"""
    code: str = Field(..., description="Generated test case code")
    file_name: str = Field(..., description="Name of the file")
    scenario: str = Field(..., description="Test case scenario")

# Update forward references
FileNode.model_rebuild()
