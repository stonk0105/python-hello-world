from http.server import BaseHTTPRequestHandler
import os
import tempfile
import shutil

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        temp_file = None
        try:
            # 1. 生成圖片（這裡先從現有文件讀取，未來可以動態生成）
            # 例如：使用 PIL 或其他庫生成圖片
            source_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Label_Data', 'pitcher1.jpg')
            
            if not os.path.exists(source_image_path):
                self.send_response(404)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write('Source image not found'.encode('utf-8'))
                return
            
            # 2. 創建臨時文件（暫存）
            # 使用 tempfile 創建臨時文件，下載後會自動刪除
            temp_dir = tempfile.gettempdir()
            temp_filename = f'report_{os.getpid()}_{os.urandom(4).hex()}.jpg'
            temp_file = os.path.join(temp_dir, temp_filename)
            
            # 3. 複製圖片到臨時文件（未來這裡可以改為生成圖片）
            # 例如：
            # from PIL import Image
            # img = Image.new('RGB', (800, 600), color='white')
            # img.save(temp_file)
            shutil.copy2(source_image_path, temp_file)
            
            # 讀取臨時文件
            with open(temp_file, 'rb') as f:
                image_data = f.read()
            
            # 4. 設置響應頭，指定為圖片下載
            self.send_response(200)
            self.send_header('Content-type','image/jpeg')
            self.send_header('Content-Disposition', 'attachment; filename="情蒐報告.jpg"')
            self.send_header('Content-Length', str(len(image_data)))
            self.end_headers()
            
            # 5. 發送圖片數據
            self.wfile.write(image_data)
            self.wfile.flush()
            
            # 6. 發送完成後，刪除臨時文件
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass  # 如果刪除失敗，系統會在稍後清理
            
        except Exception as e:
            # 確保清理臨時文件
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
            
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))
