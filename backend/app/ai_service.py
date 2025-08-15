import requests
import logging
from typing import List, Dict, Any, Optional
import json
import time

try:
	from .config import settings
	from .models import FileContent
except ImportError:
	from config import settings
	from models import FileContent

# Configure logging
logger = logging.getLogger(__name__)

class AIService:
	"""Service class for AI API operations (supports Gemini or OpenRouter)"""
	
	def __init__(self):
		"""Initialize AI service with selected provider"""
		self.provider = getattr(settings, "AI_PROVIDER", "openrouter").lower()
		if self.provider == "gemini":
			self.gemini_api_key = getattr(settings, "GEMINI_API_KEY", "")
			self.gemini_model = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")
			if not self.gemini_api_key:
				raise ValueError("GEMINI_API_KEY is missing. Add it to backend/.env")
			logger.info("AI Service initialized with Gemini API")
		else:
			self.api_key = getattr(settings, "OPENROUTER_API_KEY", "")
			self.base_url = getattr(settings, "OPENROUTER_API_BASE_URL", "https://openrouter.ai/api/v1")
			self.default_model = getattr(settings, "OPENROUTER_DEFAULT_MODEL", "openrouter/auto")
			if not self.api_key or not self.api_key.strip():
				raise ValueError("OPENROUTER_API_KEY is missing. Add it to backend/.env or set AI_PROVIDER=gemini")
			logger.info("AI Service initialized with OpenRouter API")
	
	def _make_openrouter_request(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> Dict[str, Any]:
		"""Make a request to OpenRouter API"""
		if not model:
			model = self.default_model
		headers = {
			"Authorization": f"Bearer {self.api_key}",
			"Content-Type": "application/json",
			"HTTP-Referer": "http://localhost:8000",
			"X-Title": "Test Case Generator"
		}
		
		payload = {
			"model": model,
			"messages": messages,
			"max_tokens": 4000,
			"temperature": 0.7
		}
		
		resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=30)
		resp.raise_for_status()
		return resp.json()
	
	def _make_gemini_request(self, messages: List[Dict[str, str]], model: Optional[str] = None) -> Dict[str, Any]:
		"""Make a request to Gemini Generative Language API"""
		if not model:
			model = self.gemini_model
		# Convert messages to Gemini contents (simple mapping)
		contents = []
		for m in messages:
			text = m.get("content", "")
			contents.append({"role": "user", "parts": [{"text": text}]})
		url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_api_key}"
		payload = {"contents": contents}
		resp = requests.post(url, json=payload, timeout=30)
		resp.raise_for_status()
		return resp.json()
	
	def _extract_json_from_response(self, response_text: str) -> List[Dict[str, Any]]:
		"""Extract JSON from AI response text"""
		try:
			# Try to find JSON in the response
			start_idx = response_text.find('[')
			end_idx = response_text.rfind(']') + 1
			
			if start_idx != -1 and end_idx != -1:
				json_str = response_text[start_idx:end_idx]
				return json.loads(json_str)
			else:
				# If no JSON array found, try to parse the entire response
				return json.loads(response_text)
		except json.JSONDecodeError as e:
			logger.warning(f"Failed to parse JSON from AI response: {e}")
			# Return a fallback response
			return [{"id": 1, "summary": "Failed to parse AI response"}]
	
	def generate_test_case_summaries(self, file_contents: List[FileContent], framework: str = "pytest") -> List[Dict[str, Any]]:
		"""
		Generate test case summaries for given file contents.
		
		Args:
			file_contents: List of file contents to analyze
			framework: Testing framework to target (default: pytest)
			
		Returns:
			List of test case summaries with id and summary
		"""
		try:
			# Prepare the prompt for test case summarization
			prompt = self._build_summary_prompt(file_contents, framework)
			
			messages = [
				{
					"role": "system",
					"content": "You are a test case generation assistant. Generate concise test case summaries in the exact JSON format requested."
				},
				{
					"role": "user",
					"content": prompt
				}
			]
			
			# Make API request
			if self.provider == "gemini":
				resp = self._make_gemini_request(messages)
				ai_response = resp.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "[]")
			else:
				resp = self._make_openrouter_request(messages)
				ai_response = resp["choices"][0]["message"]["content"]
			
			summaries = self._extract_json_from_response(ai_response)
			logger.info(f"Generated {len(summaries)} test case summaries for {len(file_contents)} files")
			return summaries
			
		except Exception as e:
			logger.error(f"Failed to generate test case summaries: {e}")
			raise
	
	def generate_test_case_code(self, file_content: FileContent, summary: str, framework: str = "pytest") -> str:
		"""
		Generate complete test case code for a given summary.
		
		Args:
			file_content: File content to generate test for
			summary: Test case summary to implement
			framework: Testing framework to target (default: pytest)
			
		Returns:
			Generated test case code as string
		"""
		try:
			# Prepare the prompt for code generation
			prompt = self._build_code_prompt(file_content, summary, framework)
			
			messages = [
				{
					"role": "system",
					"content": "You are a test case code generator. Generate complete, runnable test code in the specified framework."
				},
				{
					"role": "user",
					"content": prompt
				}
			]
			
			# Make API request
			if self.provider == "gemini":
				resp = self._make_gemini_request(messages)
				generated_code = resp.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
			else:
				resp = self._make_openrouter_request(messages)
				generated_code = resp["choices"][0]["message"]["content"]
			
			logger.info(f"Generated test case code for: {summary}")
			return generated_code
			
		except Exception as e:
			logger.error(f"Failed to generate test case code: {e}")
			raise
	
	def generate_test_code_improved(self, file_name: str, file_content: str, scenario: str) -> str:
		"""
		Generate complete pytest test code using the improved prompt.
		
		Args:
			file_name: Name of the file to generate test for
			file_content: Content of the file
			scenario: Test case scenario to implement
			
		Returns:
			Generated test case code as string
		"""
		try:
			# Use the improved prompt
			prompt = f"""
You are an expert software test engineer.
I will give you a Python source file and a specific test case scenario.

**Task:**
Generate a complete **pytest** test function for the given scenario **without any placeholders or TODO comments**.
The test should include:
- Realistic example inputs
- Expected outputs based on the provided code logic
- Assertions verifying correctness
- Import statements if needed

**Rules:**
- Use descriptive test function names based on the file name and scenario
- Do NOT leave implementation details as TODO
- Ensure the test is runnable as-is
- If the function interacts with external APIs or files, mock them

**Python File Name:** `{file_name}`

**Scenario:** {scenario}

**Source Code:**
```
{file_content}
```

Now, generate the complete pytest test code for the above scenario.
			"""

			messages = [
				{
					"role": "system",
					"content": "You are an expert software test engineer specializing in pytest. Generate complete, runnable test code without any placeholders or TODO comments."
				},
				{
					"role": "user",
					"content": prompt
				}
			]
			
			# Make API request
			if self.provider == "gemini":
				resp = self._make_gemini_request(messages)
				generated_code = resp.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
			else:
				resp = self._make_openrouter_request(messages)
				generated_code = resp["choices"][0]["message"]["content"]
			
			logger.info(f"Generated improved test case code for: {scenario}")
			return generated_code
			
		except Exception as e:
			logger.error(f"Failed to generate improved test case code: {e}")
			raise
	
	def _build_summary_prompt(self, file_contents: List[FileContent], framework: str) -> str:
		"""Build the prompt for test case summarization"""
		prompt = f"""You are a test case generation assistant.
Given the following source code, suggest potential test cases in {framework.upper()}.
Return an array of JSON objects with:
- id: integer (starting from 1)
- summary: short description of the test case

Source Code:
"""
		
		for file_content in file_contents:
			prompt += f"\n--- File: {file_content.path} ---\n"
			prompt += file_content.content[:2000]  # Limit content length
			if len(file_content.content) > 2000:
				prompt += "\n... (content truncated)"
			prompt += "\n"
		
		prompt += f"\nGenerate 3-5 test case summaries for {framework.upper()} in this exact JSON format:\n"
		prompt += """[
  {"id": 1, "summary": "Test function with valid input"},
  {"id": 2, "summary": "Test function with invalid input"},
  {"id": 3, "summary": "Test edge case scenario"}
]"""
		
		return prompt
	
	def _build_code_prompt(self, file_content: FileContent, summary: str, framework: str) -> str:
		"""Build the prompt for test case code generation"""
		prompt = f"""You are a {framework.upper()} test case generator.
Given the following source code and selected test case summary, generate the complete test case code.

Source Code:
--- File: {file_content.path} ---
{file_content.content[:3000]}  # Limit content length

Selected Test Case Summary:
{summary}

Generate a complete, runnable {framework.upper()} test case that:
1. Imports necessary modules
2. Sets up test fixtures if needed
3. Implements the test logic
4. Uses proper assertions
5. Follows {framework.upper()} best practices

Special instructions when framework is SELENIUM:
- Use Python Selenium (selenium.webdriver) with a headless Chrome WebDriver
- Provide a pytest fixture named `driver` that sets up and tears down the WebDriver
- Use WebDriverWait and expected_conditions; avoid arbitrary sleeps
- Target realistic interactions (find elements, click, type, assert text/URL)
- Return only executable pytest test code using Selenium

Return only the test code, no explanations."""
		
		return prompt
	
	def test_connection(self) -> Dict[str, Any]:
		"""Perform a minimal real call to verify API key works and return output."""
		try:
			messages = [
				{"role": "system", "content": "You are a helpful assistant."},
				{"role": "user", "content": "Reply with the word: pong"}
			]
			if self.provider == "gemini":
				resp = self._make_gemini_request(messages)
				content = resp.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
				model_used = self.gemini_model
			else:
				resp = self._make_openrouter_request(messages)
				content = resp.get("choices", [{}])[0].get("message", {}).get("content", "")
				model_used = resp.get("model") or self.default_model
			return {"ok": True, "model": model_used, "output": content}
		except Exception as e:
			logger.error(f"AI connection test failed: {e}")
			return {"ok": False, "error": str(e)}
