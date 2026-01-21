from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # 讀取圖片文件
            # 使用與 api/index.py 相同的路徑策略
            project_root = os.path.dirname(os.path.dirname(__file__))
            
            # 優先使用 Pitcher2.png
            image_path = os.path.join(project_root, 'Label_Data', 'Batter1.png')
            
            # 如果 Pitcher2.png 不存在，返回錯誤（不要自動降級到其他圖片）
            if not os.path.exists(image_path):
                self.send_response(404)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                error_msg = f'Pitcher2.png not found at: {image_path}'
                self.wfile.write(error_msg.encode('utf-8'))
                return
            
            # 讀取圖片二進制內容
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 設置響應頭，顯示圖片（不設置下載）
            # 使用 no-cache 確保每次都是最新圖片，避免瀏覽器快取舊版本
            self.send_response(200)
            self.send_header('Content-type','image/png')
            self.send_header('Content-Length', str(len(image_data)))
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            
            # 發送圖片數據
            self.wfile.write(image_data)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))
