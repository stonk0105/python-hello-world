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

# 導入 Toolbox 模組
try:
    sys.path.insert(0, os.path.join(project_root, 'Label_Data'))
    from Toolbox import *
    # 確保 AVG 函數被導入
    from Toolbox import AVG, RISPAVG, GB_FB
except ImportError as e:
    print(f"Warning: Could not import Toolbox: {e}")
    AVG = None
    RISPAVG = None
    GB_FB = None

# 資料庫緩存（避免重複查詢）
_db_cache = {
    'Stonk_batter': None,
    'Stonk_pitcher': None,
    'cache_balls_stat': None,
    'cache_balls_stat_pa': None
}

def generate_batter_page1(batter_name='小園海斗', country='日本', df_all_players=None):
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
    
    # 從傳入的資料或資料庫獲取球員資料
    if df_all_players is not None:
        # 使用傳入的資料（已優化查詢）
        df_player_stat = df_all_players[df_all_players['球員'] == batter_name].reset_index(drop=True)
    else:
        # 如果沒有傳入資料，則從資料庫查詢（向後兼容）
        engine = create_engine(
            "mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules"
        )
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

def generate_batter_page2(batter_name='小園海斗', country='日本', df_cache_balls_stat=None):
    """生成打者報告第二頁"""
    if p12_func is None:
        raise ImportError("p12_func module is not available")
    
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # 從傳入的資料或資料庫獲取比賽數據
    if df_cache_balls_stat is not None:
        bb_BallsStat_Bungee = df_cache_balls_stat[df_cache_balls_stat['Batter'] == batter_name].reset_index(drop=True)
    else:
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
    
    # 處理數據（這些操作是冪等的，即使數據已經處理過也不會出錯）
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
    # 隱藏主圖表的座標軸
    axes0.get_xaxis().set_visible(False)
    axes0.get_yaxis().set_visible(False)
    axes0.spines['top'].set_visible(False)
    axes0.spines['right'].set_visible(False)
    axes0.spines['bottom'].set_visible(False)
    axes0.spines['left'].set_visible(False)
    
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

