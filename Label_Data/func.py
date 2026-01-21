import matplotlib.pyplot as plt
import requests
import pandas as pd
import os
import numpy as np
from sqlalchemy import create_engine


#建資料表
def new_folder(reportpath='../../每週報告',folderpathlist=['ba_setting_report', 'ba_report','P-report','13宮格','進壘點','落點圖','圓餅圖',
    '統一打者報告, 統一投手報告','統一落點報告']):
    if not os.path.exists(reportpath):
        os.mkdir(reportpath)
    for file_name in folderpathlist:
        folder_path=reportpath+'/'+file_name
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        for TeamFile in ['中信兄弟','樂天桃猿','富邦悍將','味全龍','統一7-ELEVEn獅']:
            TeamFile_path=reportpath+'/'+ file_name +'/' + TeamFile
            if not os.path.exists(TeamFile_path):
                os.mkdir(TeamFile_path)

#函數
def color(df):
    colors = []
    for row in df['SLG_Loc']:
        if df.SLG_Loc.mean()+3*df.SLG_Loc.std() < row: 
            colors.append('#d82129')
        elif df.SLG_Loc.mean()+2*df.SLG_Loc.std()< row: 
            colors.append('#e2585e')
        elif df.SLG_Loc.mean()+1*df.SLG_Loc.std() < row: 
            colors.append("#ec9094")
        elif df.SLG_Loc.mean()+0*df.SLG_Loc.std() < row: 
            colors.append("#cdd8eb")
        elif 0 <= row:
            colors.append("#6889c2")
            
    return colors
def mscatter(x,y,ax=None, m=None, **kw):
    import matplotlib.markers as mmarkers
    if not ax: ax=plt.gca()
    sc = ax.scatter(x,y,**kw)
    if (m is not None) and (len(m)==len(x)):
        paths = []
        for marker in m:
            if isinstance(marker, mmarkers.MarkerStyle):
                marker_obj = marker
            else:
                marker_obj = mmarkers.MarkerStyle(marker)
            path = marker_obj.get_path().transformed(
                        marker_obj.get_transform())
            paths.append(path)
        sc.set_paths(paths)
    return sc

def colorC(df):
    colors = []
    for row in df['TaggedPitchType']:
        if "FB" in row: 
            colors.append("#FF0000")
        elif "CB" in row: 
            colors.append("#0080FF")
        elif "CH" in row: 
            colors.append("#007500")
        elif "FT" in row: 
            colors.append("#b62170")
        elif "SL" in row: 
            colors.append("#FFFF37")
        elif "SP" in row: 
            colors.append("#FF8000")
        elif "CT" in row:
            colors.append("#613030")
        elif "SFF" in row:
            colors.append("#D94600")
        elif "KN" in row:
            colors.append("#6F00D2")
        elif "SC" in row:
            colors.append("#00f2ff")
        elif "OT" in row: 
            colors.append("#FFFFFF")
        elif "UN" in row: 
            colors.append("#FFFFFF")
        elif "?" in row: 
            colors.append("#FFFFFF")
        else: 
            colors.append("#FFFFFF")

    return colors

def colorTx(x):
    if "FB" ==x: 
        return "#FF0000"
    elif "CB" ==x: 
        return "#0080FF"
    elif "CH" ==x: 
        return "#007500"
    elif "FT" ==x: 
        return "#FF95CA"
    elif "SL" ==x: 
        return "#FFFF37"
    elif "SP" ==x: 
        return "#FF8000"
    elif "CT" ==x:
        return "#613030"
    elif "SFF" ==x:
        return "#D94600"
    elif "KN" ==x:
        return "#6F00D2"
    elif "SC" ==x:
        return "#00f2ff"
    elif "OT" ==x:
        return "#ADADAD"
    elif "UN" ==x: 
        return "#272727"
    elif "?" == x: 
        return "#FFFFFF" 
    else: 
        return "#FFFFFF"


