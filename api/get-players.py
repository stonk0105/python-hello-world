from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.parse
import pymysql

# 國家代碼到中文名稱的映射表
COUNTRY_CODE_TO_NAME = {
    # Pool A
    'CA CAN': '加拿大',
    'CO COL': '哥倫比亞',
    'CU CUB': '古巴',
    'PA PAN': '巴拿馬',
    'PR PUR': '波多黎各',
    # Pool B
    'GB GBR': '英國',
    'IT ITA': '義大利',
    'MX MEX': '墨西哥',
    'US USA': '美國',
    'BR BRA': '巴西',
    # Pool C
    'AU AUS': '澳洲',
    'CZ CZE': '捷克',
    'JP JPN': '日本',
    'KR KOR': '韓國',
    # Pool D
    'DO DOM': '多明尼加',
    'IL ISR': '以色列',
    'NL NLD': '荷蘭',
    'NI NIC': '尼加拉瓜',
    'VE VEN': '委內瑞拉'
}

# 資料庫連接配置
DB_CONFIG = {
    'host': 'database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com',
    'port': 38064,
    'user': 'cloudeep',
    'password': 'iEEsgOxVpU4RIGMo',
    'database': 'test_ERP_Modules',
    'charset': 'utf8mb4'
}

def get_team_chinese_name(team_code):
    """將球隊代碼轉換為中文國家名稱"""
    return COUNTRY_CODE_TO_NAME.get(team_code, team_code)

def get_players_from_db(team_code, role):
    """從資料庫查詢球員列表"""
    # 將球隊代碼轉換為中文國家名稱
    country_name = get_team_chinese_name(team_code)
    
    # 根據角色決定資料表名稱
    # role: 'pitcher' 或 'batter' (前端傳遞) 或 'hitter' (參考邏輯)
    if role in ['pitcher', 'p']:
        table_name = 'Stonk_pitcher'
    elif role in ['batter', 'b', 'hitter', 'h']:
        table_name = 'Stonk_batter'
    else:
        raise ValueError(f"Invalid role: {role}")
    
    # 連接資料庫
    connection = pymysql.connect(**DB_CONFIG)
    
    try:
        with connection.cursor() as cursor:
            # 使用參數化查詢，只查詢球員名稱
            query = f"SELECT DISTINCT `球員` FROM `{table_name}` WHERE `國家` = %s ORDER BY `球員`"
            cursor.execute(query, (country_name,))
            rows = cursor.fetchall()
            
            # 提取球員名稱列表
            players = [row[0] for row in rows if row[0]]  # 過濾掉 None 值
            
            return players
    finally:
        connection.close()

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # 解析查詢參數
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            # 獲取參數
            team = query_params.get('team', [])
            if isinstance(team, list) and len(team) > 0:
                team_code = team[0]
            else:
                team_code = team if isinstance(team, str) else ''
            
            role = query_params.get('role', ['pitcher'])[0]  # 預設為投手
            
            if not team_code:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': '請提供球隊代碼'
                }, ensure_ascii=False).encode('utf-8'))
                return
            
            # 從資料庫查詢球員列表
            players = get_players_from_db(team_code, role)
            
            # 返回結果
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'team': team_code,
                'role': role,
                'players': players,
                'count': len(players)
            }, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            import traceback
            self.send_response(500)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_info = {
                'error': str(e),
                'type': type(e).__name__,
                'traceback': traceback.format_exc().splitlines()[-10:],  # 返回最後10行
                'debug': {
                    'team': team_code if 'team_code' in locals() else 'unknown',
                    'role': role if 'role' in locals() else 'unknown'
                }
            }
            self.wfile.write(json.dumps(error_info, ensure_ascii=False).encode('utf-8'))
