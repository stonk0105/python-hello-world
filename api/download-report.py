from http.server import BaseHTTPRequestHandler
import os
import sys
import traceback

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # 在 Vercel 中，工作目錄通常是 /var/task
            # 嘗試多種路徑策略
            
            # 策略1: 相對於當前文件
            current_file = __file__
            base_dir1 = os.path.dirname(os.path.dirname(current_file))
            image_path1 = os.path.join(base_dir1, 'Label_Data', 'pitcher1.jpg')
            
            # 策略2: 相對於工作目錄
            cwd = os.getcwd()
            image_path2 = os.path.join(cwd, 'Label_Data', 'pitcher1.jpg')
            
            # 策略3: 絕對路徑（Vercel 標準）
            image_path3 = os.path.join('/var/task', 'Label_Data', 'pitcher1.jpg')
            
            # 策略4: 相對於 api 目錄
            api_dir = os.path.dirname(current_file)
            image_path4 = os.path.join(api_dir, '..', 'Label_Data', 'pitcher1.jpg')
            image_path4 = os.path.normpath(image_path4)
            
            # 嘗試所有路徑
            image_path = None
            for path in [image_path1, image_path2, image_path3, image_path4]:
                if os.path.exists(path):
                    image_path = path
                    break
            
            if not image_path:
                # 返回詳細的調試信息
                debug_info = {
                    'current_file': current_file,
                    'cwd': cwd,
                    'tried_paths': [image_path1, image_path2, image_path3, image_path4],
                    'all_paths_exist': [os.path.exists(p) for p in [image_path1, image_path2, image_path3, image_path4]],
                    'parent_dir_contents': os.listdir(os.path.dirname(os.path.dirname(current_file))) if os.path.exists(os.path.dirname(os.path.dirname(current_file))) else 'N/A'
                }
                
                self.send_response(404)
                self.send_header('Content-type','application/json')
                self.end_headers()
                import json
                self.wfile.write(json.dumps({
                    'error': 'Image not found',
                    'debug': debug_info
                }, indent=2).encode('utf-8'))
                return
            
            # 讀取圖片二進制內容
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 設置響應頭，指定為圖片下載
            self.send_response(200)
            self.send_header('Content-type','image/jpeg')
            self.send_header('Content-Disposition', 'attachment; filename="情蒐報告.jpg"')
            self.send_header('Content-Length', str(len(image_data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # 發送圖片數據
            self.wfile.write(image_data)
            
        except Exception as e:
            # 返回詳細錯誤信息
            error_trace = traceback.format_exc()
            self.send_response(500)
            self.send_header('Content-type','application/json')
            self.end_headers()
            import json
            error_info = {
                'error': str(e),
                'type': type(e).__name__,
                'traceback': error_trace,
                'current_file': __file__ if '__file__' in globals() else 'N/A',
                'cwd': os.getcwd()
            }
            self.wfile.write(json.dumps(error_info, indent=2).encode('utf-8'))