def colorT(x):
    colors = []
    if "FB" == x: 
        colors.append("#FF0000")
    elif "CB" == x: 
        colors.append("#0080FF")
    elif "CH" == x: 
        colors.append("#007500")
    elif "FT" == x: 
        colors.append("#b62170")
    elif "SL" == x: 
        colors.append("#FFFF37")
    elif "SP" == x: 
        colors.append("#FF8000")
    elif "CT" == x:
        colors.append("#613030")
    elif "SFF" == x:
        colors.append("#D94600")
    elif "KN" == x:
        colors.append("#6F00D2")
    elif "SC" == x:
        colors.append("#00f2ff")
    elif "OT" == x: 
        colors.append("#FFFFFF")
    elif "UN" == x: 
        colors.append("#FFFFFF")
    elif "?" == x: 
        colors.append("#FFFFFF")
    else: 
        colors.append("#FFFFFF")

    return colors

def colorspin(i):
    if i == "FB" : 
        colors="#FF0000"
    elif i == "CB" : 
        colors="#0080FF"
    elif i == "CH" : 
        colors="#007500"
    elif i == "FT" : 
        colors="#b62170"
    elif i == "SL" : 
        colors="#FFFF37"
    elif i == "SP" : 
        colors="#FF8000"
    elif i == "CT" :
        colors="#613030"
    elif i == "SFF" :
        colors="#D94600"
    elif i == "KN" :
        colors = "#6F00D2"
    elif i == "SC" :
        colors="#00f2ff"
    elif i == "OT" : 
        colors="#ADADAD"
    elif i == "UN" : 
        colors="#ADADAD"

    return colors


def PTran(x):
    if "CB" ==x: 
        return "曲球"
    elif "CH" ==x: 
        return "變速"
    elif "SL" ==x: 
        return "滑球"
    elif "SP" ==x: 
        return "指叉"
    elif "CT" ==x:
        return "切球"
    elif "KN" ==x:
        return "蝴蝶"
    elif "SC" ==x:
        return "慢曲"
    elif "OT" ==x:
        return "其他"
    elif "UN" ==x: 
        return "未知"
    elif "FB" ==x:
        return "直球"
    elif "FT" ==x:
        return "二縫"


def genPitchingStatDFWithID(id):
    url = f'https://statsapi.mlb.com/api/v1/people/{id}?hydrate=currentTeam,team,stats(type=[yearByYear,yearByYearAdvanced,careerRegularSeason,careerAdvanced,availableStats](team(league)),leagueListId=mlb_hist)&site=en'
    resp = requests.get(url)
    stat = resp.json()['people'][0]['stats']
    output = []
    targets = ['wins', 'losses', 'era', 'gamesPlayed', 'gamesStarted', 'completeGames', 'shutouts', 'holds', 'saves', 'saveOpportunities', 'inningsPitched', 'hits', 'runs', 'earnedRuns', 'homeRuns', 'numberOfPitches', 'hitBatsmen', 'baseOnBalls', 'intentionalWalks', 'strikeOuts', 'avg', 'whip']
    titles = ['Year', 'W', 'L', 'ERA', 'G', 'GS', 'CG', 'SHO', 'HLD', 'SV', 'SVO', 'IP', 'H', 'R', 'ER', 'HR', 'NP', 'HB', 'BB', 'IBB', 'SO', 'AVG', 'WHIP', 'GO/AO']
    print(stat)
    for s in stat:
        if (s['type']['displayName'] not in ['yearByYear', 'career']): continue # 'yearByYearAdvanced', 'careerAdvanced'
        for i in range(len(s['splits'])):
            st = s['splits'][i]['stat']
            score = []
            if s['type']['displayName'] == 'yearByYear':
                score.append(s['splits'][i]['season'])
            else:
                score.append('Career')
            score += [st[t] for t in targets]
            try:
                score.append(str(round(float(st['groundOuts']) / float(st['airOuts']), 2)))
            except:
                score.append('--/--')
            output.append(score)
            
    df = pd.DataFrame(output, columns=titles)
    return df



def PitCP(i):
    colorsm=['black','#ec9094','#FF0000']
    if i =='-':
        return colorsm[0]
    elif float(i) >60:
        return colorsm[2]
    elif float(i) >40:
        return colorsm[1]
    else:
        return colorsm[0]

