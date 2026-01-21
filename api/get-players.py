from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.parse
from sqlalchemy import create_engine, text

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
            countries = [c.strip() for c in countries_str.split(',') if c.strip()] if countries_str else []
            
            role = query_params.get('role', ['pitcher'])[0]  # 預設為投手
            
            if not countries:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': '請至少選擇一個國家'
                }, ensure_ascii=False).encode('utf-8'))
                return
            
            # 連接資料庫
            engine = create_engine(
                "mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules"
            )
            
            # 根據角色選擇資料表
            table_name = 'Stonk_pitcher' if role == 'pitcher' else 'Stonk_batter'
            
            # 構建 SQL 查詢
            # 將國家列表轉換為 SQL IN 語句
            countries_str = ','.join([f"'{c}'" for c in countries])
            query = f"SELECT * FROM {table_name} WHERE 國家 IN ({countries_str})"
            
            # 執行查詢
            with engine.connect() as conn:
                result = conn.execute(text(query))
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
