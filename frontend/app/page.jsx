"use client"
import { useState, useEffect } from 'react'
import FileTree from '../components/FileTree'
import { summarizeTests, generateTest, checkBackendHealth } from '../lib/backend'

export default function HomePage() {
  const [owner, setOwner] = useState('')
  const [repo, setRepo] = useState('')
  const [framework, setFramework] = useState('selenium')
  const [selectedFiles, setSelectedFiles] = useState([])
  const [summaries, setSummaries] = useState([])
  const [loading, setLoading] = useState(false)
  const [connected, setConnected] = useState(false)
  const [generated, setGenerated] = useState('')

  // health ping
  useEffect(() => {
    let cancelled = false
    async function ping() {
      const ok = await checkBackendHealth()
      if (!cancelled) setConnected(ok)
    }
    ping()
    const id = setInterval(ping, 5000)
    return () => { cancelled = true; clearInterval(id) }
  }, [])

  const handleGenerateSummaries = async ({ owner, repo, paths }) => {
    setLoading(true)
    try {
      const res = await summarizeTests(owner, repo, paths, framework)
      setSummaries(res.summaries || [])
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen">
      <header className="border-b bg-white">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="font-semibold">AI-Powered Test Generation</div>
          <div className={`text-xs px-2 py-1 rounded-full ${connected ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
            {connected ? 'Connected' : 'Disconnected'}
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-8 space-y-8">
        <section className="bg-white rounded-xl border p-6 shadow-sm">
          <h2 className="font-semibold mb-4">Repository Configuration</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm text-slate-600">Repository Owner</label>
              <input value={owner} onChange={e=>setOwner(e.target.value)} placeholder="e.g., facebook" className="mt-1 w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-emerald-200 focus:outline-none" />
            </div>
            <div>
              <label className="text-sm text-slate-600">Repository Name</label>
              <input value={repo} onChange={e=>setRepo(e.target.value)} placeholder="e.g., react" className="mt-1 w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-emerald-200 focus:outline-none" />
            </div>
            <div>
              <label className="text-sm text-slate-600">Testing Framework</label>
              <select value={framework} onChange={e=>setFramework(e.target.value)} className="mt-1 w-full rounded-lg border px-3 py-2 focus:ring-2 focus:ring-emerald-200 focus:outline-none">
                <option value="selenium">selenium</option>
                <option value="pytest">pytest</option>
                <option value="unittest">unittest</option>
                <option value="jest">jest</option>
              </select>
            </div>
          </div>
        </section>

        <section className="bg-white rounded-xl border p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold">Repository Files</h2>
          </div>
          <FileTree
            owner={owner}
            repo={repo}
            onSelectedFilesChange={setSelectedFiles}
            onGenerateSummaries={handleGenerateSummaries}
          />
        </section>

        <section className="bg-white rounded-xl border p-6 shadow-sm">
          <h2 className="font-semibold mb-3">Test Case Generation</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              {!summaries.length ? (
                <div className="text-center py-10 text-slate-500 text-sm">No summaries yet<br/>Load files and click Generate Test Cases</div>
              ) : (
                <ul className="space-y-2">
                  {summaries.map(s => (
                    <li key={s.id} className="border rounded-lg p-3 text-sm flex items-center justify-between">
                      <span className="pr-2">{s.summary}</span>
                      <button
                        className="text-xs rounded-md bg-emerald-500 hover:bg-emerald-600 text-white px-2 py-1"
                        onClick={async () => {
                          setGenerated('')
                          setLoading(true)
                          try {
                            // Require owner/repo and at least one selected file; use the first file for code gen demo
                            // In a fuller UI you'd choose specific file + summary
                            const filePath = (selectedFiles?.[0])
                            if (!filePath) return
                            // fetch file content then generate code
                            // Reuse summarize path: we need /repos/file-contents
                            const contents = await (await import('../lib/backend')).fetchFileContents(owner, repo, [filePath])
                            const fileContent = contents[0]
                            const res = await generateTest(fileContent.path, fileContent.content, s.summary)
                            setGenerated(res.code || '')
                          } catch (e) {
                            setGenerated(`/* Failed to generate code: ${e?.message || e} */`)
                          } finally {
                            setLoading(false)
                          }
                        }}
                      >
                        Generate Code
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div>
              <div className="text-xs text-slate-500 mb-2">Output</div>
              <pre className="min-h-[240px] max-h-[420px] overflow-auto bg-slate-900 text-slate-100 rounded-lg p-3 text-xs whitespace-pre-wrap">
{generated || '/* Generated code will appear here */'}
              </pre>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}


