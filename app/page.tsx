'use client'

import { useState, useEffect } from 'react'

export default function Home() {
  const [message, setMessage] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const [downloading, setDownloading] = useState<boolean>(false)

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

  const [imageUrl, setImageUrl] = useState<string | null>(null)

  const loadImage = async () => {
    try {
      setDownloading(true)
      setError(null)
      // 直接使用圖片 URL
      const imageUrl = '/api/download-report'
      setImageUrl(imageUrl)
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '載入圖片失敗'
      setError(errorMsg)
      console.error('Load image error:', err)
    } finally {
      setDownloading(false)
    }
  }

  const downloadImage = async () => {
    try {
      if (!imageUrl) return
      
      setDownloading(true)
      const response = await fetch(imageUrl)
      
      if (!response.ok) {
        throw new Error(`下載失敗: ${response.status}`)
      }
      
      // 獲取圖片數據
      const blob = await response.blob()
      
      // 創建下載連結
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = '情蒐報告.jpg'
      document.body.appendChild(a)
      a.click()
      
      // 清理
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : '下載失敗'
      setError(errorMsg)
      console.error('Download error:', err)
    } finally {
      setDownloading(false)
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

        <div className="download-section">
          <h2>情蒐報告</h2>
          <button 
            onClick={loadImage} 
            disabled={downloading}
            className="download-button"
          >
            {downloading ? '載入中...' : '顯示情蒐報告'}
          </button>
          {error && (
            <div className="error" style={{ marginTop: '1rem', fontSize: '0.9rem' }}>
              <p>錯誤: {error}</p>
            </div>
          )}
          {imageUrl && (
            <div style={{ marginTop: '1rem' }}>
              <img 
                src={imageUrl} 
                alt="情蒐報告" 
                style={{ 
                  maxWidth: '100%', 
                  height: 'auto',
                  borderRadius: '8px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                  marginBottom: '1rem'
                }}
              />
              <button 
                onClick={downloadImage} 
                disabled={downloading}
                className="download-button"
                style={{ 
                  width: '100%',
                  marginTop: '0.5rem'
                }}
              >
                {downloading ? '下載中...' : '下載圖片'}
              </button>
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