def PitC(i):
    colorsm=['#ffffff','#ffe9e5','#ffa291','#ff7b63','#ff2600']
    if i =='--':
        return colorsm[0]
    elif float(i) >12:
        return colorsm[4]
    elif float(i) >9:
        return colorsm[3]
    elif float(i) >6:
        return colorsm[2]
    elif float(i) >3:
        return colorsm[1]
    elif float(i) >=0:
        return colorsm[0]

def PitCOut(i):
    colorsm=['#ffffff','#ffe9e5','#ffa291','#ff7b63','#ff2600']
    if i =='--':
        return colorsm[0]
    elif float(i) >20:
        return colorsm[4]
    elif float(i) >16:
        return colorsm[3]
    elif float(i) >12:
        return colorsm[2]
    elif float(i) >8:
        return colorsm[1]
    elif float(i) >4:
        return colorsm[0]
    elif float(i) >=0:
        return colorsm[0]

def SwingC(i):
    colorsm=['#ffffff','#0433ff','#4d6eff','#99acff','#e5eaff','#ffe9e5','#ffa291','#ff7b63','#ff2600']
    if i =='--':
        return colorsm[0]
    elif float(i) >=90:
        return colorsm[8]
    elif float(i) >80:
        return colorsm[7]
    elif float(i) >70:
        return colorsm[6]
    elif float(i) >60:
        return colorsm[5]
    elif float(i) >50:
        return colorsm[0]
    elif float(i) >40:
        return colorsm[0]
    elif float(i) >30:
        return colorsm[4]
    elif float(i) >20:
        return colorsm[3]
    elif float(i) >10:
        return colorsm[2]
    elif float(i) >=0:
        return colorsm[1]



#打者打擊率13宮格，打擊率&顏色
def HitC(i):
    colorsm=['#ffffff','#0433ff','#4d6eff','#99acff','#e5eaff', '#ffe9e5','#ffa291','#ff7b63','#ff2600']
    if i =='--':
        return colorsm[0]
    elif float(i) >0.330:
        return colorsm[8]
    elif float(i) >0.315:
        return colorsm[7]
    elif float(i) >0.300:
        return colorsm[6]
    elif float(i) >0.285:
        return colorsm[5]
    elif float(i) >0.270:
        return colorsm[0]
    elif float(i) >0.255:
        return colorsm[0]
    elif float(i) >0.240:
        return colorsm[0]
    elif float(i) >0.225:
        return colorsm[4]
    elif float(i) >0.210:
        return colorsm[3]
    elif float(i) >0.195:
        return colorsm[2]
    elif float(i) >=0:
        return colorsm[1]

def HitCSLG(i):
    colorsm=['#6889c2','#9bb0d6','#cdd8eb','#ffffff','#f5c8ca','#ec9094','#e2585e','#d82129']
    if i =='--':
        return colorsm[0]
    elif float(i) >0.59:
        return colorsm[7]
    elif float(i) >0.52:
        return colorsm[6]
    elif float(i) >0.45:
        return colorsm[5]
    elif float(i) >0.38:
        return colorsm[4]
    elif float(i) >0.31:
        return colorsm[3]
    elif float(i) >0.24:
        return colorsm[2]
    elif float(i) >0.17:
        return colorsm[1]
    elif float(i) >0:
        return colorsm[0]

def PiW(i):
    if i =='--':
        return 'black'
    elif float(i) >9:
        return '#ffffff'
    else :
        return 'black'
        
def PiOW(i):
    if i =='--':
        return 'black'
    elif float(i) >16:
        return '#ffffff'
    else :
        return 'black'


def BaW(i):
    if i =='--':
        return 'black'
    elif float(i) >0.315:
        return '#ffffff'
    elif float(i) <0.210:
        return '#ffffff'
    else :
        return 'black'

def SwingW(i):
    if i =='--':
        return 'black'
    elif float(i) >=80:
        return '#ffffff'
    elif float(i) <=20:
        return '#ffffff'
    else :
        return 'black'

def BaSLGW(i):
    if i =='--':
        return 'black'
    elif float(i) >0.52:
        return '#ffffff'
    elif float(i) <0.240:
        return '#ffffff'
    else :
        return 'black'
    
