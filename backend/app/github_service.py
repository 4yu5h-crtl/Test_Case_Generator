from github import Github, GithubException
from typing import List, Optional, Dict, Any
import base64
import logging

try:
    from .config import settings
    from .models import FileNode, FileType, RepositoryInfo, FileContent
except ImportError:
    from config import settings
    from models import FileNode, FileType, RepositoryInfo, FileContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubService:
    """Service class for GitHub API operations"""
    
    def __init__(self):
        """Initialize GitHub service with authentication token"""
        if not settings.GITHUB_TOKEN:
            raise ValueError("GitHub token is required. Please set GITHUB_TOKEN environment variable.")
        
        self.github = Github(settings.GITHUB_TOKEN)
        self._authenticated_user = None
    
    def _get_authenticated_user(self):
        """Get the authenticated user information"""
        if not self._authenticated_user:
            try:
                self._authenticated_user = self.github.get_user()
                logger.info(f"Authenticated as: {self._authenticated_user.login}")
            except GithubException as e:
                logger.error(f"Failed to authenticate with GitHub: {e}")
                raise
        return self._authenticated_user
    
    def get_repository_info(self, owner: str, repo_name: str) -> RepositoryInfo:
        """Get repository information"""
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            return RepositoryInfo(
                owner=owner,
                name=repo_name,
                full_name=repo.full_name,
                description=repo.description,
                default_branch=repo.default_branch
            )
        except GithubException as e:
            logger.error(f"Failed to get repository info for {owner}/{repo_name}: {e}")
            raise
    
    def get_file_tree(self, owner: str, repo_name: str, path: str = "") -> List[FileNode]:
        """Get file tree for a repository path"""
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            if path:
                contents = repo.get_contents(path)
            else:
                contents = repo.get_contents("")
            
            file_nodes = []
            
            for content in contents:
                node = FileNode(
                    name=content.name,
                    path=content.path,
                    type=FileType(content.type),
                    size=getattr(content, 'size', None),
                    sha=content.sha,
                    url=content.url,
                    children=None
                )
                
                # If it's a directory, recursively get its contents
                if content.type == "dir":
                    try:
                        children = self.get_file_tree(owner, repo_name, content.path)
                        node.children = children
                    except Exception as e:
                        logger.warning(f"Failed to get contents for directory {content.path}: {e}")
                        node.children = []
                
                file_nodes.append(node)
            
            return file_nodes
            
        except GithubException as e:
            logger.error(f"Failed to get file tree for {owner}/{repo_name}/{path}: {e}")
            raise
    
    def get_file_content(self, owner: str, repo_name: str, file_path: str) -> FileContent:
        """Get content of a specific file"""
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            content = repo.get_contents(file_path)
            
            # Decode content based on encoding
            if content.encoding == "base64":
                decoded_content = base64.b64decode(content.content).decode('utf-8')
            else:
                decoded_content = content.content
            
            return FileContent(
                path=content.path,
                content=decoded_content,
                encoding=content.encoding,
                size=content.size,
                sha=content.sha
            )
            
        except GithubException as e:
            logger.error(f"Failed to get file content for {owner}/{repo_name}/{file_path}: {e}")
            raise
    
    def get_multiple_file_contents(self, owner: str, repo_name: str, file_paths: List[str]) -> List[FileContent]:
        """Get contents of multiple files"""
        file_contents = []
        
        for file_path in file_paths:
            try:
                content = self.get_file_content(owner, repo_name, file_path)
                file_contents.append(content)
            except Exception as e:
                logger.error(f"Failed to get content for {file_path}: {e}")
                # Continue with other files even if one fails
                continue
        
        return file_contents
    
    def test_connection(self) -> bool:
        """Test GitHub API connection"""
        try:
            user = self._get_authenticated_user()
            logger.info(f"GitHub connection successful. Authenticated as: {user.login}")
            return True
        except Exception as e:
            logger.error(f"GitHub connection failed: {e}")
            return False
