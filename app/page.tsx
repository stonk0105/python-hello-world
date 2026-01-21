'use client'

import { useState, useEffect } from 'react'

export default function Home() {
  const [downloading, setDownloading] = useState<boolean>(false)
  const [imageUrl, setImageUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [selectedTeams, setSelectedTeams] = useState<Set<string>>(new Set())
  const [selectedRoles, setSelectedRoles] = useState<Set<'pitcher' | 'batter'>>(new Set(['pitcher']))
  // 球員名單快取：{ teamCode: { pitcher: string[], batter: string[] } }
  const [playersCache, setPlayersCache] = useState<Record<string, { pitcher: string[], batter: string[] }>>({})
  const [loadingPlayers, setLoadingPlayers] = useState<boolean>(false)

  // 獲取所有球隊的完整列表（用於全選功能）
  const getAllTeams = () => {
    const allTeams: { code: string; name: string }[] = []
    Object.values(pools).forEach(teams => {
      allTeams.push(...teams)
    })
    return allTeams
  }

  // 載入單個球隊的球員名單
  const loadTeamPlayers = async (teamCode: string, role: 'pitcher' | 'batter', forceReload: boolean = false) => {
    // 檢查快取
    if (!forceReload && playersCache[teamCode] && playersCache[teamCode][role]?.length > 0) {
      return // 已存在快取，不需要重新載入
    }

    try {
      const params = new URLSearchParams({
        team: teamCode,
        role: role
      })
      
      const response = await fetch(`/api/get-players?${params.toString()}`)
      
      if (!response.ok) {
        console.error(`獲取${teamCode}的${role === 'pitcher' ? '投手' : '打者'}名單失敗: ${response.status}`)
        return
      }
      
      const data = await response.json()
      if (data.players && Array.isArray(data.players)) {
        // 更新快取
        setPlayersCache(prev => ({
          ...prev,
          [teamCode]: {
            ...prev[teamCode],
            [role]: data.players
          }
        }))
      }
    } catch (err) {
      console.error(`載入${teamCode}的${role === 'pitcher' ? '投手' : '打者'}名單失敗:`, err)
    }
  }

  // 處理球隊選擇
  const handleTeamToggle = (teamCode: string) => {
    const newSelected = new Set(selectedTeams)
    if (newSelected.has(teamCode)) {
      // 取消選擇
      newSelected.delete(teamCode)
    } else {
      // 選擇球隊時，自動載入該球隊的所有角色名單
      newSelected.add(teamCode)
      // 載入打者名單
      loadTeamPlayers(teamCode, 'batter', true)
      // 載入投手名單
      loadTeamPlayers(teamCode, 'pitcher', true)
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

  // 處理角色選擇（checkbox）
  const handleRoleToggle = (role: 'pitcher' | 'batter') => {
    const newSelected = new Set(selectedRoles)
    if (newSelected.has(role)) {
      newSelected.delete(role)
    } else {
      newSelected.add(role)
    }
    // 至少保留一個角色
    if (newSelected.size === 0) {
      return
    }
    setSelectedRoles(newSelected)
  }

  // 當角色改變時，確保已選擇的球隊都有載入該角色的名單
  useEffect(() => {
    if (selectedTeams.size === 0 || selectedRoles.size === 0) {
      return
    }

    // 為每個選中的球隊和角色載入名單（如果尚未載入）
    Array.from(selectedTeams).forEach(teamCode => {
      Array.from(selectedRoles).forEach(role => {
        if (!playersCache[teamCode] || !playersCache[teamCode][role] || playersCache[teamCode][role].length === 0) {
          loadTeamPlayers(teamCode, role, false)
        }
      })
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedTeams.size, selectedRoles.size])

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
                    type="checkbox"
                    checked={selectedRoles.has('pitcher')}
                    onChange={() => handleRoleToggle('pitcher')}
                  />
                  <span>投手</span>
                </label>
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                  <input 
                    type="checkbox"
                    checked={selectedRoles.has('batter')}
                    onChange={() => handleRoleToggle('batter')}
                  />
                  <span>打者</span>
                </label>
              </div>
            </div>
          </div>
        )}

        {/* 球員名單 */}
        {selectedTeams.size > 0 && selectedRoles.size > 0 && (
          <div className="statsinsight-players" style={{ 
            marginTop: '2rem', 
            padding: '1.5rem', 
            background: '#f8f9fa', 
            borderRadius: '8px',
            border: '2px solid #e9ecef'
          }}>
            {loadingPlayers ? (
              <p>載入中...</p>
            ) : (
              <>
                {Array.from(selectedTeams).map(teamCode => {
                  const team = getAllTeams().find(t => t.code === teamCode)
                  const teamName = team?.name || teamCode
                  
                  return Array.from(selectedRoles).map(role => {
                    const roleText = role === 'pitcher' ? '投手' : '打者'
                    const rolePlayers = playersCache[teamCode]?.[role] || []
                    
                    if (rolePlayers.length === 0) return null
                    
                    return (
                      <div key={`${teamCode}-${role}`} style={{ marginBottom: '2rem' }}>
                        <div style={{ 
                          display: 'flex', 
                          justifyContent: 'space-between', 
                          alignItems: 'center',
                          marginBottom: '1rem'
                        }}>
                          <h3 style={{ fontSize: '1.1rem', margin: 0 }}>
                            {teamCode} - {roleText}
                          </h3>
                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <a 
                              href="#" 
                              onClick={(e) => {
                                e.preventDefault()
                                // TODO: 實現全選功能
                              }}
                              style={{ fontSize: '0.875rem', color: '#007bff' }}
                            >
                              全選
                            </a>
                            <span> / </span>
                            <a 
                              href="#" 
                              onClick={(e) => {
                                e.preventDefault()
                                // TODO: 實現取消全選功能
                              }}
                              style={{ fontSize: '0.875rem', color: '#007bff' }}
                            >
                              取消全選
                            </a>
                          </div>
                        </div>
                        <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
                          <ul style={{ 
                            listStyle: 'none', 
                            padding: 0, 
                            margin: 0,
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
                            gap: '0.5rem'
                          }}>
                            {rolePlayers.map((playerName, index) => (
                              <li key={index} style={{ 
                                padding: '0.5rem',
                                background: 'white',
                                borderRadius: '4px',
                                border: '1px solid #e9ecef'
                              }}>
                                {playerName}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    )
                  })
                }).flat()}
                {Array.from(selectedTeams).every(teamCode => 
                  Array.from(selectedRoles).every(role => 
                    !playersCache[teamCode]?.[role] || playersCache[teamCode][role].length === 0
                  )
                ) && (
                  <p style={{ color: '#666' }}>沒有找到球員資料</p>
                )}
              </>
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