def PTran(x):
    if "CB" ==x: 
        return "曲球"
    elif "CH" ==x: 
        return "變速"
    elif "SL" ==x: 
        return "滑球"
    elif "SP" ==x: 
        return "指叉"
    elif "CT" ==x:
        return "切球"
    elif "KN" ==x:
        return "蝴蝶"
    elif "SC" ==x:
        return "慢曲"
    elif "OT" ==x:
        return "其他"
    elif "UN" ==x: 
        return "未知"
    elif "FB" ==x:
        return "直球"
    elif "FT" ==x:
        return "二縫"
    elif "SFF" ==x:
        return ""
def get_data_stock_P12():
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    cnx = engine.connect()
    #抓資料庫
    stock = pd.read_sql(f"SELECT * FROM `bb_BallsStat_MiLB` WHERE PitchCode IN ('PPO','CS-PP','CS-PA','PB-PA','SB-PA','Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi','Strk-PN','Ball-PN')   ORDER BY _id", con=cnx)
    stock = stock.where(pd.notnull(stock), np.nan)
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=stock.APP_VeloRel.replace('null','')
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':'',
             '0': '',
             'BB': ''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','OBD','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        try : 
            stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
            stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        except :
            pass
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    stock.HTMark = stock.HTMark.replace(np.nan, '')
    return stock
def get_data_stock_NPB():
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    # cnx = engine.connect()
    #抓資料庫
    with engine.connect() as con:
        stock = pd.read_sql(f"SELECT * FROM `bb_BallsStat_NPB` WHERE PitchCode IN ('PPO','CS-PP','CS-PA','PB-PA','SB-PA','Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi','Strk-PN','Ball-PN') AND Year IN (2024)  ORDER BY _id", con)
    stock = stock.where(pd.notnull(stock), np.nan)
    stock.HTMark = stock.HTMark.replace(np.nan, '')
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=stock.APP_VeloRel.replace('null','')
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':'',
             '0': '',
             'BB': ''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','OBD','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        try : 
            stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
            stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        except :
            pass
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    return stock

def get_data_stock_2025(extend_conditions: str):
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    # cnx = engine.connect()
    #抓資料庫
    with engine.connect() as con:
        stock = pd.read_sql(f"SELECT * FROM `bb_BallsStat_CPBL` WHERE PitchCode IN ('PPO','CS-PP','CS-PA','PB-PA','SB-PA','Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi','Strk-PN','Ball-PN') AND YEAR(Date) IN (2025) {extend_conditions} ORDER BY plate_id,sequence", con)
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=stock.APP_VeloRel.replace('null','')
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','OBD','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
        stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    return stock

def get_data_stock_2024(extend_conditions: str):
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    # cnx = engine.connect()
    #抓資料庫
    with engine.connect() as con:
        stock = pd.read_sql(f"SELECT * FROM `bb_BallsStat_CPBL` WHERE PitchCode IN ('PPO','CS-PP','CS-PA','PB-PA','SB-PA','Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi','Strk-PN','Ball-PN') AND YEAR(Date) IN (2024) {extend_conditions} ORDER BY plate_id,sequence", con)
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=stock.APP_VeloRel.replace('null','')
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','OBD','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
        stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    return stock

def get_data_stock_2023(extend_conditions: str):
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    # cnx = engine.connect()
    #抓資料庫
    with engine.connect() as con:
        stock = pd.read_sql(f"SELECT * FROM `bb_BallsStat_CPBL` WHERE PitchCode IN ('Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi') AND YEAR(Date) IN (2023) {extend_conditions} ORDER BY plate_id,sequence", con)
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
        stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    return stock

def get_data_stock_2022(extend_conditions: str):
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    # cnx = engine.connect()
    #抓資料庫
    with engine.connect() as con:
        stock = pd.read_sql(f"SELECT * FROM `bb_BallsStat_CPBL` WHERE PitchCode IN ('ER','Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi') AND YEAR(Date) IN (2022) {extend_conditions} ORDER BY plate_id,sequence", con)
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
        stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    return stock

def get_data_stock_highschool(extend_conditions: str):
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    # cnx = engine.connect()
    #抓資料庫
    with engine.connect() as con:
        stock = pd.read_sql(f"SELECT * FROM `vw_bb_BallsStat_HighSchool_Big3` WHERE PitchCode IN ('Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi') {extend_conditions} ORDER BY plate_id,sequence", con)
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
        stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    return stock

