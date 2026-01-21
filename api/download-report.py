from http.server import BaseHTTPRequestHandler
import os
import io
import zipfile
import tempfile
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')  # 使用非交互式後端
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
import pymysql

# 添加項目根目錄到路徑，以便導入 p12_func 和 func
project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 導入 p12_func 和 func 模組
try:
    from p12_func import p12_func
    from func import mscatter, colorC, HitC
except ImportError as e:
    print(f"Warning: Could not import p12_func or func: {e}")
    p12_func = None

def generate_batter_page1(batter_name='小園海斗', country='日本'):
    """生成打者報告第一頁"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # 讀取底圖
    base_image_path = os.path.join(project_root, 'Label_Data', 'Batter1.png')
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f'Batter1.png not found at: {base_image_path}')
    
    im = Image.open(base_image_path)
    I1 = ImageDraw.Draw(im)
    
    # 載入字體
    font_path = os.path.join(project_root, 'Label_Data', 'msjhbd.ttc')
    statistic_font_path = os.path.join(project_root, 'Label_Data', 'msjh.ttc')
    
    try:
        font = ImageFont.truetype(font_path, 35)
        statistic_font = ImageFont.truetype(statistic_font_path, 13)
    except:
        # 如果字體載入失敗，使用默認字體
        font = ImageFont.load_default()
        statistic_font = ImageFont.load_default()
    
    # 從資料庫獲取球員資料
    engine = create_engine(
        "mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules"
    )
    
    # 查詢球員資料（使用參數化查詢）
    with engine.connect() as conn:
        from sqlalchemy import text
        query = text("SELECT * FROM Stonk_batter WHERE 球員 = :player_name LIMIT 1")
        df_player_stat = pd.read_sql(query, conn, params={'player_name': batter_name})
    
    if len(df_player_stat) == 0:
        raise ValueError(f'找不到球員: {batter_name}')
    
    # 球員名稱
    player_name_chinese = batter_name
    player_name_eng = ''  # 可以從資料庫或其他來源獲取
    
    I1.text((30, 50), player_name_chinese, fill=(0, 0, 0), font=font)
    if player_name_eng:
        I1.text((30, 90), player_name_eng, fill=(0, 0, 0), font=font)
    
    # 基本資料
    if not pd.isna(df_player_stat.at[0, '年紀']):
        age = f"{int(df_player_stat.at[0, '年紀'])}歲"
        I1.text((235, 160), age, fill=(255, 255, 255), font=ImageFont.truetype(font_path, 14) if os.path.exists(font_path) else font)
    
    if not pd.isna(df_player_stat.at[0, '身高']) and not pd.isna(df_player_stat.at[0, '體重']):
        height_weight = f"{int(df_player_stat.at[0, '身高'])}cm {int(df_player_stat.at[0, '體重'])}kg"
        I1.text((235, 180), height_weight, fill=(255, 255, 255), font=ImageFont.truetype(font_path, 14) if os.path.exists(font_path) else font)
    
    # 打擊率區塊
    AVG_list = ['AVG', 'AVG_RHP', 'AVG_LHP', 'OPS', 'OBP', 'SLG', 'K百分比', 'BB百分比']
    for i in range(len(AVG_list)):
        column = AVG_list[i]
        if column not in df_player_stat.columns:
            continue
        statistic_value = df_player_stat.at[0, column]
        if pd.isna(statistic_value):
            continue
        
        if column == 'OBP':
            display_value = f"{float(statistic_value):.3f}"
        else:
            display_value = str(statistic_value)
        
        if i < 4:
            I1.text((145 + 45 * i, 245), display_value, fill=(0, 0, 0), font=statistic_font)
        else:
            if i >= 6:
                I1.text((143 + 45 * (i - 4), 290), display_value, fill=(0, 0, 0), font=ImageFont.truetype(statistic_font_path, 11.5) if os.path.exists(statistic_font_path) else statistic_font)
            else:
                I1.text((143 + 45 * (i - 4), 290), display_value, fill=(0, 0, 0), font=statistic_font)
    
    # PA區塊
    PA_list = ['PA', 'H', 'RBI', 'BB', 'SO', 'HR', 'SB']
    for i in range(len(PA_list)):
        column = PA_list[i]
        if column not in df_player_stat.columns:
            continue
        statistic_value = df_player_stat.at[0, column]
        if pd.isna(statistic_value):
            continue
        
        if i < 5:
            I1.text((328 + 37 * i, 249), f"{int(statistic_value)}", fill=(0, 0, 0), font=statistic_font)
        else:
            I1.text((330 + 37 * (i - 5), 292), f"{int(statistic_value)}", fill=(0, 0, 0), font=statistic_font)
    
    # 秒數區塊
    if '跑一壘' in df_player_stat.columns and not pd.isna(df_player_stat.at[0, '跑一壘']):
        I1.text((405, 292), str(df_player_stat.at[0, '跑一壘']), fill=(0, 0, 0), font=statistic_font)
    
    if 'pop time' in df_player_stat.columns and not pd.isna(df_player_stat.at[0, 'pop time']):
        I1.text((460, 292), str(df_player_stat.at[0, 'pop time']), fill=(0, 0, 0), font=statistic_font)
    
    # 保存到內存
    img_buffer = io.BytesIO()
    im.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer.getvalue()

def generate_batter_page2(batter_name='小園海斗', country='日本'):
    """生成打者報告第二頁"""
    if p12_func is None:
        raise ImportError("p12_func module is not available")
    
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # 連接資料庫
    engine = create_engine(
        "mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules"
    )
    
    # 從資料庫讀取比賽數據
    with engine.connect() as conn:
        query = text("""
            SELECT _id, Date, Pitcher, Pitcherid, PT, Batter, Batterid, BatS, BS, PitchCode, `On-Base`, PA_Result, HitType, HardnessTag, TaggedPitchType, APP_KZoneY, APP_KZoneZ, APP_VeloRel, Zone, OZone, LocX, LocY, League
            FROM cache_balls_stat
            WHERE PitchCode IN ('Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi','Strk-PN','Ball-PN')
            AND Batter = :batter_name
        """)
        bb_BallsStat_Bungee = pd.read_sql(query, conn, params={'batter_name': batter_name})
    
    if len(bb_BallsStat_Bungee) == 0:
        raise ValueError(f'找不到球員 {batter_name} 的比賽數據')
    
    # 處理數據
    bb_BallsStat_Bungee['Batter'].replace('Erisbel Arruebarruena', 'Erisbel Arruebarrena', inplace=True)
    bb_BallsStat_Bungee['APP_KZoneY'] = pd.to_numeric(bb_BallsStat_Bungee['APP_KZoneY'], errors='coerce')
    bb_BallsStat_Bungee['APP_KZoneZ'] = pd.to_numeric(bb_BallsStat_Bungee['APP_KZoneZ'], errors='coerce')
    bb_BallsStat_Bungee['APP_VeloRel'] = pd.to_numeric(bb_BallsStat_Bungee['APP_VeloRel'], errors='coerce')
    bb_BallsStat_Bungee['LocX'] = pd.to_numeric(bb_BallsStat_Bungee['LocX'], errors='coerce')
    bb_BallsStat_Bungee['LocY'] = pd.to_numeric(bb_BallsStat_Bungee['LocY'], errors='coerce')
    bb_BallsStat_Bungee['OZone'] = pd.to_numeric(bb_BallsStat_Bungee['OZone'], errors='coerce')
    bb_BallsStat_Bungee = bb_BallsStat_Bungee.dropna(subset=['APP_KZoneY', 'APP_KZoneZ']).reset_index(drop=True)
    bb_BallsStat_Bungee = bb_BallsStat_Bungee[~bb_BallsStat_Bungee['TaggedPitchType'].isin(['?', '', 'OT'])].reset_index(drop=True)
    
    # 添加顏色標記
    HTMARK = {'': '', np.nan: '', 'GROUND': 'o', 'FLYB': '^', 'LINE': 's', 'POPB': '^', None: ''}
    HTColor = {'': '', np.nan: '', 'HARD': '#FF0000', 'MED': '#FF3333', 'SOFT': '#FF6666', None: ''}
    PRColor = {'': ''}
    Hlist = ['1B', '2B', '3B', 'HR', 'IHR']
    Outlist = ['E-DP', 'GT', 'IF', 'G-', 'G', 'F', 'SF', 'SH', 'E-T', 'E-C', 'E', 'E-SF', 'FOT', 'FOTE', 'E-SH', 'DP', 'TP', 'FC', 'E-SHT', 'E-SHC', 'FSH', 'INT', 'LO', 'OBC', 'UN-IO', 'OT-IP', 'DP-S', 'OT-PO']
    for i in Hlist:
        PRColor[i] = 'r'
    for i in Outlist:
        PRColor[i] = 'grey'
    
    bb_BallsStat_Bungee['HTColor'] = bb_BallsStat_Bungee['HardnessTag'].apply(
        lambda x: HTColor.get(x, 'grey') if HTColor.get(x, '') != '' else 'grey'
    )
    bb_BallsStat_Bungee['HTMark'] = bb_BallsStat_Bungee['HitType'].apply(lambda x: HTMARK.get(x, ''))
    
    def assign_prcolor(row):
        if row['PitchCode'] == 'In-Play':
            return PRColor.get(row['PA_Result'], 'grey')
        return 'grey'
    
    bb_BallsStat_Bungee['PRColor'] = bb_BallsStat_Bungee.apply(assign_prcolor, axis=1)
    
    # 創建圖表
    bgc = '#FFFFFF'
    fig = plt.figure(figsize=(11.69, 8.27), facecolor=bgc)
    axes0 = fig.add_axes([0, 0, 1, 1], facecolor=bgc)
    axes0.set_xlim(0, 11.69)
    axes0.set_ylim(0, 8.27)
    
    # 讀取底圖
    base_image_path = os.path.join(project_root, 'Label_Data', 'Batter2.png')
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f'Batter2.png not found at: {base_image_path}')
    
    im = Image.open(base_image_path)
    I1 = ImageDraw.Draw(im)
    
    # 載入字體
    font_path = os.path.join(project_root, 'Label_Data', 'msjhbd.ttc')
    
    try:
        font = ImageFont.truetype(font_path, 35)
    except:
        font = ImageFont.load_default()
    
    # 球員名稱
    player_name_chinese = batter_name
    player_name_eng = ''
    
    I1.text((90, 10), player_name_chinese, fill=(0, 0, 0), font=font)
    if player_name_eng:
        I1.text((90, 50), player_name_eng, fill=(0, 0, 0), font=font)
    
    # 將底圖添加到圖表
    newax = fig.add_axes([0, 0, 1, 1], anchor='NE', zorder=0, facecolor='#00000000')
    newax.get_xaxis().set_visible(False)
    newax.get_yaxis().set_visible(False)
    newax.spines['top'].set_visible(False)
    newax.spines['right'].set_visible(False)
    newax.spines['bottom'].set_visible(False)
    newax.spines['left'].set_visible(False)
    newax.imshow(im, extent=[0, 11.69, 0, 8.27])
    
    # 初始化 p12_func
    p12 = p12_func()
    
    # 獲取球員數據
    df_player = bb_BallsStat_Bungee[bb_BallsStat_Bungee['Batter'] == batter_name].reset_index(drop=True)
    
    if batter_name == 'マルティネス':
        batter_name = 'A.マルティネス'
    
    if len(df_player) == 0:
        print(f"找不到 {batter_name} 的數據")
    else:
        # 為左右投分別繪製圖表
        for pt in [1, 0]:  # 1=左投, 0=右投
            df_pt = df_player[df_player['PT'] == pt]
            
            if len(df_pt) == 0:
                continue
            
            # 畫落點(兩好球後)
            df_2s = df_pt[df_pt['BS'].isin(["0-2", "1-2", "2-2", "3-2"])]
            p12.diammondScenario_batter_page(0.135 + (pt - 1) * -0.5, 0.53, 0.25 * 0.77, 0.35 * 0.79, df_2s, fig, 20)
            
            # 畫落點(全部)
            p12.diammondScenario_batter_page(0.304 + (pt - 1) * -0.5, 0.53, 0.25 * 0.77, 0.35 * 0.79, df_pt, fig, 10)
            
            # 畫13宮格
            p12.zoneAVG_B(-0.01 + (pt - 1) * -0.5, 0.53, 0.25 * 0.8, 0.35 * 0.8, df_pt, fig, 'Total')
            
            # 畫進壘點 - Swing
            df_swing = df_pt[(df_pt['PitchCode'].isin(['Strk-S', 'In-Play', 'Foul'])) & (df_pt['BS'] == '0-0')]
            p12.plate_location(0.06 + (pt - 1) * -0.5, 0.33, 0.25 * 0.8, 0.35 * 0.8, df_swing, fig, 'Swing')
            
            # 畫進壘點 - O-Swing
            p12.plate_location(0.27 + (pt - 1) * -0.5, 0.33, 0.25 * 0.8, 0.35 * 0.8, df_pt, fig, 'O-Swing')
            
            # 畫進壘點 - 安打
            p12.plate_location(0.06 + (pt - 1) * -0.5, 0.1, 0.25 * 0.8, 0.35 * 0.8, df_pt, fig, '安打')
            
            # 畫進壘點 - Miss
            p12.plate_location(0.27 + (pt - 1) * -0.5, 0.1, 0.25 * 0.8, 0.35 * 0.8, df_pt, fig, 'Miss')
    
    # 保存到內存
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='PNG', dpi=100, bbox_inches='tight', facecolor=bgc)
    plt.close(fig)
    img_buffer.seek(0)
    return img_buffer.getvalue()

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            import urllib.parse
            # 解析查詢參數
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            # 檢查是否為查看模式（返回單張圖片）或下載模式（返回 ZIP）
            action = query_params.get('action', ['download'])[0]  # 'view' 或 'download'
            
            if action == 'view':
                # 查看模式：返回 Page1 圖片
                page1_data = generate_batter_page1('小園海斗', '日本')
                
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.send_header('Content-Length', str(len(page1_data)))
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.end_headers()
                self.wfile.write(page1_data)
            else:
                # 下載模式：返回 ZIP 文件
                page1_data = generate_batter_page1('小園海斗', '日本')
                page2_data = generate_batter_page2('小園海斗', '日本')
                
                # 創建 ZIP 文件
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.writestr('小園海斗_完整報告p1.png', page1_data)
                    zip_file.writestr('小園海斗_完整報告p2.png', page2_data)
                
                zip_buffer.seek(0)
                zip_data = zip_buffer.getvalue()
                
                # 設置響應頭
                self.send_response(200)
                self.send_header('Content-type', 'application/zip')
                self.send_header('Content-Disposition', 'attachment; filename="小園海斗_完整報告.zip"')
                self.send_header('Content-Length', str(len(zip_data)))
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.end_headers()
                
                # 發送 ZIP 數據
                self.wfile.write(zip_data)
            
        except Exception as e:
            import traceback
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            error_msg = f'Error: {str(e)}\n{traceback.format_exc()}'
            self.wfile.write(error_msg.encode('utf-8'))
