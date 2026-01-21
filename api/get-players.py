from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.parse
from sqlalchemy import create_engine, text

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

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # 解析查詢參數
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            # 獲取參數
            countries_param = query_params.get('countries', [])
            # 處理參數：可能是列表或字符串（用逗號分隔）
            if isinstance(countries_param, list) and len(countries_param) > 0:
                countries_str = countries_param[0]
            else:
                countries_str = countries_param if isinstance(countries_param, str) else ''
            
            # 將逗號分隔的字符串轉換為列表
            country_codes = [c.strip() for c in countries_str.split(',') if c.strip()] if countries_str else []
            
            role = query_params.get('role', ['pitcher'])[0]  # 預設為投手
            
            if not country_codes:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': '請至少選擇一個國家'
                }, ensure_ascii=False).encode('utf-8'))
                return
            
            # 將國家代碼轉換為中文名稱
            country_names = []
            for code in country_codes:
                chinese_name = COUNTRY_CODE_TO_NAME.get(code, code)  # 如果找不到映射，使用原值
                country_names.append(chinese_name)
            
            # 連接資料庫
            engine = create_engine(
                "mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules"
            )
            
            # 根據角色選擇資料表
            table_name = 'Stonk_pitcher' if role == 'pitcher' else 'Stonk_batter'
            
            # 構建 SQL 查詢
            # 將國家名稱列表轉換為 SQL IN 語句（使用參數化查詢避免 SQL 注入）
            placeholders = ', '.join([f':country{i}' for i in range(len(country_names))])
            query = text(f"SELECT * FROM {table_name} WHERE 國家 IN ({placeholders})")
            params = {f'country{i}': name for i, name in enumerate(country_names)}
            
            # 執行查詢
            with engine.connect() as conn:
                result = conn.execute(query, params)
                rows = result.fetchall()
                
                # 轉換為字典列表
                players = []
                for row in rows:
                    player_dict = {}
                    for key, value in row._mapping.items():
                        # 處理日期等特殊類型
                        if hasattr(value, 'isoformat'):
                            player_dict[key] = value.isoformat()
                        else:
                            player_dict[key] = value
                    players.append(player_dict)
            
            # 返回結果
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'players': players,
                'count': len(players)
            }, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type','application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_info = {
                'error': str(e),
                'type': type(e).__name__
            }
            self.wfile.write(json.dumps(error_info, ensure_ascii=False).encode('utf-8'))
