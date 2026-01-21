from func import *
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from PIL import Image
from sqlalchemy import create_engine
from matplotlib.font_manager import FontProperties
import pandas as pd
import seaborn as sns
import os
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



class p12_func:
    def __init__(self):
        pass
#進壘點(x座標, y座標, 寬, 高, 資料表, 底圖, 篩選條件)
    def plate_location(self, left, bottom, width, height, dft, fig, scenario):


        if scenario == '安打':
            dft=dft[dft['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR'])]
        if scenario == 'Strike':
            dft = dft[dft['PitchCode'].isin(['Strk-C', 'Strk-S', 'Foul', 'In-Play'])]

        if scenario == '直球安打':
            dft=dft[(dft['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR']))&(dft['TaggedPitchType'].isin(['FT','FB']))]

        if scenario == '變化球安打':
            dft=dft[dft['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR'])&(~(dft['TaggedPitchType'].isin(['FT','FB'])))]

        elif scenario == 'GB+POP':
            dft=dft[dft['HitType'].isin(['GROUND', 'POPB'])]

        elif scenario == 'GB':
            dft=dft[dft['HitType'].isin(['GROUND'])]

        elif scenario == 'POP':
            dft=dft[dft['HitType'].isin(['POPB'])]

        elif scenario == 'FLY':
            dft=dft[dft['HitType'].isin(['FLYB'])]

        elif scenario == 'Call':
            dft=dft[dft['PitchCode'].isin(['Strk-C'])]

        elif scenario == 'Miss':
            dft=dft[dft['PitchCode'].isin(['Strk-S'])]

        elif scenario == 'In-Play':
            dft=dft[dft['PitchCode'].isin(['In-Play'])]

        elif scenario == "首球出棒":
            dft=dft[(dft['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play'])) & (dft['BS'].isin(['0-0']))] 

        elif scenario == '三振':
            dft = dft[dft['PA_Result'].isin(['K', 'Ks', 'K-DO', 'K-BS', 'K-BF', 'K-DS','K-SF'])]

        elif scenario == 'Swing':
            dft = dft[dft['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play'])]

        elif scenario == 'Foul':
            dft = dft[dft['PitchCode'].isin(['Foul'])]

        elif scenario == 'Hard':
            dft = dft[dft['HardnessTag'] == 'HARD']

        elif scenario == 'O-Swing':
            dft = dft[(dft['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play']))& (dft['Zone'] == 0)]
  
        elif scenario == 'Total':
            dft = dft[~(dft['TaggedPitchType'].isnull())]

        elif scenario == '出局':
            dft=dft[dft['PA_Result'].isin(['DP','F','FC','FOT','G','G-','GT','IF','E-C','E-T','K', 'Ks', 'K-DO', 'K-BS', 'K-BF', 'K-DS','K-SF'])]
       
        ax_ins = fig.add_axes([left, bottom, width, height])
        ax_ins.set_facecolor('none')
        ax_ins.set_xlim(-26, 26)
        ax_ins.set_ylim(9, 60)

        line1 = [(-10,-5),(10,-5)]
        line2 = [(-10,-3),(-10,-5)]
        line3 = [(10,-3),(10,-5)]
        line4 = [(-10,-3),(0,0)]
        line5 = [(10,-3),(0,0)]
        line6 = [(-10,18),(-10,42)]
        line7 = [(10,18),(10,42)]
        line8 = [(-10,18),(10,18)]
        line9 = [(-10,42),(10,42)]

        (line1_xs, line1_ys) = zip(*line1)
        (line2_xs, line2_ys) = zip(*line2)
        (line3_xs, line3_ys) = zip(*line3)
        (line4_xs, line4_ys) = zip(*line4)
        (line5_xs, line5_ys) = zip(*line5)
        (line6_xs, line6_ys) = zip(*line6)
        (line7_xs, line7_ys) = zip(*line7)
        (line8_xs, line8_ys) = zip(*line8)
        (line9_xs, line9_ys) = zip(*line9)
        
        x1=dft['APP_KZoneY']
        # y1=dft['APP_KZoneZ']+(35*(dft['APP_KZoneZ']-42)/42)
        y1=dft['APP_KZoneZ']
        ax_ins.add_line(Line2D(line6_xs, line6_ys, linewidth=1, color='red',zorder=190))
        ax_ins.add_line(Line2D(line7_xs, line7_ys, linewidth=1, color='red',zorder=190))
        ax_ins.add_line(Line2D(line8_xs, line8_ys, linewidth=1, color='red',zorder=190))
        ax_ins.add_line(Line2D(line9_xs, line9_ys, linewidth=1, color='red',zorder=190))
        ax_ins.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=190))
        ax_ins.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=190))
        ax_ins.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=190))
        ax_ins.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=190))
        ax_ins.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=190))
        # ax_ins.scatter(x1,y1,c=colorC(dft),s=7*7,edgecolors='none', alpha = 1)
        ax_ins.scatter(x1,y1,c=colorC(dft),s=7*7,edgecolors='black', alpha = 1, linewidths = 0.2)

        ax_ins.set_xlim(-33,33)
        ax_ins.set_ylim(-6,66)
        ax_ins.axis('off')
        return ax_ins