def generate_pitcher_page1(pitcher_name='小園海斗', country='日本', df_all_pitchers=None, df_cache_balls_stat=None, df_cache_balls_stat_pa=None):
    """生成投手報告第一頁"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # 讀取底圖
    base_image_path = os.path.join(project_root, 'Label_Data', 'Pitcher1.png')
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f'Pitcher1.png not found at: {base_image_path}')
    
    im = Image.open(base_image_path)
    I1 = ImageDraw.Draw(im)
    
    # 載入字體
    font_path = os.path.join(project_root, 'Label_Data', 'msjhbd.ttc')
    statistic_font_path = os.path.join(project_root, 'Label_Data', 'msjh.ttc')
    
    try:
        font = ImageFont.truetype(font_path, 35)
        statistic_font = ImageFont.truetype(statistic_font_path, 13)
    except:
        font = ImageFont.load_default()
        statistic_font = ImageFont.load_default()
    
    # 從傳入的資料或資料庫獲取投手資料
    if df_all_pitchers is not None:
        df_player_stat = df_all_pitchers[df_all_pitchers['球員'] == pitcher_name].reset_index(drop=True)
    else:
        engine = create_engine(
            "mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules"
        )
        with engine.connect() as conn:
            from sqlalchemy import text
            query = text("SELECT * FROM Stonk_pitcher WHERE 球員 = :player_name LIMIT 1")
            df_player_stat = pd.read_sql(query, conn, params={'player_name': pitcher_name})
    
    if df_cache_balls_stat_pa is not None:
        df_player_each_PA = df_cache_balls_stat_pa[df_cache_balls_stat_pa['Pitcher'] == pitcher_name].reset_index(drop=True)
    else:
        engine = create_engine(
            "mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules"
        )
        with engine.connect() as conn:
            from sqlalchemy import text
            query = text("""
                SELECT _id, Date, Pitcher, Pitcherid, PT, Batter, Batterid, BatS, BS, PitchCode, `On-Base`, PA_Result, HitType, HardnessTag, TaggedPitchType, APP_KZoneY, APP_KZoneZ, APP_VeloRel, Zone, OZone, LocX, LocY, League
                FROM cache_balls_stat
                WHERE PA_Result IS NOT NULL AND PA_Result != '' AND Pitcher = :pitcher_name
            """)
            df_player_each_PA = pd.read_sql(query, conn, params={'pitcher_name': pitcher_name})
    
    if len(df_player_stat) == 0:
        raise ValueError(f'找不到投手: {pitcher_name}')
    
    # 球員名稱
    player_name_chinese = pitcher_name
    player_name_eng = ''
    
    I1.text((30, 40), player_name_chinese, fill=(0, 0, 0), font=font)
    if player_name_eng:
        I1.text((30, 80), player_name_eng, fill=(0, 0, 0), font=font)
    
    # 基本資料
    if not pd.isna(df_player_stat.at[0, '年紀']):
        age = f"{int(df_player_stat.at[0, '年紀'])}歲"
        I1.text((210, 130), age, fill=(255, 255, 255), font=ImageFont.truetype(font_path, 14) if os.path.exists(font_path) else font)
    
    if not pd.isna(df_player_stat.at[0, '身高']) and not pd.isna(df_player_stat.at[0, '體重']):
        height_weight = f"{int(df_player_stat.at[0, '身高'])}cm {int(df_player_stat.at[0, '體重'])}kg"
        I1.text((210, 150), height_weight, fill=(255, 255, 255), font=ImageFont.truetype(font_path, 14) if os.path.exists(font_path) else font)
    
    # 如果 AVG 相關欄位為空，則從 cache_balls_stat 計算
    if AVG is not None and len(df_player_each_PA) > 0:
        if 'AVG' in df_player_stat.columns and pd.isna(df_player_stat.at[0, 'AVG']):
            df_player_stat.at[0, 'AVG'] = AVG(df_player_each_PA)
        if 'AVG_RHB' in df_player_stat.columns and pd.isna(df_player_stat.at[0, 'AVG_RHB']):
            df_player_RHB = df_player_each_PA[df_player_each_PA['BatS'] == 0].reset_index(drop=True)
            if len(df_player_RHB) > 0:
                df_player_stat.at[0, 'AVG_RHB'] = AVG(df_player_RHB)
        if 'AVG_LHB' in df_player_stat.columns and pd.isna(df_player_stat.at[0, 'AVG_LHB']):
            df_player_LHB = df_player_each_PA[df_player_each_PA['BatS'] == 1].reset_index(drop=True)
            if len(df_player_LHB) > 0:
                df_player_stat.at[0, 'AVG_LHB'] = AVG(df_player_LHB)
    
    # K% 區塊 - 對照資料表欄位名稱
    # 資料表欄位：K百分比, BB百分比, WHIP, AVG, AVG_RHB, AVG_LHB
    # 嘗試多種可能的欄位名稱格式
    K_P_list = [
        ("K百分比", "K%"),  # 優先使用中文欄位名
        ("BB百分比", "BB%"),
        ("WHIP", "WHIP"),
        ("AVG", "AVG"),
        ("AVG_RHB", "AVG_RHB"),
        ("AVG_LHB", "AVG_LHB")
    ]
    for i, (column_primary, column_fallback) in enumerate(K_P_list):
        # 優先使用主要欄位名，如果不存在則嘗試備用名稱
        column = column_primary if column_primary in df_player_stat.columns else column_fallback
        if column not in df_player_stat.columns:
            continue
        statistic_value = df_player_stat.at[0, column]
        if pd.isna(statistic_value):
            continue
        
        if column == "WHIP":
            display_value = f"{float(statistic_value):.2f}"
        else:
            display_value = str(statistic_value)
        
        if i < 3:
            I1.text((22 + 47 * i, 235), display_value, fill=(0, 0, 0), font=statistic_font)
        else:
            I1.text((22 + 46 * (i - 3), 280), display_value, fill=(0, 0, 0), font=statistic_font)
    
    # ERA 區塊 - 對照資料表欄位名稱
    # 資料表欄位：ERA, IP, W_L, G_SP, H, 中繼, 後援, SO, BB, K_9, BB_9
    # 嘗試多種可能的欄位名稱格式
    ERA_list = [
        ("ERA", "ERA"),
        ("IP", "IP"),
        ("W_L", "W-L"),  # 優先使用下劃線格式
        ("G_SP", "G/SP"),
        ("H", "H"),
        ("中繼", "中繼"),
        ("後援", "後援"),
        ("SO", "SO"),
        ("BB", "BB"),
        ("K_9", "K/9"),  # 優先使用下劃線格式
        ("BB_9", "BB/9")
    ]
    for i, (column_primary, column_fallback) in enumerate(ERA_list):
        # 優先使用主要欄位名，如果不存在則嘗試備用名稱
        column = column_primary if column_primary in df_player_stat.columns else column_fallback
        if column not in df_player_stat.columns:
            continue
        statistic_value = df_player_stat.at[0, column]
        if pd.isna(statistic_value):
            continue
        
        if i < 2:
            I1.text((165 + 37 * i, 195), str(statistic_value), fill=(0, 0, 0), font=statistic_font)
        elif 2 <= i < 4:
            I1.text((168 + 37 * i, 195), str(statistic_value), fill=(0, 0, 0), font=statistic_font)
        elif 4 <= i < 7:
            I1.text((288 + 40 * (i - 3), 195), str(statistic_value), fill=(0, 0, 0), font=statistic_font)
        elif 7 <= i < 9:
            I1.text((170 + 42 * (i - 7), 235), str(statistic_value), fill=(0, 0, 0), font=statistic_font)
        elif 9 <= i < 11:
            I1.text((160 + 42 * (i - 7), 235), str(statistic_value), fill=(0, 0, 0), font=statistic_font)
    
    # 滾飛比 / 得點圈
    
    if RISPAVG and GB_FB and len(df_player_each_PA) > 0:
        得點圈 = RISPAVG(df_player_each_PA)
        滾飛比 = GB_FB(df_player_each_PA)
        I1.text((328, 235), str(滾飛比), fill=(0, 0, 0), font=statistic_font)
        I1.text((380, 235), str(得點圈), fill=(0, 0, 0), font=statistic_font)
    
    # 時間區塊
    time_list = ['快投時間', '牽制一壘']
    for i in range(len(time_list)):
        column = time_list[i]
        if column not in df_player_stat.columns:
            continue
        statistic_value = df_player_stat.at[0, column]
        if pd.isna(statistic_value):
            continue
        I1.text((160 + 80 * i, 280), str(statistic_value), fill=(0, 0, 0), font=statistic_font)
    
    # 右下角球速表格
    if df_cache_balls_stat is not None:
        df_player = df_cache_balls_stat[df_cache_balls_stat['Pitcher'] == pitcher_name].reset_index(drop=True)
    else:
        engine = create_engine(
            "mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules"
        )
        with engine.connect() as conn:
            from sqlalchemy import text
            query = text("""
                SELECT _id, Date, Pitcher, Pitcherid, PT, Batter, Batterid, BatS, BS, PitchCode, `On-Base`, PA_Result, HitType, HardnessTag, TaggedPitchType, APP_KZoneY, APP_KZoneZ, APP_VeloRel, Zone, OZone, LocX, LocY, League
                FROM cache_balls_stat
                WHERE PitchCode IN ('Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi','Strk-PN','Ball-PN')
                AND Pitcher = :pitcher_name
            """)
            df_player = pd.read_sql(query, conn, params={'pitcher_name': pitcher_name})
    
    if len(df_player) > 0:
        # 處理數據類型
        df_player['APP_KZoneY'] = pd.to_numeric(df_player['APP_KZoneY'], errors='coerce')
        df_player['APP_KZoneZ'] = pd.to_numeric(df_player['APP_KZoneZ'], errors='coerce')
        df_player['APP_VeloRel'] = pd.to_numeric(df_player['APP_VeloRel'], errors='coerce')
        df_player = df_player.dropna(subset=['APP_KZoneY', 'APP_KZoneZ']).reset_index(drop=True)
        df_player = df_player[~df_player['TaggedPitchType'].isin(['?', '', 'OT'])].reset_index(drop=True)
        
        taggedpitchtype_dict = {"FB": "速球", "FT": "伸卡", "SL": "滑球", "CT": "卡特", "CB": "曲球", "CH": "變速", "SP": "指叉", "SFF": '快叉'}
        
        # 計算每個球路出現的次數
        pitchtype_counts = df_player['TaggedPitchType'].value_counts().to_dict()
        taggedpitchtype_list = sorted(pitchtype_counts, key=pitchtype_counts.get, reverse=True)
        taggedpitchtype_list = taggedpitchtype_list if len(taggedpitchtype_list) <= 5 else taggedpitchtype_list[:5]
        
        for i in range(len(taggedpitchtype_list)):
            taggedpitchtype = taggedpitchtype_list[i]
            if taggedpitchtype == "?":
                continue
            
            pitch_type = taggedpitchtype_dict.get(taggedpitchtype, taggedpitchtype)
            df_player_R = df_player[df_player['BatS'] == 0]
            df_player_L = df_player[df_player['BatS'] == 1]
            
            df_player_taggedpitchtype = df_player[df_player['TaggedPitchType'] == taggedpitchtype].reset_index(drop=True)
            df_player_taggedpitchtype_R = df_player[(df_player['TaggedPitchType'] == taggedpitchtype) & (df_player['BatS'] == 0)].reset_index(drop=True)
            df_player_taggedpitchtype_L = df_player[(df_player['TaggedPitchType'] == taggedpitchtype) & (df_player['BatS'] == 1)].reset_index(drop=True)
            
            speed = round(df_player_taggedpitchtype['APP_VeloRel'].mean(), 1) if len(df_player_taggedpitchtype) > 0 else None
            Max_speed = round(df_player_taggedpitchtype['APP_VeloRel'].max(), 1) if len(df_player_taggedpitchtype) > 0 else None
            
            try:
                total_usage = f"{round(len(df_player_taggedpitchtype_R) / len(df_player_R) * 100, 1) if len(df_player_R) > 0 else 0} / {round(len(df_player_taggedpitchtype_L) / len(df_player_L) * 100, 1) if len(df_player_L) > 0 else 0}"
            except:
                total_usage = "--- / ---"
            
            try:
                first_pitch_usage = f"{round(len(df_player_taggedpitchtype_R[df_player_taggedpitchtype_R['BS'] == '0-0']) / len(df_player_R[df_player_R['BS'] == '0-0']) * 100, 1) if len(df_player_R[df_player_R['BS'] == '0-0']) > 0 else 0} / {round(len(df_player_taggedpitchtype_L[df_player_taggedpitchtype_L['BS'] == '0-0']) / len(df_player_L[df_player_L['BS'] == '0-0']) * 100, 1) if len(df_player_L[df_player_L['BS'] == '0-0']) > 0 else 0}"
            except:
                first_pitch_usage = "--- / ---"
            
            try:
                R_2 = round(len(df_player_taggedpitchtype_R[df_player_taggedpitchtype_R['BS'] == '2-2']) / len(df_player_R[df_player_R['BS'] == '2-2']) * 100, 1) if len(df_player_R[df_player_R['BS'] == '2-2']) > 0 else 0
            except:
                R_2 = '---'
            
            try:
                L_2 = round(len(df_player_taggedpitchtype_L[df_player_taggedpitchtype_L['BS'] == '2-2']) / len(df_player_L[df_player_L['BS'] == '2-2']) * 100, 1) if len(df_player_L[df_player_L['BS'] == '2-2']) > 0 else 0
            except:
                L_2 = '---'
            
            twotwo_usage = f"{R_2} / {L_2}"
            
            batter_ahead_count = ['1-0', '2-0', '2-1', '3-0', '3-1']
            try:
                batter_ahead_usage = f"{round(len(df_player_taggedpitchtype_R[df_player_taggedpitchtype_R['BS'].isin(batter_ahead_count)]) / len(df_player_R[df_player_R['BS'].isin(batter_ahead_count)]) * 100, 1) if len(df_player_R[df_player_R['BS'].isin(batter_ahead_count)]) > 0 else 0} / {round(len(df_player_taggedpitchtype_L[df_player_taggedpitchtype_L['BS'].isin(batter_ahead_count)]) / len(df_player_L[df_player_L['BS'].isin(batter_ahead_count)]) * 100, 1) if len(df_player_L[df_player_L['BS'].isin(batter_ahead_count)]) > 0 else 0}"
            except:
                batter_ahead_usage = "--- / ---"
            
            if len(df_player_taggedpitchtype[df_player_taggedpitchtype['Zone'].isin([0])]) > 0:
                strike_chase_percentage = f"{round(len(df_player_taggedpitchtype[df_player_taggedpitchtype['PitchCode'].isin(['Strk-C', 'Strk-S', 'Foul', 'In-Play'])]) / len(df_player_taggedpitchtype) * 100, 1)} / {round(len(df_player_taggedpitchtype[(df_player_taggedpitchtype['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play'])) & (df_player_taggedpitchtype['Zone'] == 0)]) / len(df_player_taggedpitchtype[df_player_taggedpitchtype['Zone'].isin([0])]) * 100, 1)}"
            else:
                strike_chase_percentage = f"{round(len(df_player_taggedpitchtype[df_player_taggedpitchtype['PitchCode'].isin(['Strk-C', 'Strk-S', 'Foul', 'In-Play'])]) / len(df_player_taggedpitchtype) * 100, 1) if len(df_player_taggedpitchtype) > 0 else 0} / ---"
            
            I1.text((572 + 98 * i, 435), pitch_type, fill=(0, 0, 0), font=statistic_font)
            
            if not pd.isna(speed) and not pd.isna(Max_speed):
                I1.text((545 + 98 * i, 460), str(speed) + ' / ' + str(Max_speed), fill=(0, 0, 0), font=statistic_font)
            
            if 'nan' not in str(total_usage).lower():
                I1.text((552 + 98 * i, 505), total_usage, fill=(0, 0, 0), font=statistic_font)
            if 'nan' not in str(first_pitch_usage).lower():
                I1.text((552 + 98 * i, 540), first_pitch_usage, fill=(0, 0, 0), font=statistic_font)
            if 'nan' not in str(twotwo_usage).lower():
                I1.text((552 + 98 * i, 575), twotwo_usage, fill=(0, 0, 0), font=statistic_font)
            if 'nan' not in str(batter_ahead_usage).lower():
                I1.text((552 + 98 * i, 610), batter_ahead_usage, fill=(0, 0, 0), font=statistic_font)
            if 'nan' not in str(strike_chase_percentage).lower():
                I1.text((552 + 98 * i, 640), strike_chase_percentage, fill=(0, 0, 0), font=statistic_font)
    
    # 保存到內存
    img_buffer = io.BytesIO()
    im.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer.getvalue()

def generate_pitcher_page2(pitcher_name='小園海斗', country='日本', df_cache_balls_stat=None):
    """生成投手報告第二頁"""
    if p12_func is None:
        raise ImportError("p12_func module is not available")
    
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # 從傳入的資料或資料庫獲取比賽數據
    if df_cache_balls_stat is not None:
        df_player = df_cache_balls_stat[df_cache_balls_stat['Pitcher'] == pitcher_name].reset_index(drop=True)
    else:
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
                AND Pitcher = :pitcher_name
            """)
            df_player = pd.read_sql(query, conn, params={'pitcher_name': pitcher_name})
    
    if len(df_player) == 0:
        raise ValueError(f'找不到投手 {pitcher_name} 的比賽數據')
    
    # 處理數據
    df_player['APP_KZoneY'] = pd.to_numeric(df_player['APP_KZoneY'], errors='coerce')
    df_player['APP_KZoneZ'] = pd.to_numeric(df_player['APP_KZoneZ'], errors='coerce')
    df_player['APP_VeloRel'] = pd.to_numeric(df_player['APP_VeloRel'], errors='coerce')
    df_player = df_player.dropna(subset=['APP_KZoneY', 'APP_KZoneZ']).reset_index(drop=True)
    df_player = df_player[~df_player['TaggedPitchType'].isin(['?', '', 'OT'])].reset_index(drop=True)
    
    # 特殊處理：米奇白
    if pitcher_name == '米奇白':
        pitcher_name = 'Mitch White'
    
    # 創建圖表
    bgc = '#FFFFFF'
    fig = plt.figure(figsize=(11.69, 8.27), facecolor=bgc)
    axes0 = fig.add_axes([0, 0, 1, 1], facecolor=bgc)
    axes0.set_xlim(0, 11.69)
    axes0.set_ylim(0, 8.27)
    # 隱藏主圖表的座標軸
    axes0.get_xaxis().set_visible(False)
    axes0.get_yaxis().set_visible(False)
    axes0.spines['top'].set_visible(False)
    axes0.spines['right'].set_visible(False)
    axes0.spines['bottom'].set_visible(False)
    axes0.spines['left'].set_visible(False)
    
    # 讀取底圖
    base_image_path = os.path.join(project_root, 'Label_Data', 'Pitcher2.png')
    if not os.path.exists(base_image_path):
        raise FileNotFoundError(f'Pitcher2.png not found at: {base_image_path}')
    
    im = Image.open(base_image_path)
    I1 = ImageDraw.Draw(im)
    
    # 載入字體
    font_path = os.path.join(project_root, 'Label_Data', 'msjhbd.ttc')
    
    try:
        font = ImageFont.truetype(font_path, 35)
    except:
        font = ImageFont.load_default()
    
    # 球員名稱
    player_name_chinese = pitcher_name
    player_name_eng = ''
    
    I1.text((90, 10), player_name_chinese, fill=(0, 0, 0), font=font)
    if player_name_eng:
        I1.text((90, 50), player_name_eng, fill=(0, 0, 0), font=font)
    
    # 投球手型態（PT: 0=右投, 1=左投）
    pt_dict = {0: '右投', 1: '左投'}
    if len(df_player) > 0 and 'PT' in df_player.columns:
        pt_value = df_player.at[0, 'PT'] if not pd.isna(df_player.at[0, 'PT']) else 0
        pt_text = pt_dict.get(int(pt_value), '右投')
        I1.text((480, 50), pt_text, fill=(0, 0, 0), font=font)
    
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
    
    # 場景列表
    scenario_list = [['0-0'], ['0-1'], ['1-0'], ['0-2', '1-2', '2-2', '3-2'], ['1B', '2B', '3B', 'HR', 'IHR'], ['Strk-S']]
    
    # 為左右打者分別繪製圖表
    for bats in [0, 1]:  # 0=右打, 1=左打
        df_bats = df_player[df_player['BatS'] == bats].reset_index(drop=True)
        
        if len(df_bats) == 0:
            continue
        
        # 為每個場景繪製進壘點
        for scenario in range(len(scenario_list)):
            if scenario <= 3:
                # 場景 0-3: 根據 BS (球數) 篩選
                df_scenario = df_bats[df_bats['BS'].isin(scenario_list[scenario])].reset_index(drop=True)
            elif scenario == 4:
                # 場景 4: 根據 PA_Result (打擊結果) 篩選
                df_scenario = df_bats[df_bats['PA_Result'].isin(scenario_list[scenario])].reset_index(drop=True)
            else:
                # 場景 5: 根據 PitchCode 篩選
                df_scenario = df_bats[df_bats['PitchCode'].isin(scenario_list[scenario])].reset_index(drop=True)
            
            # 繪製進壘點
            # 位置計算：0.06 + scenario * 0.15, 0.52 - bats * 0.405
            p12.plate_location(
                0.06 + scenario * 0.15, 
                0.52 - bats * 0.405, 
                0.25 * 0.8, 
                0.35 * 0.8, 
                df_scenario, 
                fig, 
                'Total'
            )
    
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
            import json
            # 解析查詢參數
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            # 檢查是否為查看模式（返回單張圖片）或下載模式（返回 ZIP）
            action = query_params.get('action', ['download'])[0]  # 'view' 或 'download'
            page = query_params.get('page', ['1'])[0]  # '1' 或 '2'
            
            # 獲取球員列表和角色（如果有的話）
            players_param = query_params.get('players', [])
            role_param = query_params.get('role', ['batter'])[0]  # 'pitcher' 或 'batter'
            
            if players_param:
                # 解析 JSON 格式的球員列表
                try:
                    players_list = json.loads(players_param[0]) if isinstance(players_param[0], str) else players_param
                except:
                    players_list = players_param if isinstance(players_param, list) else [players_param[0]] if players_param else []
            else:
                players_list = ['小園海斗']  # 默認球員
            
            # 資料庫緩存：一次查詢所有需要的資料
            engine = create_engine(
                "mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules"
            )
            
            # 根據角色選擇資料表
            if role_param == 'pitcher':
                table_name = 'Stonk_pitcher'
                # 查詢投手基本資料
                with engine.connect() as conn:
                    from sqlalchemy import text
                    placeholders = ','.join([f':player_{i}' for i in range(len(players_list))])
                    query = text(f"SELECT * FROM {table_name} WHERE 球員 IN ({placeholders})")
                    params = {f'player_{i}': player for i, player in enumerate(players_list)}
                    df_all_players = pd.read_sql(query, conn, params=params)
                
                # 查詢 cache_balls_stat（所有投手共用）
                with engine.connect() as conn:
                    from sqlalchemy import text
                    placeholders = ','.join([f':player_{i}' for i in range(len(players_list))])
                    query = text(f"""
                        SELECT _id, Date, Pitcher, Pitcherid, PT, Batter, Batterid, BatS, BS, PitchCode, `On-Base`, PA_Result, HitType, HardnessTag, TaggedPitchType, APP_KZoneY, APP_KZoneZ, APP_VeloRel, Zone, OZone, LocX, LocY, League
                        FROM cache_balls_stat
                        WHERE PitchCode IN ('Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi','Strk-PN','Ball-PN')
                        AND Pitcher IN ({placeholders})
                    """)
                    params = {f'player_{i}': player for i, player in enumerate(players_list)}
                    df_cache_balls_stat = pd.read_sql(query, conn, params=params)
                    df_cache_balls_stat['APP_KZoneY'] = pd.to_numeric(df_cache_balls_stat['APP_KZoneY'], errors='coerce')
                    df_cache_balls_stat['APP_KZoneZ'] = pd.to_numeric(df_cache_balls_stat['APP_KZoneZ'], errors='coerce')
                    df_cache_balls_stat['APP_VeloRel'] = pd.to_numeric(df_cache_balls_stat['APP_VeloRel'], errors='coerce')
                    df_cache_balls_stat = df_cache_balls_stat.dropna(subset=['APP_KZoneY', 'APP_KZoneZ']).reset_index(drop=True)
                    df_cache_balls_stat = df_cache_balls_stat[~df_cache_balls_stat['TaggedPitchType'].isin(['?', '', 'OT'])].reset_index(drop=True)
                
                # 查詢 cache_balls_stat_pa（所有投手共用）
                with engine.connect() as conn:
                    from sqlalchemy import text
                    placeholders = ','.join([f':player_{i}' for i in range(len(players_list))])
                    query = text(f"""
                        SELECT _id, Date, Pitcher, Pitcherid, PT, Batter, Batterid, BatS, BS, PitchCode, `On-Base`, PA_Result, HitType, HardnessTag, TaggedPitchType, APP_KZoneY, APP_KZoneZ, APP_VeloRel, Zone, OZone, LocX, LocY, League
                        FROM cache_balls_stat
                        WHERE PA_Result IS NOT NULL AND PA_Result != ''
                        AND Pitcher IN ({placeholders})
                    """)
                    params = {f'player_{i}': player for i, player in enumerate(players_list)}
                    df_cache_balls_stat_pa = pd.read_sql(query, conn, params=params)
            else:
                # 打者
                table_name = 'Stonk_batter'
                with engine.connect() as conn:
                    from sqlalchemy import text
                    placeholders = ','.join([f':player_{i}' for i in range(len(players_list))])
                    query = text(f"SELECT * FROM {table_name} WHERE 球員 IN ({placeholders})")
                    params = {f'player_{i}': player for i, player in enumerate(players_list)}
                    df_all_players = pd.read_sql(query, conn, params=params)
                
                # 查詢 cache_balls_stat（打者 Page 2 需要）
                with engine.connect() as conn:
                    from sqlalchemy import text
                    placeholders = ','.join([f':player_{i}' for i in range(len(players_list))])
                    query = text(f"""
                        SELECT _id, Date, Pitcher, Pitcherid, PT, Batter, Batterid, BatS, BS, PitchCode, `On-Base`, PA_Result, HitType, HardnessTag, TaggedPitchType, APP_KZoneY, APP_KZoneZ, APP_VeloRel, Zone, OZone, LocX, LocY, League
                        FROM cache_balls_stat
                        WHERE PitchCode IN ('Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi','Strk-PN','Ball-PN')
                        AND Batter IN ({placeholders})
                    """)
                    params = {f'player_{i}': player for i, player in enumerate(players_list)}
                    df_cache_balls_stat = pd.read_sql(query, conn, params=params)
                    
                    # 檢查是否查詢到數據
                    if len(df_cache_balls_stat) == 0:
                        print(f'警告: 找不到打者 {players_list} 的 cache_balls_stat 數據')
                    else:
                        print(f'查詢到 {len(df_cache_balls_stat)} 筆 cache_balls_stat 數據')
                    
                    df_cache_balls_stat['APP_KZoneY'] = pd.to_numeric(df_cache_balls_stat['APP_KZoneY'], errors='coerce')
                    df_cache_balls_stat['APP_KZoneZ'] = pd.to_numeric(df_cache_balls_stat['APP_KZoneZ'], errors='coerce')
                    df_cache_balls_stat['APP_VeloRel'] = pd.to_numeric(df_cache_balls_stat['APP_VeloRel'], errors='coerce')
                    df_cache_balls_stat['LocX'] = pd.to_numeric(df_cache_balls_stat['LocX'], errors='coerce')
                    df_cache_balls_stat['LocY'] = pd.to_numeric(df_cache_balls_stat['LocY'], errors='coerce')
                    df_cache_balls_stat['OZone'] = pd.to_numeric(df_cache_balls_stat['OZone'], errors='coerce')
                    df_cache_balls_stat = df_cache_balls_stat.dropna(subset=['APP_KZoneY', 'APP_KZoneZ']).reset_index(drop=True)
                    df_cache_balls_stat = df_cache_balls_stat[~df_cache_balls_stat['TaggedPitchType'].isin(['?', '', 'OT'])].reset_index(drop=True)
                    
                    # 檢查處理後的數據
                    if len(df_cache_balls_stat) == 0:
                        print(f'警告: 處理後找不到有效的 cache_balls_stat 數據')
                    else:
                        print(f'處理後剩餘 {len(df_cache_balls_stat)} 筆有效數據')
                df_cache_balls_stat_pa = None
            
            # 如果有多個球員，生成 ZIP 文件
            if len(players_list) >= 1:
                # 生成所有球員的圖片並打包成 ZIP
                zip_buffer = io.BytesIO()
                warnings = []  # 收集警告信息
                errors = []   # 收集錯誤信息
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for player_name in players_list:
                        try:
                            # 根據角色生成不同的報告
                            if role_param == 'pitcher':
                                # 投手：生成 Page 1 和 Page 2
                                image_data_p1 = generate_pitcher_page1(player_name, '日本', df_all_players, df_cache_balls_stat, df_cache_balls_stat_pa)
                                filename_p1 = f'{player_name}_完整報告p1.png'
                                zip_file.writestr(filename_p1, image_data_p1)
                                
                                # 生成 Page 2，如果失敗則記錄詳細錯誤
                                try:
                                    if df_cache_balls_stat is None or len(df_cache_balls_stat) == 0:
                                        raise ValueError(f'找不到 {player_name} 的 cache_balls_stat 數據')
                                    
                                    # 檢查該球員是否有數據
                                    player_data = df_cache_balls_stat[df_cache_balls_stat['Pitcher'] == player_name]
                                    if len(player_data) == 0:
                                        raise ValueError(f'找不到 {player_name} 在 cache_balls_stat 中的數據')
                                    
                                    image_data_p2 = generate_pitcher_page2(player_name, '日本', df_cache_balls_stat)
                                    filename_p2 = f'{player_name}_完整報告p2.png'
                                    zip_file.writestr(filename_p2, image_data_p2)
                                except Exception as e2:
                                    # Page 2 生成失敗，記錄錯誤但繼續（Page 1 已經寫入）
                                    import traceback
                                    error_msg = f'{player_name} 的 Page 2 生成失敗: {str(e2)}'
                                    warnings.append(error_msg)
                                    print(error_msg)
                                    print(traceback.format_exc())
                                    # 不 raise，讓 Page 1 保留在 ZIP 中
                            else:
                                # 打者：生成 Page 1 和 Page 2
                                image_data_p1 = generate_batter_page1(player_name, '日本', df_all_players)
                                filename_p1 = f'{player_name}_完整報告p1.png'
                                zip_file.writestr(filename_p1, image_data_p1)
                                
                                # 生成 Page 2，如果失敗則記錄詳細錯誤
                                try:
                                    if df_cache_balls_stat is None or len(df_cache_balls_stat) == 0:
                                        raise ValueError(f'找不到 {player_name} 的 cache_balls_stat 數據')
                                    
                                    # 檢查該球員是否有數據
                                    player_data = df_cache_balls_stat[df_cache_balls_stat['Batter'] == player_name]
                                    if len(player_data) == 0:
                                        raise ValueError(f'找不到 {player_name} 在 cache_balls_stat 中的數據')
                                    
                                    image_data_p2 = generate_batter_page2(player_name, '日本', df_cache_balls_stat)
                                    filename_p2 = f'{player_name}_完整報告p2.png'
                                    zip_file.writestr(filename_p2, image_data_p2)
                                except Exception as e2:
                                    # Page 2 生成失敗，記錄錯誤但繼續（Page 1 已經寫入）
                                    import traceback
                                    error_msg = f'{player_name} 的 Page 2 生成失敗: {str(e2)}'
                                    warnings.append(error_msg)
                                    print(error_msg)
                                    print(traceback.format_exc())
                                    # 不 raise，讓 Page 1 保留在 ZIP 中
                        except Exception as e:
                            # 如果某個球員的 Page 1 生成失敗，記錄錯誤但繼續處理其他球員
                            import traceback
                            error_msg = f'{player_name} 的報告生成失敗: {str(e)}'
                            errors.append(error_msg)
                            print(error_msg)
                            print(traceback.format_exc())
                            continue
                    
                    # 如果有警告或錯誤，添加到 ZIP 中
                    if warnings or errors:
                        error_log = []
                        if errors:
                            error_log.append("=== 錯誤 ===")
                            error_log.extend(errors)
                        if warnings:
                            error_log.append("\n=== 警告 ===")
                            error_log.extend(warnings)
                        error_log_text = "\n".join(error_log)
                        zip_file.writestr('錯誤日誌.txt', error_log_text.encode('utf-8'))
                
                zip_buffer.seek(0)
                zip_data = zip_buffer.getvalue()
                
                # 設置響應頭（view 模式不帶下載頭，讓前端處理下載）
                self.send_response(200)
                self.send_header('Content-type', 'application/zip')
                # 只有在 download 模式才添加下載頭
                if action == 'download':
                    role_name = '投手' if role_param == 'pitcher' else '打者'
                    self.send_header('Content-Disposition', f'attachment; filename="{role_name}報告.zip"')
                
                # 如果有警告或錯誤，通過響應頭傳遞給前端
                if warnings:
                    import json
                    warnings_json = json.dumps(warnings, ensure_ascii=False)
                    self.send_header('X-Report-Warnings', warnings_json)
                if errors:
                    import json
                    errors_json = json.dumps(errors, ensure_ascii=False)
                    self.send_header('X-Report-Errors', errors_json)
                
                self.send_header('Content-Length', str(len(zip_data)))
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.end_headers()
                self.wfile.write(zip_data)
            else:
                # 單個球員
                if action == 'download':
                    # 下載模式：生成 ZIP 文件（打者包含 Page 1 和 Page 2）
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        player_name = players_list[0]
                        try:
                            if role_param == 'pitcher':
                                # 投手：生成 Page 1 和 Page 2
                                image_data_p1 = generate_pitcher_page1(player_name, '日本', df_all_players, df_cache_balls_stat, df_cache_balls_stat_pa)
                                filename_p1 = f'{player_name}_完整報告p1.png'
                                zip_file.writestr(filename_p1, image_data_p1)
                                
                                image_data_p2 = generate_pitcher_page2(player_name, '日本', df_cache_balls_stat)
                                filename_p2 = f'{player_name}_完整報告p2.png'
                                zip_file.writestr(filename_p2, image_data_p2)
                            else:
                                # 打者：生成 Page 1 和 Page 2
                                image_data_p1 = generate_batter_page1(player_name, '日本', df_all_players)
                                filename_p1 = f'{player_name}_完整報告p1.png'
                                zip_file.writestr(filename_p1, image_data_p1)
                                
                                image_data_p2 = generate_batter_page2(player_name, '日本', df_cache_balls_stat)
                                filename_p2 = f'{player_name}_完整報告p2.png'
                                zip_file.writestr(filename_p2, image_data_p2)
                        except Exception as e:
                            print(f'生成 {player_name} 的報告失敗: {str(e)}')
                            raise
                    
                    zip_buffer.seek(0)
                    zip_data = zip_buffer.getvalue()
                    
                    # 設置響應頭
                    self.send_response(200)
                    self.send_header('Content-type', 'application/zip')
                    role_name = '投手' if role_param == 'pitcher' else '打者'
                    self.send_header('Content-Disposition', f'attachment; filename="{role_name}報告_1人.zip"')
                    self.send_header('Content-Length', str(len(zip_data)))
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.end_headers()
                    self.wfile.write(zip_data)
                else:
                    # 預覽模式：返回單張圖片（用於查看）
                    if role_param == 'pitcher':
                        # 投手：支持 Page 1 和 Page 2
                        if page == '2':
                            image_data = generate_pitcher_page2(players_list[0], '日本', df_cache_balls_stat)
                        else:
                            # 默認返回 Page 1
                            image_data = generate_pitcher_page1(players_list[0], '日本', df_all_players, df_cache_balls_stat, df_cache_balls_stat_pa)
                    else:
                        # 打者
                        if page == '2':
                            image_data = generate_batter_page2(players_list[0], '日本', df_cache_balls_stat)
                        else:
                            # 默認返回 Page1
                            image_data = generate_batter_page1(players_list[0], '日本', df_all_players)
                    
                    # 設置響應頭
                    self.send_response(200)
                    self.send_header('Content-type', 'image/png')
                    self.send_header('Content-Length', str(len(image_data)))
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.end_headers()
                    self.wfile.write(image_data)
            
        except Exception as e:
            import traceback
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            error_msg = f'Error: {str(e)}\n{traceback.format_exc()}'
            self.wfile.write(error_msg.encode('utf-8'))
