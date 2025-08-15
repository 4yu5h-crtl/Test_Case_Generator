import axios from 'axios'

const BASE = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000/api/v1'

export async function fetchRepoFiles(owner, repo) {
  if (!owner || !repo) {
    throw new Error('Owner and repository name are required')
  }
  
  const url = `${BASE}/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/files`
  try {
    const res = await axios.get(url, { timeout: 8000 })
    // Backend returns { repository, files: FileNode[], total_count }
    const nodes = res.data?.files || []
    return flattenFiles(nodes)
  } catch (err) {
    throw normalizeAxiosError(err)
  }
}

export async function fetchFileContents(owner, repo, paths) {
  if (!owner || !repo) {
    throw new Error('Owner and repository name are required')
  }
  if (!paths || !Array.isArray(paths) || paths.length === 0) {
    throw new Error('File paths array is required and must not be empty')
  }
  
  const url = `${BASE}/repos/file-contents`
  try {
    const res = await axios.post(url, { owner, repo, file_paths: paths }, { timeout: 15000 })
    return res.data?.files || res.data || []
  } catch (err) {
    throw normalizeAxiosError(err)
  }
}

export async function summarizeTestsWithContent(fileContents, framework = 'pytest') {
  if (!fileContents || !Array.isArray(fileContents) || fileContents.length === 0) {
    throw new Error('File contents array is required and must not be empty')
  }
  
  const url = `${BASE}/ai/summarize-tests-with-content?framework=${encodeURIComponent(framework)}`
  try {
    const res = await axios.post(url, fileContents, { timeout: 60000 })
    return res.data
  } catch (err) {
    throw normalizeAxiosError(err)
  }
}

export async function summarizeTests(owner, repo, paths, framework = 'pytest') {
  if (!owner || !repo) {
    throw new Error('Owner and repository name are required')
  }
  if (!paths || !Array.isArray(paths) || paths.length === 0) {
    throw new Error('File paths array is required and must not be empty')
  }
  
  try {
    // First, fetch the file contents from GitHub
    const fileContents = await fetchFileContents(owner, repo, paths)
    
    // Then, use the summarize-tests-with-content endpoint
    const url = `${BASE}/ai/summarize-tests-with-content?framework=${encodeURIComponent(framework)}`
    const res = await axios.post(url, fileContents, { timeout: 60000 })
    return res.data
  } catch (err) {
    throw normalizeAxiosError(err)
  }
}

export async function generateCode(fileContent, summary, framework = 'pytest') {
  if (!fileContent) {
    throw new Error('File content is required')
  }
  if (!summary) {
    throw new Error('Summary is required')
  }
  
  const url = `${BASE}/ai/generate-code?summary=${encodeURIComponent(summary)}&framework=${encodeURIComponent(framework)}`
  try {
    const res = await axios.post(url, fileContent, { timeout: 60000 })
    return res.data
  } catch (err) {
    throw normalizeAxiosError(err)
  }
}

export async function generateTest(fileName, fileContent, scenario) {
  if (!fileName) {
    throw new Error('File name is required')
  }
  if (!fileContent) {
    throw new Error('File content is required')
  }
  if (!scenario) {
    throw new Error('Scenario is required')
  }
  
  const url = `${BASE}/ai/generate-test`
  try {
    const res = await axios.post(url, {
      file_name: fileName,
      file_content: fileContent,
      scenario: scenario
    }, { timeout: 60000 })
    return res.data
  } catch (err) {
    throw normalizeAxiosError(err)
  }
}

export async function checkBackendHealth() {
  const baseRoot = BASE.endsWith('/api/v1') ? BASE.slice(0, -7) : BASE
  const candidates = [
    `${baseRoot}/health`,
    `${BASE}/repos/health`,
    `${BASE}/ai/health`,
  ]
  for (const url of candidates) {
    try {
      const res = await axios.get(url, { timeout: 3000 })
      if (res.status === 200) return true
    } catch (err) {
      // Log the error for debugging but continue to next candidate
      console.debug(`Health check failed for ${url}:`, err?.message || err)
      // try next
    }
  }
  return false
}

function normalizeAxiosError(err) {
  // Handle axios response errors
  if (err?.response) {
    const status = err.response.status || 'Unknown'
    const statusText = err.response.statusText || 'Unknown Error'
    const data = err.response.data
    
    // If there's error data from the backend, use it
    if (data && typeof data === 'object') {
      const detail = data.detail || data.message || data.error || data.msg
      if (detail && typeof detail === 'string' && detail.trim()) {
        return new Error(detail.trim())
      }
    } else if (data && typeof data === 'string' && data.trim()) {
      // If data is a string, use it directly
      return new Error(data.trim())
    }
    
    return new Error(`${status} ${statusText}`)
  }
  
  // Handle network errors (no response received)
  if (err?.request) {
    return new Error('Network error: backend unreachable')
  }
  
  // Handle other errors
  if (err?.message) {
    return new Error(err.message)
  }
  
  // Handle case where err might be null, undefined, or not an object
  if (!err) {
    return new Error('Unknown error occurred')
  }
  
  // If err is not an object, convert it to string
  if (typeof err !== 'object') {
    return new Error(String(err))
  }
  
  return new Error('Unknown error occurred')
}

function flattenFiles(nodes, prefix = '') {
  if (!nodes || !Array.isArray(nodes)) {
    return []
  }
  
  const files = []
  const walk = (n, pfx) => {
    for (const node of n) {
      if (!node || typeof node !== 'object') {
        continue // Skip invalid nodes
      }
      
      const full = pfx ? `${pfx}/${node.name}` : node.name
      const nodeType = node.type || node.file_type
      if (nodeType === 'file') {
        files.push({ path: node.path || full, size: node.size || 0 })
      } else if (nodeType === 'dir' || nodeType === 'directory' || node.children) {
        walk(node.children || [], full)
      }
    }
  }
  walk(nodes, prefix)
  return files
}


