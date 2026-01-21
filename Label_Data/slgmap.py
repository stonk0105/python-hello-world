from func import *
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# class Slgmap:

    # def __init__(self):
    #     pass    
def slgScenario(df, scenario):
    scenario = scenario
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
    fig = plt.figure(figsize=(6.6,7.2),facecolor=bgc)
    axes1 = fig.add_axes([0, 0, 1, 1],facecolor=bgc,zorder=20)
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
    ax1.scatter(x1,y1,c=color(dfx),s=20*20,edgecolors='black')
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
    return fig
     