def get_data_stock_highschool_old(extend_conditions: str):
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    # cnx = engine.connect()
    #抓資料庫
    with engine.connect() as con:
        stock = pd.read_sql(f"SELECT * FROM `vw_bb_BallsStat_HighSchool_Big3_Backup` WHERE PitchCode IN ('Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi') {extend_conditions} ORDER BY plate_id,sequence", con)
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
        stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    return stock

def get_data_stock_Flexibility(extend_conditions: str) :
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    # cnx = engine.connect()
    #抓資料庫
    with engine.connect() as con:
        stock = pd.read_sql(f"SELECT * FROM `vw_bb_BallsStat_Flexibility` WHERE PitchCode IN ('Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi') AND YEAR(Date) IN (2024) {extend_conditions} ORDER BY plate_id,sequence", con)
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
        stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    return stock

def get_data_stock_AsiaChamp(extend_conditions: str) :
    engine =create_engine("mysql+pymysql://lshyu0520:O1ueufpkd5ivf@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
    cnx = engine.connect()
    #抓資料庫
    stock = pd.read_sql(f"SELECT * FROM `vw_bb_BallsStat_AsiaChamp` WHERE PitchCode IN ('Strk-C','Strk-S','Ball','Foul','In-Play','Inplay','IBB','Ball-B-I','Ball-Ill-Pi') AND YEAR(Date) IN (2023) {extend_conditions} ORDER BY plate_id,sequence", con=cnx)
    stock.APP_KZoneY=stock.APP_KZoneY.replace('null',-100)
    stock.APP_KZoneZ=stock.APP_KZoneZ.replace('null',-100)
    stock.APP_KZoneY=pd.to_numeric(stock.APP_KZoneY)
    stock.APP_KZoneZ=pd.to_numeric(stock.APP_KZoneZ)
    try:
        stock.ExitVelo=stock.ExitVelo.replace('null',-100)
        stock.ExitAngle=stock.ExitAngle.replace('null',-100)
        stock.ExitDistance=stock.ExitDistance.replace('null',-100)
    except:
        stock.ExitVelo=stock.ExitVelo.fillna(-100)
        stock.ExitAngle=stock.ExitAngle.fillna(-100)
        stock.ExitDistance=stock.ExitDistance.fillna(-100)
    stock.ExitVelo=pd.to_numeric(stock.ExitVelo)
    stock.ExitAngle=pd.to_numeric(stock.ExitAngle)
    stock.ExitDistance=pd.to_numeric(stock.ExitDistance)
    stock.LocX=pd.to_numeric(stock.LocX)
    stock.LocY=pd.to_numeric(stock.LocY)
    stock.Theta=pd.to_numeric(stock.Theta)
    stock.PT=pd.to_numeric(stock.PT)
    stock.OZone=pd.to_numeric(stock.OZone)
    stock.Strikes=pd.to_numeric(stock.Strikes)
    stock.Balls=pd.to_numeric(stock.Balls)
    stock.DirectionDeg=pd.to_numeric(stock.DirectionDeg)
    stock.APP_VeloRel=pd.to_numeric(stock.APP_VeloRel)
    HTMARK= {'':'',
            np.nan:'',
            'GROUND':'o',
            'FLYB':'^',
            'LINE': 's',
            'POPB':'^'}
    HTColor= {'':'',
            np.nan:'',
            'HARD':'#FF0000',
            'MED':'#FF3333',
            'SOFT': '#FF6666'}
    PRColor={'':''}
    Hlist=['1B','2B','3B','HR','IHR']
    Outlist=['E-DP','GT','IF','G-','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
    for i in Hlist:
        PRColor[i]='r'
    for i in Outlist:
        PRColor[i]='grey'

    for i in range(len(stock)):
        stock.loc[i,'HTMark']=HTMARK[stock.loc[i,'HitType']]
        stock.loc[i,'HTColor']=HTColor[stock.loc[i,'HardnessTag']]
        if stock.loc[i,'PitchCode']=='In-Play':
            stock.loc[i,'PRColor']=PRColor[stock.loc[i,'PA_Result']]
    return stock
