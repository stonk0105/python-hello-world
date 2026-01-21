from func import *
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


class diammondlocation:
    def __init__(self):
        pass

# scenario: GROUND, Total, ['counts']
    def diammondScenario(self, dft, scenario):       
        if scenario == 'GROUND':
            dfFar = dft[(dft['HitType'] == "GROUND")]  .reset_index(drop = True)
        elif scenario == "Total":
            dfFar = dft[(dft['HitType'] == "GROUND")]  .reset_index(drop = True)

        if scenario == "Total" :
            dfFly = dft[(dft['HitType'].isin(['FLYB','POPB','LINE']))]  .reset_index(drop = True)
        dfB=dft
        bgc='#FFFFFF'
        fig = plt.figure(figsize=(3.6,3.3),facecolor=bgc)
        axes1 = fig.add_axes([0, 0, 1, 1],facecolor=bgc,zorder=20)
        ax=axes1
        Pic = np.array(Image.open('C:/Users/clayt/OneDrive/桌面/CPBLREPORT/Label_Data/落點底圖線圖-01.png'))
        # Pic = np.array(Image.open('C:/Users/lin14/OneDrive/桌面/CPBLReport/Label_Data/落點底圖線圖-01.png'))        
        image = ax.imshow(Pic, cmap=plt.cm.gray, extent=[-400, 400, -100, 500],alpha=1)

        if scenario == 'GROUND':
            df=dfB[(dfB['HitType']=='GROUND')]
        elif scenario == "Total":
            df = dfB[dfB["PitchCode"] == 'In-Play']
        scLoc = mscatter(df['LocX'] , df['LocY'],c=list(df['PRColor']),s=(3)**2, m=list(df['HTMark']), ax=ax,alpha=1,picker=True,edgecolors='black',linewidth=0.3)

        #滾地球標線
        for disP in range(len(dfFar)):
            line3 = [(dfFar.LocX[disP],dfFar.LocY[disP]),(0,0)]
            (line3_xs, line3_ys) = zip(*line3)
            ax.add_line(Line2D(line3_xs, line3_ys, ls='dashed',linewidth=0.5, color='#666666',zorder=90))
        #飛球標線
        for disF in range(len(dfFly)):
            line4 = [(dfFly.LocX[disF],dfFly.LocY[disF]),(0,0)]
            (line4_xs, line4_ys) = zip(*line4)
            ax.add_line(Line2D(line4_xs, line4_ys,linewidth=0.5, color='#666666',zorder=90))

        ax.set_xlim(-300,300)
        ax.set_ylim(-100,510)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False) 