from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # 讀取圖片文件
            # 使用與 api/index.py 相同的路徑策略
            project_root = os.path.dirname(os.path.dirname(__file__))
            image_path = os.path.join(project_root, 'Label_Data', 'Pitcher2.png')
            
            if not os.path.exists(image_path):
                self.send_response(404)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write('Image not found'.encode('utf-8'))
                return
            
            # 讀取圖片二進制內容
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 設置響應頭，顯示圖片（不設置下載）
            self.send_response(200)
            self.send_header('Content-type','image/png')
            self.send_header('Content-Length', str(len(image_data)))
            self.send_header('Cache-Control', 'public, max-age=3600')
            self.end_headers()
            
            # 發送圖片數據
            self.wfile.write(image_data)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))
