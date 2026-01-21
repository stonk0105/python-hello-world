'use client'

import { useState, useEffect } from 'react'

export default function Home() {
  const [downloading, setDownloading] = useState<boolean>(false)
  const [imageUrl, setImageUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [selectedTeams, setSelectedTeams] = useState<Set<string>>(new Set())
  const [selectedRole, setSelectedRole] = useState<'pitcher' | 'batter'>('pitcher')
  const [players, setPlayers] = useState<any[]>([])
  const [loadingPlayers, setLoadingPlayers] = useState<boolean>(false)

  // 獲取所有球隊的完整列表（用於全選功能）
  const getAllTeams = () => {
    const allTeams: { code: string; name: string }[] = []
    Object.values(pools).forEach(teams => {
      allTeams.push(...teams)
    })
    return allTeams
  }

  // 處理球隊選擇
  const handleTeamToggle = (teamCode: string) => {
    const newSelected = new Set(selectedTeams)
    if (newSelected.has(teamCode)) {
      newSelected.delete(teamCode)
    } else {
      newSelected.add(teamCode)
    }
    setSelectedTeams(newSelected)
  }

  // 處理全選
  const handleSelectAll = (poolName: string) => {
    const poolTeams = pools[poolName as keyof typeof pools]
    const poolCodes = poolTeams.map(t => t.code)
    const allSelected = poolCodes.every(code => selectedTeams.has(code))
    
    const newSelected = new Set(selectedTeams)
    if (allSelected) {
      // 取消全選
      poolCodes.forEach(code => newSelected.delete(code))
    } else {
      // 全選
      poolCodes.forEach(code => newSelected.add(code))
    }
    setSelectedTeams(newSelected)
  }

  // 從資料庫獲取球員名單
  const fetchPlayers = async () => {
    if (selectedTeams.size === 0) {
      setPlayers([])
      return
    }

    try {
      setLoadingPlayers(true)
      const countries = Array.from(selectedTeams)
      const params = new URLSearchParams({
        countries: countries.join(','),
        role: selectedRole
      })
      
      const response = await fetch(`/api/get-players?${params.toString()}`)
      
      if (!response.ok) {
        // 嘗試解析錯誤響應
        let errorMessage = `獲取名單失敗: ${response.status}`
        try {
          const errorData = await response.json()
          console.error('API Error:', errorData)
          if (errorData.error) {
            errorMessage = `錯誤: ${errorData.error}`
            if (errorData.debug) {
              console.error('Debug info:', errorData.debug)
            }
          }
        } catch (e) {
          // 如果無法解析 JSON，使用默認錯誤信息
        }
        throw new Error(errorMessage)
      }
      
      const data = await response.json()
      setPlayers(data.players || [])
    } catch (err) {
      console.error('Fetch players error:', err)
      const errorMsg = err instanceof Error ? err.message : '獲取球員名單失敗，請稍後再試'
      alert(errorMsg)
      setPlayers([])
    } finally {
      setLoadingPlayers(false)
    }
  }

  // 當選擇的球隊或角色改變時，自動獲取名單
  useEffect(() => {
    fetchPlayers()
  }, [selectedTeams.size, selectedRole])

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

  const viewReport = async () => {
    try {
      setLoading(true)
      // 在 URL 後面加上時間戳，強制瀏覽器重新請求（避免快取）
      const timestamp = new Date().getTime()
      const imageUrl = `/api/download-report?t=${timestamp}`
      setImageUrl(imageUrl)
    } catch (err) {
      console.error('Load image error:', err)
      alert('載入圖片失敗，請稍後再試')
    } finally {
      setLoading(false)
    }
  }

  const downloadReport = async () => {
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
                <a 
                  href="#" 
                  className="select-all-link"
                  onClick={(e) => {
                    e.preventDefault()
                    handleSelectAll(poolName)
                  }}
                >
                  全選
                </a>
              </div>
              <div className="pool-teams">
                {teams.map((team) => (
                  <div key={team.code} className="team-item">
                    <input 
                      type="checkbox" 
                      id={team.code}
                      className="team-checkbox"
                      checked={selectedTeams.has(team.code)}
                      onChange={() => handleTeamToggle(team.code)}
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

        {/* 選擇角色 */}
        {selectedTeams.size > 0 && (
          <div className="statsinsight-role-selection" style={{ 
            marginTop: '2rem', 
            padding: '1.5rem', 
            background: '#f8f9fa', 
            borderRadius: '8px',
            border: '2px solid #e9ecef'
          }}>
            <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>選擇角色</h3>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <span style={{ fontWeight: '500' }}>
                {Array.from(selectedTeams).map(code => {
                  const team = getAllTeams().find(t => t.code === code)
                  return team?.name || code
                }).join(', ')}
              </span>
              <div style={{ display: 'flex', gap: '1rem', marginLeft: 'auto' }}>
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                  <input 
                    type="radio" 
                    name="role"
                    value="pitcher"
                    checked={selectedRole === 'pitcher'}
                    onChange={() => setSelectedRole('pitcher')}
                  />
                  <span>投手</span>
                </label>
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                  <input 
                    type="radio" 
                    name="role"
                    value="batter"
                    checked={selectedRole === 'batter'}
                    onChange={() => setSelectedRole('batter')}
                  />
                  <span>打者</span>
                </label>
              </div>
            </div>
          </div>
        )}

        {/* 球員名單 */}
        {selectedTeams.size > 0 && (
          <div className="statsinsight-players" style={{ 
            marginTop: '2rem', 
            padding: '1.5rem', 
            background: '#f8f9fa', 
            borderRadius: '8px',
            border: '2px solid #e9ecef'
          }}>
            <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>
              球員名單 {loadingPlayers && '(載入中...)'}
            </h3>
            {loadingPlayers ? (
              <p>載入中...</p>
            ) : players.length > 0 ? (
              <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
                <ul style={{ 
                  listStyle: 'none', 
                  padding: 0, 
                  margin: 0,
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
                  gap: '0.5rem'
                }}>
                  {players.map((player, index) => {
                    const playerName = player.球員 || `球員 ${index + 1}`
                    return (
                      <li key={index} style={{ 
                        padding: '0.5rem',
                        background: 'white',
                        borderRadius: '4px',
                        border: '1px solid #e9ecef'
                      }}>
                        {playerName}
                      </li>
                    )
                  })}
                </ul>
                <p style={{ marginTop: '1rem', color: '#666', fontSize: '0.875rem' }}>
                  共 {players.length} 位球員
                </p>
              </div>
            ) : (
              <p style={{ color: '#666' }}>沒有找到球員資料</p>
            )}
          </div>
        )}

        {/* View/Download Button */}
        <div className="statsinsight-download">
          {!imageUrl ? (
            <button 
              onClick={viewReport}
              disabled={loading}
              className="download-report-button"
            >
              {loading ? '載入中...' : '查看'}
            </button>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'center' }}>
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
                onClick={downloadReport}
                disabled={downloading}
                className="download-report-button"
                style={{ width: '200px' }}
              >
                {downloading ? '下載中...' : '下載報告'}
              </button>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}