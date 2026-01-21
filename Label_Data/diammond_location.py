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
            dfFar = dft[(dft['HitType'] == "GROUND")].reset_index(drop = True)
        elif scenario == "Total":
            dfFar = dft[(dft['HitType'] == "GROUND")].reset_index(drop = True)
            # dfFar = dft

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
        fig = plt.figure(figsize=(3.6,3.3),facecolor=bgc)
        axes1 = fig.add_axes([0, 0, 1, 1],facecolor=bgc,zorder=20)
        ax=axes1
        Pic = np.array(Image.open('C:/Users/clayt/OneDrive/桌面/CPBLREPORT/Label_Data/落點底圖線圖-01.png'))
        # Pic = np.array(Image.open('C:/Users/lin14/OneDrive/桌面/CPBLReport/Label_Data/落點底圖線圖-01.png'))        
        # image = ax.imshow(Pic, cmap=plt.cm.gray, extent=[-400, 400, -100, 500],alpha=0.35)
        image = ax.imshow(Pic, cmap=plt.cm.gray, extent=[-400, 400, -100, 500],alpha=1)

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
        scLoc = mscatter(df['LocX'] , df['LocY'],c=list(df['PRColor']),s=(3)**2, m=list(df['HTMark']), ax=ax,alpha=1,picker=True,edgecolors='black',linewidth=0.3)

        #滾地球標線
        for disP in range(len(dfFar)):
            line3 = [(dfFar.LocX[disP],dfFar.LocY[disP]),(0,0)]
            (line3_xs, line3_ys) = zip(*line3)
            ax.add_line(Line2D(line3_xs, line3_ys, ls='dashed',linewidth=0.5, color='#666666',zorder=90))

        ax.set_xlim(-300,300)
        ax.set_ylim(-100,500)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

    def diammondHardness(self, dft, hardness):
        if hardness == "Total_Hardness":
            df = dft[dft["PitchCode"] == 'In-Play']
            dfH=df[df['HardnessTag']=='HARD']
            dfM=df[df['HardnessTag']=='MED']
            dfS=df[df['HardnessTag']=='SOFT']
            bgc='#FFFFFF'
            fig = plt.figure(figsize=(3.6,3.3),facecolor=bgc)
            axes1 = fig.add_axes([0, 0, 1, 1],facecolor=bgc,zorder=20)
            ax=axes1
            Pic = np.array(Image.open('C:/Users/clayt/OneDrive/桌面/CPBLREPORT/Label_Data/落點底圖線圖-01.png'))
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



