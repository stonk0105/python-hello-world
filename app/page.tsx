'use client'

import { useState } from 'react'

export default function Home() {
  const [downloading, setDownloading] = useState<boolean>(false)

  const pools = {
    'Pool A': [
      { code: 'CA CAN', name: 'Canada' },
      { code: 'CO COL', name: 'Colombia' },
      { code: 'CU CUB', name: 'Cuba' },
      { code: 'PA PAN', name: 'Panama' },
      { code: 'PR PUR', name: 'Puerto Rico' }
    ],
    'Pool B': [
      { code: 'GB GBR', name: 'Great Britain' },
      { code: 'IT ITA', name: 'Italy' },
      { code: 'MX MEX', name: 'Mexico' },
      { code: 'US USA', name: 'United States of America' },
      { code: 'BR BRA', name: 'Brazil' }
    ],
    'Pool C': [
      { code: 'AU AUS', name: 'Australia' },
      { code: 'CZ CZE', name: 'Czech Republic' },
      { code: 'JP JPN', name: 'Japan' },
      { code: 'KR KOR', name: 'South Korea' }
    ],
    'Pool D': [
      { code: 'DO DOM', name: 'Dominican Republic' },
      { code: 'IL ISR', name: 'Israel' },
      { code: 'NL NLD', name: 'Netherlands' },
      { code: 'NI NIC', name: 'Nicaragua' },
      { code: 'VE VEN', name: 'Venezuela' }
    ]
  }

  const downloadReport = async () => {
    try {
      setDownloading(true)
      const response = await fetch('/api/download-report')
      
      if (!response.ok) {
        throw new Error(`下載失敗: ${response.status}`)
      }
      
      // 獲取圖片數據
      const blob = await response.blob()
      
      // 創建下載連結
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = '情蒐報告.png'
      document.body.appendChild(a)
      a.click()
      
      // 清理
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      console.error('Download error:', err)
      alert('下載失敗，請稍後再試')
    } finally {
      setDownloading(false)
    }
  }

  return (
    <main className="statsinsight-container">
      <div className="statsinsight-content">
        {/* Header */}
        <header className="statsinsight-header">
          <div className="statsinsight-logo">
            <div className="logo-circle">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                <path d="M3 3v18h18M7 16l4-8 4 8 4-12"/>
              </svg>
            </div>
          </div>
          <div className="statsinsight-title">
            <h1>StatsInsight</h1>
            <p>灼見運動數據</p>
          </div>
        </header>

        {/* Instructions */}
        <p className="statsinsight-instruction">
          請先選擇球隊,然後為每支球隊選擇要下載的打者或投手報告。
        </p>

        {/* Search Bar */}
        <div className="statsinsight-search">
          <input 
            type="text" 
            placeholder="搜尋球隊..." 
            className="search-input"
          />
        </div>

        {/* Team Pools */}
        <div className="statsinsight-pools">
          {Object.entries(pools).map(([poolName, teams]) => (
            <div key={poolName} className="pool-column">
              <div className="pool-header">
                <h3>{poolName}</h3>
                <a href="#" className="select-all-link">全選</a>
              </div>
              <div className="pool-teams">
                {teams.map((team) => (
                  <div key={team.code} className="team-item">
                    <input 
                      type="checkbox" 
                      id={team.code}
                      className="team-checkbox"
                    />
                    <label htmlFor={team.code} className="team-label">
                      <span className="team-code">{team.code}</span>
                      <span className="team-name">{team.name}</span>
                    </label>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Download Button */}
        <div className="statsinsight-download">
          <button 
            onClick={downloadReport}
            disabled={downloading}
            className="download-report-button"
          >
            {downloading ? '下載中...' : '下載報告'}
          </button>
        </div>
      </div>
    </main>
  )
}