from http.server import BaseHTTPRequestHandler
import os
import tempfile

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        temp_file_path = None
        try:
            # 1. 讀取源圖片文件
            # 從當前文件（api/download-report.py）找到專案根目錄，然後進入 Label_Data
            # __file__ 是 api/download-report.py
            # os.path.dirname(__file__) 是 api/
            # os.path.dirname(os.path.dirname(__file__)) 是專案根目錄
            # 然後加上 Label_Data/pitcher1.jpg
            project_root = os.path.dirname(os.path.dirname(__file__))
            source_image_path = os.path.join(project_root, 'Label_Data', 'pitcher1.jpg')
            
            # 或者直接寫成（推薦，更簡潔）：
            # source_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Label_Data', 'pitcher1.jpg')
            
            if not os.path.exists(source_image_path):
                self.send_response(404)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write('Image not found'.encode('utf-8'))
                return
            
            # 2. 創建臨時文件（暫存，供下載使用）
            # 使用 tempfile 創建臨時文件，下載後會自動刪除
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file_path = temp_file.name
            temp_file.close()
            
            # 3. 複製圖片到臨時文件（未來這裡可以改為動態生成圖片）
            # 例如：使用 PIL 生成圖片
            # from PIL import Image
            # img = Image.new('RGB', (800, 600), color='white')
            # img.save(temp_file_path, 'JPEG')
            
            # 目前先複製現有圖片
            with open(source_image_path, 'rb') as src:
                with open(temp_file_path, 'wb') as dst:
                    dst.write(src.read())
            
            # 讀取臨時文件數據
            with open(temp_file_path, 'rb') as f:
                image_data = f.read()
            
            # 4. 設置響應頭，指定為圖片下載
            self.send_response(200)
            self.send_header('Content-type','image/jpeg')
            self.send_header('Content-Disposition', 'attachment; filename="情蒐報告.jpg"')
            self.send_header('Content-Length', str(len(image_data)))
            self.end_headers()
            
            # 5. 發送圖片數據
            self.wfile.write(image_data)
            
            # 6. 發送完成後，刪除臨時文件
            try:
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            except:
                pass  # 如果刪除失敗，系統會在稍後清理
            
        except Exception as e:
            # 確保清理臨時文件
            try:
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            except:
                pass
            
            # 返回詳細錯誤訊息
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            error_msg = f'Error: {str(e)}'
            self.wfile.write(error_msg.encode('utf-8'))
