from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import logging

try:
    from ..ai_service import AIService
    from ..models import FileContent, FileContentRequest, GenerateTestRequest, GenerateTestResponse
except ImportError:
    from ai_service import AIService
    from models import FileContent, FileContentRequest, GenerateTestRequest, GenerateTestResponse

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/ai", tags=["AI"])

def get_ai_service() -> AIService:
    """Dependency to get AI service instance"""
    return AIService()

@router.post("/summarize-tests")
async def summarize_tests(
    request: FileContentRequest,
    framework: str = "pytest",
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Generate test case summaries for the given file contents.
    
    Args:
        request: FileContentRequest with owner, repo, and file paths
        framework: Testing framework to target (default: pytest)
        ai_service: AI service instance
    
    Returns:
        List of test case summaries with id and summary
    """
    try:
        # This endpoint requires file contents to be fetched from GitHub first
        # For now, return an error indicating this endpoint needs file contents
        raise HTTPException(
            status_code=400,
            detail="This endpoint requires file contents. Use /summarize-tests-with-content instead."
        )
        
    except Exception as e:
        logger.error(f"Error generating test case summaries: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test case summaries: {str(e)}"
        )

@router.post("/summarize-tests-with-content")
async def summarize_tests_with_content(
    file_contents: List[FileContent],
    framework: str = "pytest",
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Generate test case summaries for the given file contents.
    This endpoint accepts the actual file contents directly.
    
    Args:
        file_contents: List of file contents to analyze
        framework: Testing framework to target (default: pytest)
        ai_service: AI service instance
    
    Returns:
        List of test case summaries with id and summary
    """
    try:
        if not file_contents:
            raise HTTPException(
                status_code=400,
                detail="No file contents provided"
            )
        
        # Generate test case summaries using AI service
        summaries = ai_service.generate_test_case_summaries(file_contents, framework)
        
        return {
            "summaries": summaries,
            "framework": framework,
            "total_count": len(summaries),
            "files_analyzed": len(file_contents)
        }
        
    except Exception as e:
        logger.error(f"Error generating test case summaries: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test case summaries: {str(e)}"
        )

@router.post("/generate-code")
async def generate_test_code(
    file_content: FileContent,
    summary: str,
    framework: str = "pytest",
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Generate complete test case code for a given summary.
    
    Args:
        file_content: File content to generate test for
        summary: Test case summary to implement
        framework: Testing framework to target (default: pytest)
        ai_service: AI service instance
    
    Returns:
        Generated test case code
    """
    try:
        if not summary:
            raise HTTPException(
                status_code=400,
                detail="Test case summary is required"
            )
        
        # Generate test case code using AI service
        generated_code = ai_service.generate_test_case_code(file_content, summary, framework)
        
        return {
            "code": generated_code,
            "summary": summary,
            "framework": framework,
            "file_path": file_content.path
        }
        
    except Exception as e:
        logger.error(f"Error generating test case code: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test case code: {str(e)}"
        )

@router.post("/generate-test")
async def generate_test(
    request: GenerateTestRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Generate complete pytest test code using the improved prompt.
    
    Args:
        request: GenerateTestRequest with file_name, file_content, and scenario
        ai_service: AI service instance
    
    Returns:
        Generated test case code
    """
    try:
        if not request.scenario:
            raise HTTPException(
                status_code=400,
                detail="Test case scenario is required"
            )
        
        if not request.file_content:
            raise HTTPException(
                status_code=400,
                detail="File content is required"
            )
        
        # Generate test case code using the improved AI service method
        generated_code = ai_service.generate_test_code_improved(
            request.file_name,
            request.file_content,
            request.scenario
        )
        
        return GenerateTestResponse(
            code=generated_code,
            file_name=request.file_name,
            scenario=request.scenario
        )
        
    except Exception as e:
        logger.error(f"Error generating improved test case code: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test case code: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for AI service"""
    return {"status": "healthy", "service": "AI Test Case Generator"}

@router.get("/test-connection")
async def test_ai_connection(
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Perform a minimal real LLM call to verify API key works.
    """
    try:
        result = ai_service.test_connection()
        if result.get("ok"):
            return {"status": "connected", "mode": "live", **result}
        raise HTTPException(status_code=502, detail=result.get("error", "LLM call failed"))
    except Exception as e:
        logger.error(f"Error testing AI connection: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to test AI connection: {str(e)}")

@router.get("/supported-frameworks")
async def get_supported_frameworks():
    """Get list of supported testing frameworks"""
    return {
        "frameworks": [
            {
                "name": "pytest",
                "description": "Python testing framework",
                "language": "Python"
            },
            {
                "name": "selenium",
                "description": "Python UI automation testing with Selenium",
                "language": "Python"
            },
            {
                "name": "jest",
                "description": "JavaScript testing framework",
                "language": "JavaScript/TypeScript"
            },
            {
                "name": "unittest",
                "description": "Python built-in testing framework",
                "language": "Python"
            },
            {
                "name": "mocha",
                "description": "JavaScript testing framework",
                "language": "JavaScript/TypeScript"
            },
            {
                "name": "junit",
                "description": "Java testing framework",
                "language": "Java"
            }
        ],
        "total_count": 5
    }
