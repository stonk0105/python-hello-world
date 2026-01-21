from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # 處理圖片下載請求
        if self.path == '/api/download-report' or self.path.endswith('/download-report'):
            self.send_image()
        else:
            # 原有的 Hello, world! 端點
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write('Hello, world!'.encode('utf-8'))
        return

    def send_image(self):
        try:
            # 讀取圖片文件
            image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Label_Data', 'pitcher1.jpg')
            
            if not os.path.exists(image_path):
                self.send_response(404)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write('Image not found'.encode('utf-8'))
                return
            
            # 讀取圖片二進制內容
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 設置響應頭，指定為圖片下載
            self.send_response(200)
            self.send_header('Content-type','image/jpeg')
            self.send_header('Content-Disposition', 'attachment; filename="情蒐報告.jpg"')
            self.send_header('Content-Length', str(len(image_data)))
            self.end_headers()
            
            # 發送圖片數據
            self.wfile.write(image_data)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))
