'use client'

import { useState, useEffect } from 'react'

export default function Home() {
  const [message, setMessage] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchMessage()
  }, [])

  const fetchMessage = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch('/api')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const text = await response.text()
      setMessage(text)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch message')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container">
      <div className="content">
        <h1>Python Hello World with Next.js</h1>
        
        <div className="api-section">
          <h2>API Response:</h2>
          {loading && <p className="loading">載入中...</p>}
          {error && (
            <div className="error">
              <p>錯誤: {error}</p>
              <button onClick={fetchMessage}>重試</button>
            </div>
          )}
          {!loading && !error && (
            <div className="success">
              <p className="message">{message}</p>
              <button onClick={fetchMessage}>重新載入</button>
            </div>
          )}
        </div>

        <div className="info">
          <p>這個專案展示了如何在 Vercel 上整合 Next.js 前端與 Python Serverless Function。</p>
          <ul>
            <li>前端：Next.js 13+ App Router</li>
            <li>後端：Python Serverless Function (<code>/api</code>)</li>
          </ul>
        </div>
      </div>
    </main>
  )
}