#十三宮格_打擊率(x座標, y座標, 寬, 高, 資料表, 底圖)
    def zoneAVG_B(self, left, bottom, width, height, dft, fig):


        ax_ins = fig.add_axes([left, bottom, width, height],facecolor="#FFFFFF",zorder=20)
        line1 = [(-10,-5),(10,-5)]
        line2 = [(-10,-3),(-10,-5)]
        line3 = [(10,-3),(10,-5)]
        line4 = [(-10,-3),(0,0)]
        line5 = [(10,-3),(0,0)]
        line6 = [(-10,18),(-10,42)]
        line7 = [(10,18),(10,42)]
        line8 = [(-10,18),(10,18)]
        line9 = [(-10,42),(10,42)]

        (line1_xs, line1_ys) = zip(*line1)
        (line2_xs, line2_ys) = zip(*line2)
        (line3_xs, line3_ys) = zip(*line3)
        (line4_xs, line4_ys) = zip(*line4)
        (line5_xs, line5_ys) = zip(*line5)
        (line6_xs, line6_ys) = zip(*line6)
        (line7_xs, line7_ys) = zip(*line7)
        (line8_xs, line8_ys) = zip(*line8)
        (line9_xs, line9_ys) = zip(*line9)

        PA = dft[dft['PA_Result'].isin([ 'G', '3B', 'K', 'FC', 'K-DO', 'LO', 'K-SF', 'K-DS', 'FOT', 'E-SHC', '1B', 'IF', '2B', 'G-', 'INT', 'HR', 'K-BS', 'E-C', 'GT', 'IHR', 'K-BF', 'Ks', 'DP','E-T', 'F'])]
        hit = dft[dft['PA_Result'].isin(['3B', '2B', 'HR', '1B', 'IHR'])] 

        try:
            Z1p='%.3f'%(len(hit[hit['OZone']==1]) / len(PA[PA['OZone'] == 1]))
        except:
            Z1p='--'
        try:
            Z2p='%.3f'%(len(hit[hit['OZone']==2]) / len(PA[PA['OZone'] == 2]))
        except:
            Z2p='--'
        try:
            Z3p='%.3f'%(len(hit[hit['OZone']==3]) / len(PA[PA['OZone'] == 3]))
        except:
            Z3p='--'
        try:
            Z4p='%.3f'%(len(hit[hit['OZone']==4]) / len(PA[PA['OZone'] == 4]))
        except:
            Z4p='--'
        try:
            Z5p='%.3f'%(len(hit[hit['OZone']==5]) / len(PA[PA['OZone'] == 5]))
        except:
            Z5p='--'
        try:
            Z6p='%.3f'%(len(hit[hit['OZone']==6]) / len(PA[PA['OZone'] == 6]))
        except:
            Z6p='--'
        try:
            Z7p='%.3f'%(len(hit[hit['OZone']==7]) / len(PA[PA['OZone'] == 7]))
        except:
            Z7p='--'
        try:
            Z8p='%.3f'%(len(hit[hit['OZone']==8]) / len(PA[PA['OZone'] == 8]))
        except:
            Z8p='--'
        try:
            Z9p='%.3f'%(len(hit[hit['OZone']==9]) / len(PA[PA['OZone'] == 9]))
        except:
            Z9p='--'
        try:
            Z11p='%.3f'%(len(hit[hit['OZone']==11]) / len(PA[PA['OZone'] == 11]))
        except:
            Z11p='--'
        try:
            Z12p='%.3f'%(len(hit[hit['OZone']==12]) / len(PA[PA['OZone'] == 12]))
        except:
            Z12p='--'
        try:
            Z13p='%.3f'%(len(hit[hit['OZone']==13]) / len(PA[PA['OZone'] == 13]))
        except:
            Z13p='--'
        try:
            Z14p='%.3f'%(len(hit[hit['OZone']==14]) / len(PA[PA['OZone'] == 14]))
        except:
            Z14p='--'
        c1=HitC((Z1p))
        c2=HitC((Z2p))
        c3=HitC((Z3p))
        c4=HitC((Z4p))
        c5=HitC((Z5p))
        c6=HitC((Z6p))
        c7=HitC((Z7p))
        c8=HitC((Z8p))
        c9=HitC((Z9p))
        c11=HitC((Z11p))
        c12=HitC((Z12p))
        c13=HitC((Z13p))
        c14=HitC((Z14p))
        Count_hit=[]
        for i in range(1,14):
            if i<10:
                Count_hit.append(len(hit[hit['OZone']==i]))
            if i>=10:
                Count_hit.append(len(hit[hit['OZone']==(i+1)]))
        Count_PA=[]
        for i in range(1,14):
            if i<10:
                Count_PA.append(len(PA[PA['OZone']==i]))
            if i>=10:
                Count_PA.append(len(PA[PA['OZone']==(i+1)]))
        # print(len(Count))
        font={
            'weight':'black',
            'size':20 * 0.4,
        }
        font_low={
            'weight':'black',
            'size':15 * 0.4,
        }

        ax_ins.add_patch(
            patches.Rectangle(
                (-15, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c1,
                fill=True,
                zorder=90
            ) )
        ax_ins.text(-10, 43, str(Z1p), fontdict=font,ha='center', zorder=100)
        ax_ins.text(-10,39,"("+str(Count_hit[0]) + "/" + str(Count_PA[0])+")",fontdict=font_low,ha='center',zorder=100)
        ax_ins.add_patch(
            patches.Rectangle(
                (-5, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c2,
                fill=True,
                zorder=90
            ) )
        ax_ins.text(0,43,str(Z2p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(0,39,"("+str(Count_hit[1]) + "/" + str(Count_PA[1])+")",fontdict=font_low,ha='center',zorder=100)

        ax_ins.add_patch(
            patches.Rectangle(
                (5, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c3,
                fill=True,
                zorder=90
            ) )
        ax_ins.text(10,43,str(Z3p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(10,39,"("+str(Count_hit[2]) + "/" + str(Count_PA[2])+")",fontdict=font_low,ha='center',zorder=100)
        
        ax_ins.add_patch(
            patches.Rectangle(
                (-15, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c4,
                fill=True,
                zorder=90
            ) )
        ax_ins.text(-10,31,str(Z4p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(-10,27,"("+str(Count_hit[3]) + "/" + str(Count_PA[3])+")",fontdict=font_low,ha='center',zorder=100)
        ax_ins.add_patch(
            patches.Rectangle(
                (-5, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c5,
                fill=True,
                zorder=90
            ) )
        ax_ins.text(0,31,str(Z5p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(0,27,"("+str(Count_hit[4]) + "/" + str(Count_PA[4])+")",fontdict=font_low,ha='center',zorder=100)
        ax_ins.add_patch(
            patches.Rectangle(
                (5, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c6,
                fill=True,
                zorder=90
            ) )
        ax_ins.text(10,31,str(Z6p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(10,27,"("+str(Count_hit[5]) + "/" + str(Count_PA[5])+")",fontdict=font_low,ha='center',zorder=100)
        ax_ins.add_patch(
            patches.Rectangle(
                (-15, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c7,
                fill=True,
                zorder=90
            ) )
        ax_ins.text(-10,19,str(Z7p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(-10,15,"("+str(Count_hit[6]) + "/" + str(Count_PA[6])+")",fontdict=font_low,ha='center',zorder=100)
        ax_ins.add_patch(
            patches.Rectangle(
                (-5, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c8,
                fill=True,
                zorder=90
            ) )
        ax_ins.text(0,19,str(Z8p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(0,15,"("+str(Count_hit[7]) + "/" + str(Count_PA[7])+")",fontdict=font_low,ha='center',zorder=100)
        ax_ins.add_patch(
            patches.Rectangle(
                (5, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c9,
                fill=True,
                zorder=90
            ) )
        ax_ins.text(10,19,str(Z9p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(10,15,"("+str(Count_hit[8]) + "/" + str(Count_PA[8])+")",fontdict=font_low,ha='center',zorder=100)
        ax_ins.add_patch(
            patches.Rectangle(
                (0, 30),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c11,
                fill=True
            ) )
        ax_ins.text(-15,50,str(Z11p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(-9,50,"("+str(Count_hit[9]) + "/" + str(Count_PA[9])+")",fontdict=font_low,zorder=100)
        ax_ins.add_patch(
            patches.Rectangle(
                (0, 6),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c13,
                fill=True
            ) )
        ax_ins.text(-15,8,str(Z13p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(-9,8,"("+str(Count_hit[11]) + "/" + str(Count_PA[11])+")",fontdict=font_low,zorder=100)
        ax_ins.add_patch(
            patches.Rectangle(
                (0, 30),
                20,
                24,
                edgecolor = 'black',
                facecolor = c12,
                fill=True
            ) )
        ax_ins.text(5,50,str(Z12p),fontdict=font,ha='center',zorder=100)
        ax_ins.text(11,50,"("+str(Count_hit[10]) + "/" + str(Count_PA[10])+")",fontdict=font_low,zorder=100)

        ax_ins.add_patch(
            patches.Rectangle(
                (0, 6),
                20,
                24,
                edgecolor = 'black',
                facecolor = c14,
                fill=True
            ) )
        ax_ins.text(5,8,str(Z14p),fontdict=font, ha='center', zorder=100)
        ax_ins.text(11,8,"("+str(Count_hit[12]) + "/" + str(Count_PA[12])+")",fontdict=font_low,zorder=100)
        


        ax_ins.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        ax_ins.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        ax_ins.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        ax_ins.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        ax_ins.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        ax_ins.set_xlim(-33,33)
        ax_ins.set_ylim(-6,66)
        ax_ins.axis('off')
        return ax_ins
#落點圖(x座標, y座標, 寬, 高, 資料表, 底圖, 圖層順序)
    def diammondScenario_batter_page(self, left, bottom, width, height, dft, fig, order):       

        dfFar = dft[(dft['HitType'] == "GROUND")].reset_index(drop = True)
        bgc='#FFFFFF'
        axes1 = fig.add_axes([left, bottom, width, height],facecolor=bgc,zorder = order) 
        ax=axes1
        current_directory = os.path.dirname(__file__)
        image_path = os.path.join(current_directory, 'Label_Data', '落點底圖線圖-01.png')
        Pic = np.array(Image.open(image_path))
        image = ax.imshow(Pic, cmap=plt.cm.gray, extent=[-400, 400, -100, 500],alpha=1, zorder =  order) 

        scLoc = mscatter(dft['LocX'] , dft['LocY'],c=list(dft['PRColor']),s=(3)**2, m=list(dft['HTMark']), ax=ax,alpha=1,picker=True,edgecolors='black',linewidth=0.3)

        #滾地球標線
        for disP in range(len(dfFar)):
            line3 = [(dfFar.LocX[disP],dfFar.LocY[disP]),(0,0)]
            (line3_xs, line3_ys) = zip(*line3)
            ax.add_line(Line2D(line3_xs, line3_ys, ls='dashed',linewidth=0.5, color='#666666',zorder = order))

        ax.set_xlim(-300,300)
        ax.set_ylim(-100,500)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        return ax
#拉Bungeeee資料表(應該不會再用到了)
    def p12_stock(self):
        engine =create_engine("mysql+pymysql://cloudeep:iEEsgOxVpU4RIGMo@database-test.c4zrhmao4pj4.ap-northeast-1.rds.amazonaws.com:38064/test_ERP_Modules")
        cnx = engine.connect()

        query = """
                SELECT _id, Date, Pitcher, Pitcherid, PT, Batter, Batterid, BatS, Theta, BS, PitchCode, `On-Base`, PA_Result, HitType, Balls, Strikes, HardnessTag, TaggedPitchType, APP_KZoneY, APP_KZoneZ, APP_VeloRel, Zone, OZone, LocX, LocY, League
                FROM bb_BallsStat_Bungeeeee
                WHERE PitchCode IN ('In-Play', 'Ball', 'Strk-C', 'Strk-S', 'Foul')
                """
        bb_BallsStat_Bungee = pd.read_sql(query, con = cnx)
        bb_BallsStat_Bungee = bb_BallsStat_Bungee[~bb_BallsStat_Bungee['TaggedPitchType'].isin(['?', ''])].reset_index(drop = True)

        bb_BallsStat_Bungee['APP_KZoneY'] = pd.to_numeric(bb_BallsStat_Bungee['APP_KZoneY'], errors='coerce')
        bb_BallsStat_Bungee['APP_KZoneZ'] = pd.to_numeric(bb_BallsStat_Bungee['APP_KZoneZ'], errors='coerce')
        bb_BallsStat_Bungee['Theta'] = pd.to_numeric(bb_BallsStat_Bungee['Theta'], errors='coerce')
        bb_BallsStat_Bungee['APP_VeloRel'] = pd.to_numeric(bb_BallsStat_Bungee['APP_VeloRel'], errors='coerce')
        bb_BallsStat_Bungee['LocX'] = pd.to_numeric(bb_BallsStat_Bungee['LocX'], errors='coerce')
        bb_BallsStat_Bungee['LocY'] = pd.to_numeric(bb_BallsStat_Bungee['LocY'], errors='coerce')
        bb_BallsStat_Bungee['OZone'] = pd.to_numeric(bb_BallsStat_Bungee['OZone'], errors='coerce')
        # bb_BallsStat_Bungee['APP_KZoneZ'] = bb_BallsStat_Bungee['APP_KZoneZ'].apply(lambda x: np.random.uniform(9, 2) if x <= 13 else x)
        # 刪除所有包含 NaN 的行
        bb_BallsStat_Bungee = bb_BallsStat_Bungee.dropna(subset=['APP_KZoneY', 'APP_KZoneZ']).reset_index(drop = True)
        HTMARK= {'':'',
                np.nan:'',
                'GROUND':'o',
                'FLYB':'^',
                'LINE': 's',
                'POPB':'^',
                None: ''}
        HTColor= {'':'',
                np.nan:'',
                'HARD':'#FF0000',
                'MED':'#FF3333',
                'SOFT': '#FF6666',
                None: ''}
        PRColor={'':''}
        Hlist=['1B','2B','3B','HR','IHR']
        Outlist=['E-DP','GT','IF','G-','G','F','SF','SH','E-T','E-C','E','E-SF','FOT','FOTE','E-SH','DP','TP','FC','E-SHT','E-SHC','FSH','INT','LO','OBC','UN-IO','OT-IP','DP-S','OT-PO']
        for i in Hlist:
            PRColor[i]='r'
        for i in Outlist:
            PRColor[i]='grey'

        bb_BallsStat_Bungee['HTColor'] = bb_BallsStat_Bungee['HardnessTag'].apply(
            lambda x: HTColor.get(x, 'grey') if HTColor.get(x, '') != '' else 'grey'
        )
        bb_BallsStat_Bungee['HTMark'] =bb_BallsStat_Bungee['HitType'].apply(lambda x: HTMARK.get(x, ''))
        def assign_prcolor(row):
            if row['PitchCode'] == 'In-Play':
                return PRColor.get(row['PA_Result'], 'grey')
            return 'grey'

        bb_BallsStat_Bungee['PRColor'] = bb_BallsStat_Bungee.apply(assign_prcolor, axis=1)
        return bb_BallsStat_Bungee
#十三宮格_投球(x座標, y座標, 寬, 高, 資料表, 底圖, 球種選擇)
    def zonePitch(self, left, bottom, width, height, dft, fig, pitchtype):

        pitchtype = pitchtype
        bgc = '#FFFFFF'
        # fig = plt.figure(figsize=(6.6,7.2),facecolor=bgc)
        axes1 = fig.add_axes([left, bottom, width, height],facecolor="#FFFFFF",zorder=20)

        # axes1 = fig.add_axes([0, 0, 1, 1],facecolor=bgc,zorder=20)
        line1 = [(-10,-5),(10,-5)]
        line2 = [(-10,-3),(-10,-5)]
        line3 = [(10,-3),(10,-5)]
        line4 = [(-10,-3),(0,0)]
        line5 = [(10,-3),(0,0)]
        line6 = [(-10,18),(-10,42)]
        line7 = [(10,18),(10,42)]
        line8 = [(-10,18),(10,18)]
        line9 = [(-10,42),(10,42)]

        (line1_xs, line1_ys) = zip(*line1)
        (line2_xs, line2_ys) = zip(*line2)
        (line3_xs, line3_ys) = zip(*line3)
        (line4_xs, line4_ys) = zip(*line4)
        (line5_xs, line5_ys) = zip(*line5)
        (line6_xs, line6_ys) = zip(*line6)
        (line7_xs, line7_ys) = zip(*line7)
        (line8_xs, line8_ys) = zip(*line8)
        (line9_xs, line9_ys) = zip(*line9)
        if pitchtype == "Total":
            dft = dft
        elif pitchtype == "Fastball":
            dft = dft[dft["TaggedPitchType"].isin(["FB","FT"])]
        elif pitchtype == "Non-Fastball":
            dft = dft[dft["TaggedPitchType"].isin(['SL','CT', 'CB', 'SC', 'CH', 'SP', 'SFF'])]
        try:
            Z1p='%.1f'%(len(dft[dft['OZone']==1])*100/len(dft))
        except:
            Z1p='--'
        try:
            Z2p='%.1f'%(len(dft[dft['OZone']==2])*100/len(dft))
        except:
            Z2p='--'
        try:
            Z3p='%.1f'%(len(dft[dft['OZone']==3])*100/len(dft))
        except:
            Z3p='--'
        try:
            Z4p='%.1f'%(len(dft[dft['OZone']==4])*100/len(dft))
        except:
            Z4p='--'
        try:
            Z5p='%.1f'%(len(dft[dft['OZone']==5])*100/len(dft))
        except:
            Z5p='--'
        try:
            Z6p='%.1f'%(len(dft[dft['OZone']==6])*100/len(dft))
        except:
            Z6p='--'
        try:
            Z7p='%.1f'%(len(dft[dft['OZone']==7])*100/len(dft))
        except:
            Z7p='--'
        try:
            Z8p='%.1f'%(len(dft[dft['OZone']==8])*100/len(dft))
        except:
            Z8p='--'
        try:
            Z9p='%.1f'%(len(dft[dft['OZone']==9])*100/len(dft))
        except:
            Z9p='--'
        try:
            Z11p='%.1f'%(len(dft[dft['OZone']==11])*100/len(dft))
        except:
            Z11p='--'
        try:
            Z12p='%.1f'%(len(dft[dft['OZone']==12])*100/len(dft))
        except:
            Z12p='--'
        try:
            Z13p='%.1f'%(len(dft[dft['OZone']==13])*100/len(dft))
        except:
            Z13p='--'
        try:
            Z14p='%.1f'%(len(dft[dft['OZone']==14])*100/len(dft))
        except:
            Z14p='--'

        c1=PitC((Z1p))
        c2=PitC((Z2p))
        c3=PitC((Z3p))
        c4=PitC((Z4p))
        c5=PitC((Z5p))
        c6=PitC((Z6p))
        c7=PitC((Z7p))
        c8=PitC((Z8p))
        c9=PitC((Z9p))
        c11=PitCOut((Z11p))
        c12=PitCOut((Z12p))
        c13=PitCOut((Z13p))
        c14=PitCOut((Z14p))

        Count=[]
        for i in range(1,14):
            if i<10:
                Count.append(len(dft[dft['OZone']==i]))
            if i>=10:
                Count.append(len(dft[dft['OZone']==(i+1)]))
        # print(len(Count))
        font={
            'weight':'black',
            'size':20 * 0.4,
        }
        font_low={
            'weight':'black',
            'size':15 * 0.4,
        }
        
        axes1.add_patch(
            patches.Rectangle(
                (-15, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c1,
                fill=True,
                zorder=90
            ) )
        axes1.text(-10,43,str(Z1p)+"%",fontdict=font,c=PiW((Z1p)),ha='center',zorder=100)
        axes1.text(-10,39,"("+str(Count[0]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiW((Z1p)),ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-5, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c2,
                fill=True,
                zorder=90
            ) )
        axes1.text(0,43,str(Z2p)+"%",fontdict=font,c=PiW((Z2p)),ha='center', zorder=100)
        axes1.text(0,39,"("+str(Count[1]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiW((Z2p)),ha='center',zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (5, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c3,
                fill=True,
                zorder=90
            ) )
        axes1.text(10,43,str(Z3p)+"%",fontdict=font,c=PiW((Z3p)),ha='center',zorder=100)
        axes1.text(10,39,"("+str(Count[2]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiW((Z3p)),ha='center',zorder=100)
        
        axes1.add_patch(
            patches.Rectangle(
                (-15, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c4,
                fill=True,
                zorder=90
            ) )
        axes1.text(-10,31,str(Z4p)+"%",fontdict=font,c=PiW((Z4p)),ha='center',zorder=100)
        axes1.text(-10,27,"("+str(Count[3]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiW((Z4p)),ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-5, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c5,
                fill=True,
                zorder=90
            ) )
        axes1.text(0,31,str(Z5p)+"%",fontdict=font,c=PiW((Z5p)),ha='center',zorder=100)
        axes1.text(0,27,"("+str(Count[4]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiW((Z5p)),ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (5, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c6,
                fill=True,
                zorder=90
            ) )
        axes1.text(10,31,str(Z6p)+"%",fontdict=font,c=PiW((Z6p)),ha='center',zorder=100)
        axes1.text(10,27,"("+str(Count[5]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiW((Z6p)),ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-15, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c7,
                fill=True,
                zorder=90
            ))
        axes1.text(-10,19,str(Z7p)+"%",fontdict=font,c=PiW((Z7p)),ha='center',zorder=100)
        axes1.text(-10,15,"("+str(Count[6]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiW((Z7p)),ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-5, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c8,
                fill=True,
                zorder=90
            ) )
        axes1.text(0,19,str(Z8p)+"%",fontdict=font,c=PiW((Z8p)),ha='center',zorder=100)
        axes1.text(0,15,"("+str(Count[7]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiW((Z8p)),ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (5, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c9,
                fill=True,
                zorder=90
            ) )
        
        axes1.text(10,19,str(Z9p)+"%",fontdict=font,c=PiW((Z9p)),ha='center',zorder=100)
        axes1.text(10,15,"("+str(Count[8]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiW((Z9p)),ha='center',zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c11,
                fill=True
            ) )
        axes1.text(-15,50,str(Z11p)+"%",fontdict=font,c=PiOW((Z11p)),ha='center',zorder=100)
        axes1.text(-10,50,"("+str(Count[9]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiOW((Z11p)),zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c13,
                fill=True
            ) )
        axes1.text(-15,8,str(Z13p)+"%",fontdict=font,c=PiOW((Z13p)),ha='center',zorder=100)
        axes1.text(-10,8,"("+str(Count[11]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiOW((Z13p)),zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                20,
                24,
                edgecolor = 'black',
                facecolor = c12,
                fill=True
            ) )
        axes1.text(5,50,str(Z12p)+"%",fontdict=font,c=PiOW((Z12p)),ha='center',zorder=100)
        axes1.text(10,50,"("+str(Count[10]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiOW((Z12p)),zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                20,
                24,
                edgecolor = 'black',
                facecolor = c14,
                fill=True
            ) )
        axes1.text(5,8,str(Z14p)+"%",fontdict=font,ha='center' ,c=PiOW((Z14p)),zorder=100)
        axes1.text(10,8,"("+str(Count[12]) + '/' + str(len(dft))+")",fontdict=font_low,c=PiOW((Z14p)),zorder=100)
        
        # axes1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        # axes1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        # axes1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        # axes1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        # axes1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        return axes1
#十三宮格_出棒(x座標, y座標, 寬, 高, 資料表, 底圖, 揮棒型態)
    def zoneSWING(self, left, bottom, width, height, dft, fig, swing_type):
        swing_type = swing_type
        bgc='#FFFFFF'
        axes1 = fig.add_axes([left, bottom, width, height],facecolor="#FFFFFF",zorder=20)

        line1 = [(-10,-5),(10,-5)]
        line2 = [(-10,-3),(-10,-5)]
        line3 = [(10,-3),(10,-5)]
        line4 = [(-10,-3),(0,0)]
        line5 = [(10,-3),(0,0)]
        line6 = [(-10,18),(-10,42)]
        line7 = [(10,18),(10,42)]
        line8 = [(-10,18),(10,18)]
        line9 = [(-10,42),(10,42)]

        (line1_xs, line1_ys) = zip(*line1)
        (line2_xs, line2_ys) = zip(*line2)
        (line3_xs, line3_ys) = zip(*line3)
        (line4_xs, line4_ys) = zip(*line4)
        (line5_xs, line5_ys) = zip(*line5)
        (line6_xs, line6_ys) = zip(*line6)
        (line7_xs, line7_ys) = zip(*line7)
        (line8_xs, line8_ys) = zip(*line8)
        (line9_xs, line9_ys) = zip(*line9)


        if swing_type == 'Swing':
            swing = dft[dft['PitchCode'].isin(["Strk-S", "Foul","In-Play"])]
            try:
                Z1p='%.1f'%(len(swing[swing['OZone']==1])*100/len(dft[dft['OZone'] == 1]))
            except:
                Z1p='--'
            try:
                Z2p='%.1f'%(len(swing[swing['OZone']==2])*100/len(dft[dft['OZone'] == 2]))
            except:
                Z2p='--'
            try:
                Z3p='%.1f'%(len(swing[swing['OZone']==3])*100/len(dft[dft['OZone'] == 3]))
            except:
                Z3p='--'
            try:
                Z4p='%.1f'%(len(swing[swing['OZone']==4])*100/len(dft[dft['OZone'] == 4]))
            except:
                Z4p='--'
            try:
                Z5p='%.1f'%(len(swing[swing['OZone']==5])*100/len(dft[dft['OZone'] == 5]))
            except:
                Z5p='--'
            try:
                Z6p='%.1f'%(len(swing[swing['OZone']==6])*100/len(dft[dft['OZone'] == 6]))
            except:
                Z6p='--'
            try:
                Z7p='%.1f'%(len(swing[swing['OZone']==7])*100/len(dft[dft['OZone'] == 7]))
            except:
                Z7p='--'
            try:
                Z8p='%.1f'%(len(swing[swing['OZone']==8])*100/len(dft[dft['OZone'] == 8]))
            except:
                Z8p='--'
            try:
                Z9p='%.1f'%(len(swing[swing['OZone']==9])*100/len(dft[dft['OZone'] == 9]))
            except:
                Z9p='--'
            try:
                Z11p='%.1f'%(len(swing[swing['OZone']==11])*100/len(dft[dft['OZone'] == 11]))
            except:
                Z11p='--'
            try:
                Z12p='%.1f'%(len(swing[swing['OZone']==12])*100/len(dft[dft['OZone'] == 12]))
            except:
                Z12p='--'
            try:
                Z13p='%.1f'%(len(swing[swing['OZone']==13])*100/len(dft[dft['OZone'] == 13]))
            except:
                Z13p='--'
            try:
                Z14p='%.1f'%(len(swing[swing['OZone']==14])*100/len(dft[dft['OZone'] == 14]))
            except:
                Z14p='--'
        
        elif swing_type == "Miss":
            swing = dft[(dft['PitchCode'].isin(["Strk-S", "Foul","In-Play"]))]
            miss = dft[dft['PitchCode'].isin(['Strk-S'])]
            try:
                Z1p='%.1f'%(len(miss[miss['OZone']==1])*100/len(swing[swing['OZone'] == 1]))
            except:
                Z1p='--'
            try:
                Z2p='%.1f'%(len(miss[miss['OZone']==2])*100/len(swing[swing['OZone'] == 2]))
            except:
                Z2p='--'
            try:
                Z3p='%.1f'%(len(miss[miss['OZone']==3])*100/len(swing[swing['OZone'] == 3]))
            except:
                Z3p='--'
            try:
                Z4p='%.1f'%(len(miss[miss['OZone']==4])*100/len(swing[swing['OZone'] == 4]))
            except:
                Z4p='--'
            try:
                Z5p='%.1f'%(len(miss[miss['OZone']==5])*100/len(swing[swing['OZone'] == 5]))
            except:
                Z5p='--'
            try:
                Z6p='%.1f'%(len(miss[miss['OZone']==6])*100/len(swing[swing['OZone'] == 6]))
            except:
                Z6p='--'
            try:
                Z7p='%.1f'%(len(miss[miss['OZone']==7])*100/len(swing[swing['OZone'] == 7]))
            except:
                Z7p='--'
            try:
                Z8p='%.1f'%(len(miss[miss['OZone']==8])*100/len(swing[swing['OZone'] == 8]))
            except:
                Z8p='--'
            try:
                Z9p='%.1f'%(len(miss[miss['OZone']==9])*100/len(swing[swing['OZone'] == 9]))
            except:
                Z9p='--'
            try:
                Z11p='%.1f'%(len(miss[miss['OZone']==11])*100/len(swing[swing['OZone'] == 11]))
            except:
                Z11p='--'
            try:
                Z12p='%.1f'%(len(miss[miss['OZone']==12])*100/len(swing[swing['OZone'] == 12]))
            except:
                Z12p='--'
            try:
                Z13p='%.1f'%(len(miss[miss['OZone']==13])*100/len(swing[swing['OZone'] == 13]))
            except:
                Z13p='--'
            try:
                Z14p='%.1f'%(len(miss[miss['OZone']==14])*100/len(swing[swing['OZone'] == 14]))
            except:
                Z14p='--'
        



        elif swing_type == "Non_FB Miss":
            swing = dft[(dft['PitchCode'].isin(["Strk-S", "Foul","In-Play"]))&(dft["TaggedPitchType"].isin(['SL','CT', 'CB', 'SC', 'CH', 'SP', 'SFF']))]
            miss = dft[dft['PitchCode'].isin(['Strk-S'])&(dft["TaggedPitchType"].isin(['SL','CT', 'CB', 'SC', 'CH', 'SP', 'SFF']))]
            try:
                Z1p='%.1f'%(len(miss[miss['OZone']==1])*100/len(swing[swing['OZone'] == 1]))
            except:
                Z1p='--'
            try:
                Z2p='%.1f'%(len(miss[miss['OZone']==2])*100/len(swing[swing['OZone'] == 2]))
            except:
                Z2p='--'
            try:
                Z3p='%.1f'%(len(miss[miss['OZone']==3])*100/len(swing[swing['OZone'] == 3]))
            except:
                Z3p='--'
            try:
                Z4p='%.1f'%(len(miss[miss['OZone']==4])*100/len(swing[swing['OZone'] == 4]))
            except:
                Z4p='--'
            try:
                Z5p='%.1f'%(len(miss[miss['OZone']==5])*100/len(swing[swing['OZone'] == 5]))
            except:
                Z5p='--'
            try:
                Z6p='%.1f'%(len(miss[miss['OZone']==6])*100/len(swing[swing['OZone'] == 6]))
            except:
                Z6p='--'
            try:
                Z7p='%.1f'%(len(miss[miss['OZone']==7])*100/len(swing[swing['OZone'] == 7]))
            except:
                Z7p='--'
            try:
                Z8p='%.1f'%(len(miss[miss['OZone']==8])*100/len(swing[swing['OZone'] == 8]))
            except:
                Z8p='--'
            try:
                Z9p='%.1f'%(len(miss[miss['OZone']==9])*100/len(swing[swing['OZone'] == 9]))
            except:
                Z9p='--'
            try:
                Z11p='%.1f'%(len(miss[miss['OZone']==11])*100/len(swing[swing['OZone'] == 11]))
            except:
                Z11p='--'
            try:
                Z12p='%.1f'%(len(miss[miss['OZone']==12])*100/len(swing[swing['OZone'] == 12]))
            except:
                Z12p='--'
            try:
                Z13p='%.1f'%(len(miss[miss['OZone']==13])*100/len(swing[swing['OZone'] == 13]))
            except:
                Z13p='--'
            try:
                Z14p='%.1f'%(len(miss[miss['OZone']==14])*100/len(swing[swing['OZone'] == 14]))
            except:
                Z14p='--'
                
        elif swing_type == "FB Miss":
            swing = dft[(dft['PitchCode'].isin(["Strk-S", "Foul","In-Play"]))&(dft["TaggedPitchType"].isin(['FB','FT']))]
            miss = dft[dft['PitchCode'].isin(['Strk-S'])&(dft["TaggedPitchType"].isin(['FB','FT']))]
            try:
                Z1p='%.1f'%(len(miss[miss['OZone']==1])*100/len(swing[swing['OZone'] == 1]))
            except:
                Z1p='--'
            try:
                Z2p='%.1f'%(len(miss[miss['OZone']==2])*100/len(swing[swing['OZone'] == 2]))
            except:
                Z2p='--'
            try:
                Z3p='%.1f'%(len(miss[miss['OZone']==3])*100/len(swing[swing['OZone'] == 3]))
            except:
                Z3p='--'
            try:
                Z4p='%.1f'%(len(miss[miss['OZone']==4])*100/len(swing[swing['OZone'] == 4]))
            except:
                Z4p='--'
            try:
                Z5p='%.1f'%(len(miss[miss['OZone']==5])*100/len(swing[swing['OZone'] == 5]))
            except:
                Z5p='--'
            try:
                Z6p='%.1f'%(len(miss[miss['OZone']==6])*100/len(swing[swing['OZone'] == 6]))
            except:
                Z6p='--'
            try:
                Z7p='%.1f'%(len(miss[miss['OZone']==7])*100/len(swing[swing['OZone'] == 7]))
            except:
                Z7p='--'
            try:
                Z8p='%.1f'%(len(miss[miss['OZone']==8])*100/len(swing[swing['OZone'] == 8]))
            except:
                Z8p='--'
            try:
                Z9p='%.1f'%(len(miss[miss['OZone']==9])*100/len(swing[swing['OZone'] == 9]))
            except:
                Z9p='--'
            try:
                Z11p='%.1f'%(len(miss[miss['OZone']==11])*100/len(swing[swing['OZone'] == 11]))
            except:
                Z11p='--'
            try:
                Z12p='%.1f'%(len(miss[miss['OZone']==12])*100/len(swing[swing['OZone'] == 12]))
            except:
                Z12p='--'
            try:
                Z13p='%.1f'%(len(miss[miss['OZone']==13])*100/len(swing[swing['OZone'] == 13]))
            except:
                Z13p='--'
            try:
                Z14p='%.1f'%(len(miss[miss['OZone']==14])*100/len(swing[swing['OZone'] == 14]))
            except:
                Z14p='--'



        if swing_type == 'Swing':
            c1=SwingC((Z1p))
            c2=SwingC((Z2p))
            c3=SwingC((Z3p))
            c4=SwingC((Z4p))
            c5=SwingC((Z5p))
            c6=SwingC((Z6p))
            c7=SwingC((Z7p))
            c8=SwingC((Z8p))
            c9=SwingC((Z9p))
            c11=SwingC((Z11p))
            c12=SwingC((Z12p))
            c13=SwingC((Z13p))
            c14=SwingC((Z14p))
        else:
            c1=WhiffC((Z1p))
            c2=WhiffC((Z2p))
            c3=WhiffC((Z3p))
            c4=WhiffC((Z4p))
            c5=WhiffC((Z5p))
            c6=WhiffC((Z6p))
            c7=WhiffC((Z7p))
            c8=WhiffC((Z8p))
            c9=WhiffC((Z9p))
            c11=WhiffC((Z11p))
            c12=WhiffC((Z12p))
            c13=WhiffC((Z13p))
            c14=WhiffC((Z14p))
            
        Count_mom=[]
        Count_son = []
        if swing_type =='Swing':
            for i in range(1,14):
                if i<10:
                    Count_mom.append(len(dft[dft['OZone']==i]))
                    Count_son.append(len(swing[swing['OZone']==i]))

                elif i>=10:
                    Count_mom.append(len(dft[dft['OZone']==(i+1)]))
                    Count_son.append(len(swing[swing['OZone']==(i+1)]))
        else:
            for i in range(1,14):
                if i < 10:
                    Count_mom.append(len(swing[swing['OZone']==i]))
                    Count_son.append(len(miss[miss['OZone']==i]))

                elif i>=10:
                    Count_mom.append(len(swing[swing['OZone']==(i+1)]))
                    Count_son.append(len(miss[miss['OZone']==(i+1)]))                

        # print(len(Count))
        font={
            'weight':'black',
            'size':20*0.4,
        }
        font_low={
            'weight':'black',
            'size':15*0.4,
        }

        axes1.add_patch(
            patches.Rectangle(
                (-15, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c1,
                fill=True,
                zorder=90
            ) )
        # axes1.text(-10,43,str(Z1p)+"%",fontdict=font,c=SwingW((Z1p)),ha='center',zorder=100)
        # axes1.text(-10,39,"("+str(Count_son[0]) + '/' + str(Count_mom[0]) + ")",fontdict=font_low,c=SwingW((Z1p)),ha='center',zorder=100)
        axes1.text(-10,43,str(Z1p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(-10,39,"("+str(Count_son[0]) + '/' + str(Count_mom[0]) + ")",fontdict=font_low,c='black',ha='center',zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (-5, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c2,
                fill=True,
                zorder=90
            ) )
        axes1.text(0,43,str(Z2p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(0,39,"("+str(Count_son[1]) + '/' + str(Count_mom[1])+")",fontdict=font_low,c='black',ha='center',zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (5, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c3,
                fill=True,
                zorder=90
            ) )
        axes1.text(10,43,str(Z3p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(10,39,"("+str(Count_son[2]) + '/' + str(Count_mom[2])+")",fontdict=font_low,c='black',ha='center',zorder=100)
        
        axes1.add_patch(
            patches.Rectangle(
                (-15, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c4,
                fill=True,
                zorder=90
            ) )
        axes1.text(-10,31,str(Z4p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(-10,27,"("+str(Count_son[3]) + '/' + str(Count_mom[3])+")",fontdict=font_low,c='black',ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-5, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c5,
                fill=True,
                zorder=90
            ) )
        axes1.text(0,31,str(Z5p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(0,27,"("+str(Count_son[4]) + '/' + str(Count_mom[4])+")",fontdict=font_low,c='black',ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (5, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c6,
                fill=True,
                zorder=90
            ) )
        axes1.text(10,31,str(Z6p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(10,27,"("+str(Count_son[5]) + '/' + str(Count_mom[5])+")",fontdict=font_low,c='black',ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-15, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c7,
                fill=True,
                zorder=90
            ) )
        axes1.text(-10,19,str(Z7p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(-10,15,"("+str(Count_son[6]) + '/' + str(Count_mom[6])+")",fontdict=font_low,c='black',ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-5, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c8,
                fill=True,
                zorder=90
            ) )
        axes1.text(0,19,str(Z8p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(0,15,"("+str(Count_son[7]) + '/' + str(Count_mom[7])+")",fontdict=font_low,c='black',ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (5, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c9,
                fill=True,
                zorder=90
            ) )
        axes1.text(10,19,str(Z9p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(10,15,"("+str(Count_son[8]) + '/' + str(Count_mom[8])+")",fontdict=font_low,c='black',ha='center',zorder=100)


        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c11,
                fill=True
            ) )
        axes1.text(-15,50,str(Z11p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(-10.5,50,"("+str(Count_son[9]) + '/' + str(Count_mom[9])+")",fontdict=font_low,c='black',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c13,
                fill=True
            ) )
        axes1.text(-15,8,str(Z13p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(-10.5,8,"("+str(Count_son[11]) + '/' + str(Count_mom[11])+")",fontdict=font_low,c='black',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                20,
                24,
                edgecolor = 'black',
                facecolor = c12,
                fill=True
            ) )
        axes1.text(5,50,str(Z12p)+"%",fontdict=font,c='black',ha='center',zorder=100)
        axes1.text(9.5,50,"("+str(Count_son[10]) + '/' + str(Count_mom[10])+")",fontdict=font_low,c='black',zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                20,
                24,
                edgecolor = 'black',
                facecolor = c14,
                fill=True
            ) )
        axes1.text(5,8,str(Z14p)+"%",fontdict=font, ha='center', c='black',zorder=100)
        axes1.text(9.5,8,"("+str(Count_son[12]) + '/' + str(Count_mom[12])+")",fontdict=font_low,c='black',zorder=100)
        

        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        return axes1
#十三宮格_打擊率(x座標, y座標, 寬, 高, 資料表, 底圖, 球種)
    def zoneAVG_B(self, left, bottom, width, height, dft, fig, pitchtype):

        pitchtype = pitchtype
        bgc = "#FFFFFF"
        axes1 = fig.add_axes([left, bottom, width, height],facecolor="#FFFFFF",zorder=20)

        line1 = [(-10,-5),(10,-5)]
        line2 = [(-10,-3),(-10,-5)]
        line3 = [(10,-3),(10,-5)]
        line4 = [(-10,-3),(0,0)]
        line5 = [(10,-3),(0,0)]
        line6 = [(-10,18),(-10,42)]
        line7 = [(10,18),(10,42)]
        line8 = [(-10,18),(10,18)]
        line9 = [(-10,42),(10,42)]

        (line1_xs, line1_ys) = zip(*line1)
        (line2_xs, line2_ys) = zip(*line2)
        (line3_xs, line3_ys) = zip(*line3)
        (line4_xs, line4_ys) = zip(*line4)
        (line5_xs, line5_ys) = zip(*line5)
        (line6_xs, line6_ys) = zip(*line6)
        (line7_xs, line7_ys) = zip(*line7)
        (line8_xs, line8_ys) = zip(*line8)
        (line9_xs, line9_ys) = zip(*line9)

        if pitchtype == "Total":
            PA = dft[dft['PA_Result'].isin([ 'G', '3B', 'K', 'FC', 'K-DO', 'LO', 'K-SF', 'K-DS', 'FOT', 'E-SHC', '1B', 'IF', '2B', 'G-', 'INT', 'HR', 'K-BS', 'E-C', 'GT', 'IHR', 'K-BF', 'Ks', 'DP','E-T', 'F'])]
            hit = dft[dft['PA_Result'].isin(['3B', '2B', 'HR', '1B', 'IHR'])]
        elif pitchtype == "Fastball_AVG":
            dft = dft[(dft['TaggedPitchType'].isin(['FB', 'FT']))]
            PA = dft[dft['PA_Result'].isin([ 'G', '3B', 'K', 'FC', 'K-DO', 'LO', 'K-SF', 'K-DS', 'FOT', 'E-SHC', '1B', 'IF', '2B', 'G-', 'INT', 'HR', 'K-BS', 'E-C', 'GT', 'IHR', 'K-BF', 'Ks', 'DP','E-T', 'F'])]
            hit = dft[dft['PA_Result'].isin(['3B', '2B', 'HR', '1B', 'IHR'])]
        elif pitchtype == 'Non-Fastball_AVG':
            dft = dft[(dft['TaggedPitchType'].isin(['SL', 'CT', 'CB', 'SC' ,'CH', 'SP', 'SFF', 'OT', 'KN']))]
            PA = dft[dft['PA_Result'].isin([ 'G', '3B', 'K', 'FC', 'K-DO', 'LO', 'K-SF', 'K-DS', 'FOT', 'E-SHC', '1B', 'IF', '2B', 'G-', 'INT', 'HR', 'K-BS', 'E-C', 'GT', 'IHR', 'K-BF', 'Ks', 'DP','E-T', 'F'])]
            hit = dft[dft['PA_Result'].isin(['3B', '2B', 'HR', '1B', 'IHR'])]   

        try:
            Z1p='%.3f'%(len(hit[hit['OZone']==1]) / len(PA[PA['OZone'] == 1]))
        except:
            Z1p='--'
        try:
            Z2p='%.3f'%(len(hit[hit['OZone']==2]) / len(PA[PA['OZone'] == 2]))
        except:
            Z2p='--'
        try:
            Z3p='%.3f'%(len(hit[hit['OZone']==3]) / len(PA[PA['OZone'] == 3]))
        except:
            Z3p='--'
        try:
            Z4p='%.3f'%(len(hit[hit['OZone']==4]) / len(PA[PA['OZone'] == 4]))
        except:
            Z4p='--'
        try:
            Z5p='%.3f'%(len(hit[hit['OZone']==5]) / len(PA[PA['OZone'] == 5]))
        except:
            Z5p='--'
        try:
            Z6p='%.3f'%(len(hit[hit['OZone']==6]) / len(PA[PA['OZone'] == 6]))
        except:
            Z6p='--'
        try:
            Z7p='%.3f'%(len(hit[hit['OZone']==7]) / len(PA[PA['OZone'] == 7]))
        except:
            Z7p='--'
        try:
            Z8p='%.3f'%(len(hit[hit['OZone']==8]) / len(PA[PA['OZone'] == 8]))
        except:
            Z8p='--'
        try:
            Z9p='%.3f'%(len(hit[hit['OZone']==9]) / len(PA[PA['OZone'] == 9]))
        except:
            Z9p='--'
        try:
            Z11p='%.3f'%(len(hit[hit['OZone']==11]) / len(PA[PA['OZone'] == 11]))
        except:
            Z11p='--'
        try:
            Z12p='%.3f'%(len(hit[hit['OZone']==12]) / len(PA[PA['OZone'] == 12]))
        except:
            Z12p='--'
        try:
            Z13p='%.3f'%(len(hit[hit['OZone']==13]) / len(PA[PA['OZone'] == 13]))
        except:
            Z13p='--'
        try:
            Z14p='%.3f'%(len(hit[hit['OZone']==14]) / len(PA[PA['OZone'] == 14]))
        except:
            Z14p='--'
        c1=HitC((Z1p))
        c2=HitC((Z2p))
        c3=HitC((Z3p))
        c4=HitC((Z4p))
        c5=HitC((Z5p))
        c6=HitC((Z6p))
        c7=HitC((Z7p))
        c8=HitC((Z8p))
        c9=HitC((Z9p))
        c11=HitC((Z11p))
        c12=HitC((Z12p))
        c13=HitC((Z13p))
        c14=HitC((Z14p))
        Count_hit=[]
        for i in range(1,14):
            if i<10:
                Count_hit.append(len(hit[hit['OZone']==i]))
            if i>=10:
                Count_hit.append(len(hit[hit['OZone']==(i+1)]))
        Count_PA=[]
        for i in range(1,14):
            if i<10:
                Count_PA.append(len(PA[PA['OZone']==i]))
            if i>=10:
                Count_PA.append(len(PA[PA['OZone']==(i+1)]))
        # print(len(Count))
        font={
            'weight':'black',
            'size':20 * 0.4,
        }
        font_low={
            'weight':'black',
            'size':15 * 0.4,
        }

        axes1.add_patch(
            patches.Rectangle(
                (-15, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c1,
                fill=True,
                zorder=90
            ) )
        axes1.text(-10, 43, str(Z1p), c="black",fontdict=font,ha='center', zorder=100)
        axes1.text(-10,39,"("+str(Count_hit[0]) + "/" + str(Count_PA[0])+")", c="black",fontdict=font_low,ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-5, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c2,
                fill=True,
                zorder=90
            ) )
        axes1.text(0,43,str(Z2p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(0,39,"("+str(Count_hit[1]) + "/" + str(Count_PA[1])+")", c="black",fontdict=font_low,ha='center',zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (5, 36),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c3,
                fill=True,
                zorder=90
            ) )
        axes1.text(10,43,str(Z3p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(10,39,"("+str(Count_hit[2]) + "/" + str(Count_PA[2])+")", c="black",fontdict=font_low,ha='center',zorder=100)
        
        axes1.add_patch(
            patches.Rectangle(
                (-15, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c4,
                fill=True,
                zorder=90
            ) )
        axes1.text(-10,31,str(Z4p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(-10,27,"("+str(Count_hit[3]) + "/" + str(Count_PA[3])+")", c="black",fontdict=font_low,ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-5, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c5,
                fill=True,
                zorder=90
            ) )
        axes1.text(0,31,str(Z5p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(0,27,"("+str(Count_hit[4]) + "/" + str(Count_PA[4])+")", c="black",fontdict=font_low,ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (5, 24),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c6,
                fill=True,
                zorder=90
            ) )
        axes1.text(10,31,str(Z6p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(10,27,"("+str(Count_hit[5]) + "/" + str(Count_PA[5])+")", c="black",fontdict=font_low,ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-15, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c7,
                fill=True,
                zorder=90
            ) )
        axes1.text(-10,19,str(Z7p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(-10,15,"("+str(Count_hit[6]) + "/" + str(Count_PA[6])+")", c="black",fontdict=font_low,ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (-5, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c8,
                fill=True,
                zorder=90
            ) )
        axes1.text(0,19,str(Z8p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(0,15,"("+str(Count_hit[7]) + "/" + str(Count_PA[7])+")", c="black",fontdict=font_low,ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (5, 12),
                30/3,
                12,
                edgecolor = 'black',
                facecolor = c9,
                fill=True,
                zorder=90
            ) )
        axes1.text(10,19,str(Z9p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(10,15,"("+str(Count_hit[8]) + "/" + str(Count_PA[8])+")", c="black",fontdict=font_low,ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c11,
                fill=True
            ) )
        axes1.text(-15,50,str(Z11p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(-9,50,"("+str(Count_hit[9]) + "/" + str(Count_PA[9])+")", c="black",fontdict=font_low,zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c13,
                fill=True
            ) )
        axes1.text(-15,8,str(Z13p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(-9,8,"("+str(Count_hit[11]) + "/" + str(Count_PA[11])+")", c="black",fontdict=font_low,zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                20,
                24,
                edgecolor = 'black',
                facecolor = c12,
                fill=True
            ) )
        axes1.text(5,50,str(Z12p), c="black",fontdict=font,ha='center',zorder=100)
        axes1.text(11,50,"("+str(Count_hit[10]) + "/" + str(Count_PA[10])+")", c="black",fontdict=font_low,zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                20,
                24,
                edgecolor = 'black',
                facecolor = c14,
                fill=True
            ) )
        axes1.text(5,8,str(Z14p), c="black",fontdict=font, ha='center', zorder=100)
        axes1.text(11,8,"("+str(Count_hit[12]) + "/" + str(Count_PA[12])+")", c="black",fontdict=font_low,zorder=100)
        


        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        return axes1
    
#熱力圖(x座標, y座標, 寬, 高, 資料表, 底圖, 篩選條件)
    def heatScenario(self, left, bottom, width, height, df, fig, scenario):
        scenario = scenario
#ALL
        if scenario == 'All':
            dft=df
#安打
        if scenario == '安打':
            dft=df[df['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR'])]
#出局
        elif scenario == '出局':
            dft=df[df['PA_Result'].isin(['DP','F','FC','FOT','G','G-','GT','IF','E-C','E-T'])]
#Ground pop
        elif scenario == 'GB+POP':
            dft=df[df['HitType'].isin(['GROUND', 'POP'])]
#弱擊球
        elif scenario == 'SOFT':
            dft=df[df['HardnessTag'].isin(['SOFT'])]  
#Call
        elif scenario == 'Call':
            dft=df[df['PitchCode'].isin(['Strk-C'])]
#Miss
        elif scenario == 'Miss':
            dft=df[df['PitchCode'].isin(['Strk-S'])]
#In-Play
        elif scenario == 'In-Play':
            dft=df[df['PitchCode'].isin(['In-Play'])]
#首球出棒
        elif scenario == "首球出棒":
            dft=df[(df['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play'])) & (dft['BS'].isin(['0-0']))] 
#三振
        elif scenario == '三振':
            dft = df[df['PA_Result'].isin(['K', 'Ks', 'K-DO', 'K-BS', 'K-BF', 'K-DS','K-SF'])]
#Swing
        elif scenario == 'Swing':
            dft = df[df['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play'])]
#首球
        elif scenario == "首球":
            dft=df[df['BS'].isin(['0-0'])] 
#投手領先
        elif scenario == "投手領先":
            dft=df[df['BS'].isin(['0-1','0-2','1-2'])] 
#打者領先
        elif scenario == "打者領先":
            dft=df[df['BS'].isin(['1-0','2-0','2-1','3-0','3-1','3-2'])] 
#平手
        elif scenario == "平手":
            dft=df[df['BS'].isin(['1-1','2-2'])] 
        bgc = '#FFFFFF'
        # fig = plt.figure(figsize=(6.6,7.2),facecolor=bgc)
        axes1 = fig.add_axes([left, bottom, width, height],facecolor="#FFFFFF",zorder=20)
        line1 = [(-10,-5),(10,-5)]
        line2 = [(-10,-3),(-10,-5)]
        line3 = [(10,-3),(10,-5)]
        line4 = [(-10,-3),(0,0)]
        line5 = [(10,-3),(0,0)]
        line6 = [(-10,18),(-10,42)]
        line7 = [(10,18),(10,42)]
        line8 = [(-10,18),(10,18)]
        line9 = [(-10,42),(10,42)]

        (line1_xs, line1_ys) = zip(*line1)
        (line2_xs, line2_ys) = zip(*line2)
        (line3_xs, line3_ys) = zip(*line3)
        (line4_xs, line4_ys) = zip(*line4)
        (line5_xs, line5_ys) = zip(*line5)
        (line6_xs, line6_ys) = zip(*line6)
        (line7_xs, line7_ys) = zip(*line7)
        (line8_xs, line8_ys) = zip(*line8)
        (line9_xs, line9_ys) = zip(*line9)

        ax1=axes1
        x1=dft['APP_KZoneY']
        y1=dft['APP_KZoneZ']
        ax1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line6_xs, line6_ys, linewidth=1, color='red',zorder=90))
        ax1.add_line(Line2D(line7_xs, line7_ys, linewidth=1, color='red',zorder=90))
        ax1.add_line(Line2D(line8_xs, line8_ys, linewidth=1, color='red',zorder=90))
        ax1.add_line(Line2D(line9_xs, line9_ys, linewidth=1, color='red',zorder=90))
        if len(x1)>6:
            plot=sns.set()
            plot=sns.kdeplot(data = dft ,x = 'APP_KZoneY',y = 'APP_KZoneZ',shade=True, cmap='coolwarm', n_levels=9,bw_adjust=0.65,alpha=0.75,thresh=0.24,ax=ax1,zorder=90)
        else:
            
            ax1.scatter(x1,y1,c='r',s=7*7,edgecolors='black')
        ax1.set_xlim(-33,33)
        ax1.set_ylim(-6,66)
        ax1.axis('off')
        return axes1
#長打熱力圖(x座標, y座標, 寬, 高, 資料表, 底圖)
    def slgScenario(self, left, bottom, width, height, df, fig, scenario):

    #長打
        scenario = '長打'
        dft=df[df['PA_Result'].isin(['1B','2B','3B','DP','F','FC','FOT','G','G-','GT','HR','K','K-BF','K-BS','K-DO','K-DS','K-SF','Ks','IF','IHR','E-C','E-T'])].reset_index(drop=True)  
        dft.APP_KZoneY=pd.to_numeric(dft.APP_KZoneY)
        dft.APP_KZoneZ=pd.to_numeric(dft.APP_KZoneZ)
        dft['SLG_Loc']=0
        for i in range(len(dft)):
            score=0
            AtBat=0
            for s in range(len(dft)):
                if float(np.sqrt((dft['APP_KZoneY'][i]-dft['APP_KZoneY'][s])**2+(dft['APP_KZoneZ'][i]-dft['APP_KZoneZ'][s])**2))<2:
                    AtBat+=1
                    if dft['PA_Result'][s]=='1B':
                        score+=1
                    if dft['PA_Result'][s]=='2B':
                        score+=2
                    if dft['PA_Result'][s]=='3B':
                        score+=3
                    if dft['PA_Result'][s]=='HR':
                        score+=4
                    if dft['PA_Result'][s]=='IHR':
                        score+=4
                    else:
                        score+=0
                else:
                    pass
            try:
                dft.loc[i,'SLG_Loc']=round(score/AtBat,3)
            except:
                pass
        bgc = '#FFFFFF'
        # fig = plt.figure(figsize=(6.6,7.2),facecolor=bgc)
        axes1 = fig.add_axes([left, bottom, width, height],facecolor="#FFFFFF",zorder=20)

        line1 = [(-10,-5),(10,-5)]
        line2 = [(-10,-3),(-10,-5)]
        line3 = [(10,-3),(10,-5)]
        line4 = [(-10,-3),(0,0)]
        line5 = [(10,-3),(0,0)]
        line6 = [(-10,18),(-10,42)]
        line7 = [(10,18),(10,42)]
        line8 = [(-10,18),(10,18)]
        line9 = [(-10,42),(10,42)]

        (line1_xs, line1_ys) = zip(*line1)
        (line2_xs, line2_ys) = zip(*line2)
        (line3_xs, line3_ys) = zip(*line3)
        (line4_xs, line4_ys) = zip(*line4)
        (line5_xs, line5_ys) = zip(*line5)
        (line6_xs, line6_ys) = zip(*line6)
        (line7_xs, line7_ys) = zip(*line7)
        (line8_xs, line8_ys) = zip(*line8)
        (line9_xs, line9_ys) = zip(*line9)

        ax1=axes1
        dfx=dft[dft['PitchCode']=='In-Play'].sort_values('SLG_Loc',ignore_index=False)
        dfx=dfx.reset_index(drop=True)
        x1=dfx['APP_KZoneY']
        y1=dfx['APP_KZoneZ']
        ax1.scatter(x1,y1,c=color(dfx),s=7*7,edgecolors='black')
        ax1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        ax1.add_line(Line2D(line6_xs, line6_ys, linewidth=1, color='red',zorder=90))
        ax1.add_line(Line2D(line7_xs, line7_ys, linewidth=1, color='red',zorder=90))
        ax1.add_line(Line2D(line8_xs, line8_ys, linewidth=1, color='red',zorder=90))
        ax1.add_line(Line2D(line9_xs, line9_ys, linewidth=1, color='red',zorder=90))
        ax1.set_xlim(-33,33)
        ax1.set_ylim(-6,66)
        ax1.axis('off')
        return axes1
#落點圖(x座標, y座標, 寬, 高, 資料表, 底圖, 篩選條件)
    def diammondScenario(self, left, bottom, width, height, dft, fig, scenario):       
        current_directory = os.path.dirname(__file__)
        image_path = current_directory + r'/Label_Data/落點底圖線圖-01.png'
        if scenario == 'GROUND':
            dfFar = dft[(dft['HitType'] == "GROUND")].reset_index(drop = True)
        elif scenario == "Total":
            dfFar = dft[(dft['HitType'] == "GROUND")].reset_index(drop = True)
            # dfFar = dft
        elif scenario == ['FLYB','POP','LINE','GROUND']:
            dfFar = dft[(dft['HitType'] == "GROUND")].reset_index(drop = True)

        elif scenario == "安打":
            dfFar = dft[(dft['HitType'] == "GROUND")&(dft['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR']))].reset_index(drop = True)
        elif scenario == ['2sG']:
            dfFar = dft[(dft['HitType'] == "GROUND")& (dft['BS'].isin(['0-2','1-2', '2-2','3-2']))].reset_index(drop = True)
        elif scenario == ['b2sG']:
            dfFar = dft[(dft['HitType'] == "GROUND")& (dft['BS'].isin(['0-0','0-1','1-0','1-1','2-1','3-1','2-0','3-0']))].reset_index(drop = True)
        else:
            dfFar = dft[(dft['HitType'] == "GROUND") & (dft['BS'].isin(scenario))].reset_index(drop = True)
        dfB=dft
        bgc='#FFFFFF'
        # fig = plt.figure(figsize=(3.6,3.3),facecolor=bgc)
        axes1 = fig.add_axes([left, bottom, width, height],facecolor=bgc,zorder=20)
        Pic = np.array(Image.open(image_path))
        # Pic = np.array(Image.open('C:/Users/lin14/OneDrive/桌面/CPBLReport/Label_Data/落點底圖線圖-01.png'))        
        # image = ax.imshow(Pic, cmap=plt.cm.gray, extent=[-400, 400, -100, 500],alpha=0.35)
        image = axes1.imshow(Pic, cmap=plt.cm.gray, extent=[-400, 400, -100, 500],alpha=1)

        if scenario == 'GROUND':
            df=dfB[(dfB['HitType']=='GROUND')]
        elif scenario == "Total":
            df = dfB[dfB["PitchCode"] == 'In-Play']
        elif scenario == "安打":
            df = dfB[dfB['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR'])]
        elif scenario == ['FLYB','POP','LINE']:
            df = dfB[dfB['HitType'].isin(['FLYB','POP','LINE'])]
        elif scenario == ['FLYB','POP','LINE','GROUND']:
            df = dfB[dfB['HitType'].isin(['FLYB','POP','LINE','GROUND'])]
        elif scenario == ['2sG']:
            df=dfB[(dfB['HitType']=='GROUND')]
            df = df[df['BS'].isin(['0-2','1-2', '2-2','3-2'])]
        elif scenario == ['2sF']:
            df = dfB[dfB['HitType'].isin(['FLYB','POP','LINE'])]
            df = df[df['BS'].isin(['0-2','1-2', '2-2','3-2'])]
        elif scenario == ['b2sG']:
            df=dfB[(dfB['HitType']=='GROUND')]
            df = df[df['BS'].isin(['0-0','0-1','1-0','1-1','2-1','3-1','2-0','3-0'])]
        elif scenario == ['b2sF']:
            df = dfB[dfB['HitType'].isin(['FLYB','POP','LINE'])]
            df = df[df['BS'].isin(['0-0','0-1','1-0','1-1','2-1','3-1','2-0','3-0'])]
        else:
            df = dfB[(dfB['PitchCode'] == 'In-Play')]
            df = df[df['BS'].isin(scenario)]
            # df = df[df['PitchCode'] == 'In-Play']
        # scLoc = mscatter(df['LocX'] , df['LocY'],c=list(df['PRColor']),s=(3)**2, m=list(df['HTMark']), ax=ax,alpha=0.5,picker=True,edgecolors='black',linewidth=0.3)
        scLoc = mscatter(df['LocX'] , df['LocY'],c=list(df['PRColor']),s=(3)**2, m=list(df['HTMark']), ax=axes1,alpha=1,picker=True,edgecolors='black',linewidth=0.3)

        #滾地球標線
        for disP in range(len(dfFar)):
            line3 = [(dfFar.LocX[disP],dfFar.LocY[disP]),(0,0)]
            (line3_xs, line3_ys) = zip(*line3)
            axes1.add_line(Line2D(line3_xs, line3_ys, ls='dashed',linewidth=0.5, color='#666666',zorder=90))

        axes1.set_xlim(-300,300)
        axes1.set_ylim(-100,500)
        axes1.get_yaxis().set_visible(False)
        axes1.get_xaxis().set_visible(False)
        axes1.spines['top'].set_visible(False)
        axes1.spines['right'].set_visible(False)
        axes1.spines['bottom'].set_visible(False)
        axes1.spines['left'].set_visible(False)
        return axes1
#擊球強度落點圖(x座標, y座標, 寬, 高, 資料表, 底圖, 強度)
    def diammondHardness(self, left, bottom, width, height, dft, fig,  hardness):
        current_directory = os.path.dirname(__file__)
        image_path = current_directory + r'/Label_Data/落點底圖線圖-01.png'
        if hardness == "Total_Hardness":
            df = dft[dft["PitchCode"] == 'In-Play']
            dfH=df[df['HardnessTag']=='HARD']
            dfM=df[df['HardnessTag']=='MED']
            dfS=df[df['HardnessTag']=='SOFT']
            bgc='#FFFFFF'
            # fig = plt.figure(figsize=(3.6,3.3),facecolor=bgc)
            axes1 = fig.add_axes([left, bottom, width, height],facecolor=bgc,zorder=20)
            ax=axes1
            Pic = np.array(Image.open(image_path))
            image = ax.imshow(Pic, cmap=plt.cm.gray, extent=[-400, 400, -100, 500],alpha=1)
            scLoc = mscatter(dfH['LocX'] , dfH['LocY'],c='#FF0000',s=(5)**2, m=list(dfH['HTMark']), ax=ax,alpha=1,picker=True,edgecolors='black',linewidth=0.3)
            scLoc = mscatter(dfM['LocX'] , dfM['LocY'],c='#FF6666',s=(5)**2, m=list(dfM['HTMark']), ax=ax,alpha=0.7,picker=True,edgecolors='black',linewidth=0.3)
            scLoc = mscatter(dfS['LocX'] , dfS['LocY'],c='#FFC7C7',s=(5)**2, m=list(dfS['HTMark']), ax=ax,alpha=0.3,picker=True,edgecolors='black',linewidth=0.3)
            ax.set_xlim(-300,300)
            ax.set_ylim(-100,500)
            R_C=len(df[df['Theta'].between(35,75)])
            M_C=len(df[df['Theta'].between(75,105)])
            L_C=len(df[df['Theta'].between(105,135)])
            H_C=len(df[df['HardnessTag']=='HARD'])
            O_C=len(df[df['HardnessTag']=='MED'])
            S_C=len(df[df['HardnessTag']=='SOFT'])
            
            ax.set_xlim(-300,300)
            ax.set_ylim(-100,500)
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
        return axes1
#球種比例(長條)(x座標, y座標, 寬, 高, 資料表, 底圖, Pitchcode)
    def arsenalCount(self, left, bottom, width, height, df, fig, scenario):
        current_directory = os.path.dirname(__file__)
        font_path = current_directory + r'/Label_Data/msjh.ttc'
        scenario = scenario
    #見逃  
        if scenario == 'Call' :
            dfB_Call=df[(df['PitchCode']=='Strk-C')]
        elif scenario == 'Miss':
            dfB_Call=df[(df['PitchCode']=='Strk-S')]
        elif scenario == 'In-Play':
            dfB_Call=df[(df['PitchCode']=='In-Play')]
        elif scenario == 'Swing':
            dfB_Call=df[(df['PitchCode'].isin(['In-Play', 'Foul', 'Strk-S']))]

        else :
            dfB_Call=df[~(df['PitchCode']=='')]
        
        bgc='#FFFFFF' 
        simsun =FontProperties(fname=font_path, size=10)   
        if len(dfB_Call)>0:
            # fig = plt.figure(figsize=(12,12),facecolor=bgc)
            axes7 = fig.add_axes([left, bottom, width, height],facecolor=bgc,zorder=20)
            Pt=[]
            Pc=[]
            for i in list(dfB_Call.groupby('TaggedPitchType').groups):
                df_Ta=dfB_Call.groupby('TaggedPitchType').get_group(i)
                Pt.append(i)
                Pc.append(len(df_Ta)/len(dfB_Call))
            df_Ta_C=pd.DataFrame({"TaggedPitchType":Pt,"Pc":Pc}).sort_values('Pc',ascending=1).reset_index(drop=True)
            LiC=[]
            LiT=[]
            for i in range(len(df_Ta_C)):
                LiC.append([])
                LiT.append([])
                LiT[i]=df_Ta_C.loc[i,'TaggedPitchType']
                LiC[i]=round(df_Ta_C.loc[i,'Pc']*100,1)
            x=[0]
            y=LiC[0]
            highTx=0
            
            axes7.bar(x, y,color=colorT(LiT[0]),ec='black',linewidth=1)
            for i in range(1,len(df_Ta_C)):
                highTx+=LiC[i-1]
                axes7.bar(x, LiC[i],bottom=highTx,color=colorT(LiT[i]),ec='black',linewidth=1)
            axes7.axis('off')
            axes7 = fig.add_axes([left, bottom, width, height],facecolor=bgc,zorder=20)
            highT=0
            for i in range(len(df_Ta_C)):
                if i==0:
                    highTT=LiC[0]/200
                else:
                    highT+=LiC[i-1]/100
                    highTT=highT+LiC[i]/200
                axes7.text(3.5,highTT,str(LiT[i])+":"+str(LiC[i])+"%",ha='center', va='center',fontsize=12,fontproperties=simsun)
            axes7.axis('off')
            return axes7
        else:
            fig = plt.figure(figsize=(12,12),facecolor=bgc)
            return fig
        


    def diammondScenario_fire(self, left, bottom, width, height, dft, fig, scenario):       
        current_directory = os.path.dirname(__file__)
        image_path = current_directory + r'/Label_Data/落點底圖線圖_兩條線.png'
        if scenario == 'GROUND':
            dfFar = dft[(dft['HitType'] == "GROUND")].reset_index(drop = True)
        elif scenario == "Total":
            dfFar = dft[(dft['HitType'] == "GROUND")].reset_index(drop = True)
            # dfFar = dft
        elif scenario == ['FLYB','POP','LINE','GROUND']:
            dfFar = dft[(dft['HitType'] == "GROUND")].reset_index(drop = True)

        elif scenario == "安打":
            dfFar = dft[(dft['HitType'] == "GROUND")&(dft['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR']))].reset_index(drop = True)
        elif scenario == ['2sG']:
            dfFar = dft[(dft['HitType'] == "GROUND")& (dft['BS'].isin(['0-2','1-2', '2-2','3-2']))].reset_index(drop = True)
        elif scenario == ['b2sG']:
            dfFar = dft[(dft['HitType'] == "GROUND")& (dft['BS'].isin(['0-0','0-1','1-0','1-1','2-1','3-1','2-0','3-0']))].reset_index(drop = True)
        else:
            dfFar = dft[(dft['HitType'] == "GROUND") & (dft['BS'].isin(scenario))].reset_index(drop = True)
        dfB=dft
        bgc='#FFFFFF'
        # fig = plt.figure(figsize=(3.6,3.3),facecolor=bgc)
        axes1 = fig.add_axes([left, bottom, width, height],facecolor=bgc,zorder=20)
        Pic = np.array(Image.open(image_path))
        # Pic = np.array(Image.open('C:/Users/lin14/OneDrive/桌面/CPBLReport/Label_Data/落點底圖線圖-01.png'))        
        # image = ax.imshow(Pic, cmap=plt.cm.gray, extent=[-400, 400, -100, 500],alpha=0.35)
        image = axes1.imshow(Pic, cmap=plt.cm.gray, extent=[-400, 400, -100, 500],alpha=1)

        if scenario == 'GROUND':
            df=dfB[(dfB['HitType']=='GROUND')]
        elif scenario == "Total":
            df = dfB[dfB["PitchCode"] == 'In-Play']
        elif scenario == "安打":
            df = dfB[dfB['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR'])]
        elif scenario == ['FLYB','POP','LINE']:
            df = dfB[dfB['HitType'].isin(['FLYB','POP','LINE'])]
        elif scenario == ['FLYB','POP','LINE','GROUND']:
            df = dfB[dfB['HitType'].isin(['FLYB','POP','LINE','GROUND'])]
        elif scenario == ['2sG']:
            df=dfB[(dfB['HitType']=='GROUND')]
            df = df[df['BS'].isin(['0-2','1-2', '2-2','3-2'])]
        elif scenario == ['2sF']:
            df = dfB[dfB['HitType'].isin(['FLYB','POP','LINE'])]
            df = df[df['BS'].isin(['0-2','1-2', '2-2','3-2'])]
        elif scenario == ['b2sG']:
            df=dfB[(dfB['HitType']=='GROUND')]
            df = df[df['BS'].isin(['0-0','0-1','1-0','1-1','2-1','3-1','2-0','3-0'])]
        elif scenario == ['b2sF']:
            df = dfB[dfB['HitType'].isin(['FLYB','POP','LINE'])]
            df = df[df['BS'].isin(['0-0','0-1','1-0','1-1','2-1','3-1','2-0','3-0'])]
        else:
            df = dfB[(dfB['PitchCode'] == 'In-Play')]
            df = df[df['BS'].isin(scenario)]
            # df = df[df['PitchCode'] == 'In-Play']
        # scLoc = mscatter(df['LocX'] , df['LocY'],c=list(df['PRColor']),s=(3)**2, m=list(df['HTMark']), ax=ax,alpha=0.5,picker=True,edgecolors='black',linewidth=0.3)
        scLoc = mscatter(df['LocX'] , df['LocY'],c=list(df['PRColor']),s=(3)**2, m=list(df['HTMark']), ax=axes1,alpha=1,picker=True,edgecolors='black',linewidth=0.3)

        #滾地球標線
        for disP in range(len(dfFar)):
            line3 = [(dfFar.LocX[disP],dfFar.LocY[disP]),(0,0)]
            (line3_xs, line3_ys) = zip(*line3)
            axes1.add_line(Line2D(line3_xs, line3_ys, ls='dashed',linewidth=0.5, color='#666666',zorder=90))

        axes1.set_xlim(-300,300)
        axes1.set_ylim(-100,500)
        axes1.get_yaxis().set_visible(False)
        axes1.get_xaxis().set_visible(False)
        axes1.spines['top'].set_visible(False)
        axes1.spines['right'].set_visible(False)
        axes1.spines['bottom'].set_visible(False)
        axes1.spines['left'].set_visible(False)
        return axes1

#逐球順序(x座標, y座標, 寬, 高, 資料表, 底圖)
    def plate_sequence(self, left, bottom, width, height, df, fig):
        bgc = "#FFFFFF"
        # fig = plt.figure(figsize=(6.6,7.2),facecolor=bgc)
        axes1 = fig.add_axes([left, bottom, width, height],facecolor=bgc,zorder=23)
        line1 = [(-10,-5),(10,-5)]
        line2 = [(-10,-3),(-10,-5)]
        line3 = [(10,-3),(10,-5)]
        line4 = [(-10,-3),(0,0)]
        line5 = [(10,-3),(0,0)]
        line6 = [(-10,18),(-10,42)]
        line7 = [(10,18),(10,42)]
        line8 = [(-10,18),(10,18)]
        line9 = [(-10,42),(10,42)]
#內虛線
        line10 = [(6.7, 22), (6.7, 38)]
        line11 = [(-6.7, 22), (-6.7, 38)]
        line12 = [(-6.7, 22), (6.7, 22)]
        line13 = [(-6.7, 38), (6.7, 38)]
#外虛線
        line14 = [(13.3, 14), (13.3, 46)]
        line15 = [(-13.3, 14), (-13.3, 46)]
        line16 = [(-13.3, 14), (13.3, 14)]
        line17 = [(-13.3, 46), (13.3, 46)]

        (line1_xs, line1_ys) = zip(*line1)
        (line2_xs, line2_ys) = zip(*line2)
        (line3_xs, line3_ys) = zip(*line3)
        (line4_xs, line4_ys) = zip(*line4)
        (line5_xs, line5_ys) = zip(*line5)
        (line6_xs, line6_ys) = zip(*line6)
        (line7_xs, line7_ys) = zip(*line7)
        (line8_xs, line8_ys) = zip(*line8)
        (line9_xs, line9_ys) = zip(*line9)
        (line10_xs, line10_ys) = zip(*line10)
        (line11_xs, line11_ys) = zip(*line11)
        (line12_xs, line12_ys) = zip(*line12)
        (line13_xs, line13_ys) = zip(*line13)
        (line14_xs, line14_ys) = zip(*line14)
        (line15_xs, line15_ys) = zip(*line15)
        (line16_xs, line16_ys) = zip(*line16)
        (line17_xs, line17_ys) = zip(*line17)
        
        x1=df['APP_KZoneY']
        y1=df['APP_KZoneZ']
#好球帶
        axes1.add_line(Line2D(line6_xs, line6_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line7_xs, line7_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line8_xs, line8_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line9_xs, line9_ys, linewidth=1, color='red',zorder=90))
#本壘板
        axes1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
#內虛線 
        # axes1.add_line(Line2D(line10_xs, line10_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        # axes1.add_line(Line2D(line11_xs, line11_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        # axes1.add_line(Line2D(line12_xs, line12_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        # axes1.add_line(Line2D(line13_xs, line13_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
#外虛線
        # axes1.add_line(Line2D(line14_xs, line14_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        # axes1.add_line(Line2D(line15_xs, line15_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        # axes1.add_line(Line2D(line16_xs, line16_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        # axes1.add_line(Line2D(line17_xs, line17_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        ball_num = 0
        while True:
            if ball_num > len(df) - 1:

                # print(pa, ball_num, len(df))

                # print(pa, ball_num, len(df))

                break
            if df.at[ball_num, 'PA_Result'] == '':
                # print(df.at[ball_num + pa_start_num, 'PA_Result'])
                x = df.at[ball_num, 'APP_KZoneY']
                y = df.at[ball_num, 'APP_KZoneZ']
                color = colorC(df)[ball_num]
                axes1.scatter(x, y, c = color, s=17*17, edgecolors='black')
                axes1.text(x-0.1, y-1.5, str(ball_num + 1),size = 16,ha='center', color = 'black')
                ball_num += 1
            else:
                # print(str(pa) + df.at[ball_num, 'PA_Result'])
                x = df.at[ball_num, 'APP_KZoneY']
                y = df.at[ball_num, 'APP_KZoneZ']
                color = colorC(df)[ball_num]
                axes1.scatter(x, y, c = color, s=17*17, edgecolors='black')
                axes1.text(x-0.1, y-1.5, str(ball_num + 1), size = 16,ha='center', color = 'black')
                ball_num += 1
                break

        return axes1