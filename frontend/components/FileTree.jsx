"use client"
import { useEffect, useMemo, useState } from 'react'
import classNames from 'classnames'
import { fetchRepoFiles, fetchFileContents } from '../lib/backend'

function Checkbox({ checked, onChange }) {
  return (
    <input
      type="checkbox"
      className="h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-400"
      checked={checked}
      onChange={e => onChange(e.target.checked)}
    />
  )
}

function TreeNode({ node, level, onToggle, onSelect, selectedMap }) {
  const isDir = node.type === 'dir'
  const isSelected = !isDir && !!selectedMap[node.path]
  return (
    <div className="text-sm">
      <div
        className={classNames(
          "flex items-center gap-2 px-2 py-1 rounded-md hover:bg-slate-50 cursor-pointer",
        )}
        style={{ paddingLeft: `${level * 16}px` }}
        onClick={() => isDir ? onToggle(node.path) : onSelect(node.path, !isSelected)}
      >
        {isDir ? (
          <span className="w-4 text-slate-500">{node.expanded ? '▾' : '▸'}</span>
        ) : (
          <Checkbox
            checked={isSelected}
            onChange={(v) => onSelect(node.path, v)}
          />
        )}
        <span className={classNames("truncate", isDir ? "font-medium text-slate-700" : "text-slate-700")}>{node.name}</span>
        {!isDir && (
          <span className="ml-auto text-[11px] text-slate-400">{node.size ? `${Math.round(node.size/1024)}KB` : ''}</span>
        )}
      </div>
      {isDir && node.expanded && node.children?.map(child => (
        <TreeNode key={child.path} node={child} level={level + 1} onToggle={onToggle} onSelect={onSelect} selectedMap={selectedMap} />
      ))}
    </div>
  )
}

export default function FileTree({ owner, repo, onSelectedFilesChange, onGenerateSummaries }) {
  const [tree, setTree] = useState([])
  const [loading, setLoading] = useState(false)
  const [selected, setSelected] = useState({})
  const [error, setError] = useState('')
  const hasSelection = useMemo(() => Object.values(selected).some(Boolean), [selected])

  useEffect(() => {
    onSelectedFilesChange?.(Object.keys(selected).filter(p => selected[p]))
  }, [selected, onSelectedFilesChange])

  const loadFiles = async () => {
    setError('')
    if (!owner || !repo) {
      setError('Please enter both owner and repository name')
      return
    }
    setLoading(true)
    try {
      const files = await fetchRepoFiles(owner.trim(), repo.trim())
      const treeBuilt = buildTree(files)
      setTree(treeBuilt)
      if (!treeBuilt.length) {
        setError('No files returned. Ensure the backend is running and the repository is public or accessible by the configured token.')
      }
    } catch (e) {
      console.error('Load files error:', e)
      setError(e?.message || 'Failed to load files')
    } finally {
      setLoading(false)
    }
  }

  const toggleDir = (path) => {
    setTree(prev => prev.map(n => toggleNode(n, path)))
  }

  const selectFile = (path, value) => {
    setSelected(prev => ({ ...prev, [path]: value }))
  }

  const handleSummarize = async () => {
    const paths = Object.keys(selected).filter(p => selected[p])
    if (!paths.length) return
    onGenerateSummaries?.({ owner, repo, paths })
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <div className="text-sm text-slate-500">Enter repository details to load the file tree</div>
        <button onClick={loadFiles} disabled={loading} className={classNames("inline-flex items-center gap-2 rounded-lg text-sm px-3 py-2", loading ? "bg-slate-200 text-slate-500" : "bg-emerald-500 hover:bg-emerald-600 text-white") }>
          <span>Load Files</span>
        </button>
      </div>

      {error && (
        <div className="mb-3 text-sm text-rose-700 bg-rose-50 border border-rose-200 rounded-lg px-3 py-2">{error}</div>
      )}

      <div className="border rounded-lg bg-white">
        {!tree.length ? (
          <div className="p-10 text-center text-slate-400 text-sm">{loading ? 'Loading…' : 'No files loaded'}</div>
        ) : (
          <div className="max-h-80 overflow-auto py-2">
            {tree.map(node => (
              <TreeNode key={node.path} node={node} level={0} onToggle={toggleDir} onSelect={selectFile} selectedMap={selected} />
            ))}
          </div>
        )}
      </div>

      <div className="mt-4 flex items-center justify-between">
        <div className="text-xs text-slate-500">{Object.keys(selected).filter(p => selected[p]).length} files selected</div>
        <button
          disabled={!hasSelection}
          onClick={handleSummarize}
          className={classNames(
            "inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm",
            hasSelection ? "bg-emerald-500 hover:bg-emerald-600 text-white" : "bg-slate-200 text-slate-500 cursor-not-allowed"
          )}
        >
          Generate Test Cases
        </button>
      </div>
    </div>
  )
}

// Helpers
function buildTree(files) {
  const root = []
  const map = {}

  for (const f of files) {
    const parts = f.path.split('/')
    let current = root
    let currentPath = ''
    for (let i = 0; i < parts.length; i++) {
      const name = parts[i]
      currentPath = currentPath ? `${currentPath}/${name}` : name
      const isLast = i === parts.length - 1
      if (isLast) {
        current.push({ name, path: currentPath, type: 'file', size: f.size })
      } else {
        let dir = current.find(n => n.type === 'dir' && n.name === name)
        if (!dir) {
          dir = { name, path: currentPath, type: 'dir', expanded: true, children: [] }
          current.push(dir)
        }
        current = dir.children
      }
    }
  }
  return root
}

function toggleNode(node, path) {
  if (node.path === path && node.type === 'dir') {
    return { ...node, expanded: !node.expanded }
  }
  if (node.type === 'dir' && node.children) {
    return { ...node, children: node.children.map(c => toggleNode(c, path)) }
  }
  return node
}


