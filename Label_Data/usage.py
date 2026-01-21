from func import *
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.font_manager import FontProperties
from math import sqrt
simsun =FontProperties(fname=r'C:/Users/clayt/OneDrive/桌面/CPBLREPORT/Label_Data/msjh.ttc', size=10)
def usagelinechart(df_Spin):
    if len(df_Spin)>1:  
        bgc = '#FFFFFF'
        fig = plt.figure(figsize=(6.6,7.2),facecolor=bgc)
        axes1 = fig.add_axes([0, 0, 1, 1],facecolor=bgc,zorder=20)         
        df_Spin=df_Spin[~(df_Spin['TaggedPitchType'].isin(['UN','?','']))]
        df_Spin.APP_VeloRel=pd.to_numeric(df_Spin.APP_VeloRel)
        BallPercentage=[]
        VeloList=[]
        p=sns.displot(df_Spin, x="APP_VeloRel", hue="TaggedPitchType", kind="kde",)
        for i in range(len(plt.gca().get_lines())):
            BallPercentage.append(plt.gca().get_lines()[i].get_ydata().max())
        BallPercentage.sort(reverse=True)
        BallCounts=[]
        BallCountsP=[]
        for i in list(df_Spin.groupby('TaggedPitchType').groups):
            BallCounts.append(len(df_Spin.groupby('TaggedPitchType').get_group(i)))
            BallCountsP.append(len(df_Spin.groupby('TaggedPitchType').get_group(i))/len(df_Spin))
        dfPitchType=pd.DataFrame({'PitchType':list(df_Spin.groupby('TaggedPitchType').groups),'BallCounts':BallCounts,'BallCountsP':BallCountsP})
        dfPitchType_1=dfPitchType.sort_values(by=['BallCounts'],ascending=False).reset_index(drop=True)
        if len(dfPitchType_1) != len(BallPercentage):
            for i in range(len(dfPitchType_1)-len(BallPercentage)):
                BallPercentage.append('-')
        dfPitchType_1['BallPercentage']=BallPercentage
        dfPitchType_1=dfPitchType_1[(dfPitchType_1['BallCounts']>10)|(dfPitchType_1['BallCountsP']>0.01)]
        dfPitchType_1=dfPitchType_1.reset_index(drop=True)
        dfPitchType_1=dfPitchType_1.head(5)

        dfPx=df_Spin
        dfPx=dfPx[~(dfPx['TaggedPitchType'].isin(['UN','?','']))]
        dfPx.APP_VeloRel=pd.to_numeric(dfPx.APP_VeloRel)
        BallsP=[]
        BallsV=[]
        PitchT=[]
        for i in list(dfPx.groupby('TaggedPitchType').groups):
            if len(dfPx.groupby('TaggedPitchType').get_group(i))>=dfPitchType_1.BallCounts.min()  :
                BallsP.append(round((len(dfPx.groupby('TaggedPitchType').get_group(i)))*100/len(dfPx),1))
                BallsV.append(round(dfPx.groupby('TaggedPitchType').get_group(i).APP_VeloRel.mean(),1))
                PitchT.append(i)
        dfPitchTypex=pd.DataFrame({'PitchType':PitchT,'BallP':BallsP,'BallV':BallsV})
        dfPitchTypex_1=dfPitchTypex.sort_values(by=['BallP'],ascending=False).reset_index(drop=True)

        bgc='#6C6C6C'
        fig = plt.figure(figsize = (12, 12),facecolor=bgc)
        axes0 = fig.add_axes([0, 0, 1, 1])
        axes5 = fig.add_axes([0.05, 0.14, 0.9, 0.08],facecolor=bgc)
        axes4 = fig.add_axes([0.05, 0.31, 0.9, 0.08],facecolor=bgc)
        axes3 = fig.add_axes([0.05, 0.48, 0.9, 0.08],facecolor=bgc)
        axes2 = fig.add_axes([0.05, 0.65, 0.9, 0.08],facecolor=bgc)
        axes1 = fig.add_axes([0.05, 0.82, 0.9, 0.08],facecolor=bgc)
        axesL=[axes1,axes2,axes3,axes4,axes5]

        axes0.get_xaxis().set_visible(False)
        axes0.get_yaxis().set_visible(False)
        axes0.spines['top'].set_visible(False)
        axes0.spines['right'].set_visible(False)
        axes0.spines['bottom'].set_visible(False)
        axes0.spines['left'].set_visible(False)
        for t in [0,1,2,3,4]:
            try:
                sns.kdeplot(list(df_Spin[(df_Spin['TaggedPitchType'] == dfPitchType_1.PitchType[t]) & (df_Spin['APP_VeloRel'] > 0)].APP_VeloRel), fill=True, color=colorT(dfPitchType_1.PitchType[t])[0], ax=axesL[t], alpha=1, lw=0, zorder=10)
            except:
                pass
    for i in range(len(dfPitchType_1)):
        try:
            axesL[i].get_xaxis().set_visible(False)
            axesL[i].get_yaxis().set_visible(False)
            axesL[i].spines['top'].set_visible(False)
            axesL[i].spines['right'].set_visible(False)
            axesL[i].spines['bottom'].set_visible(False)
            axesL[i].spines['left'].set_visible(False)
            axesL[i].set_xlim([100,160])
            # x, y = axesL[i].get_children()[0].get_path()[0].vertices.T
            # sns.kdeplot(data=df_Spin, x='APP_VeloRel', ax=axesL[i], fill=True)

            # 獲取 PolyCollection 對象
            poly_collection = axesL[i].collections[0]

            # 遍歷每個多邊形，獲取路徑
            for path in poly_collection.get_paths():
                x, y = path.vertices.T

            maxid = y.argmax()
            yhei=y[maxid]
            if dfPitchType_1.BallPercentage[i]>10:
                axesL[i].set_ylim([0,yhei*(dfPitchType_1.BallPercentage[0]/(dfPitchType_1.BallPercentage[i]*7))])
                yheif=yhei*(dfPitchType_1.BallPercentage[0]/(dfPitchType_1.BallPercentage[i]*7))
            else:
                axesL[i].set_ylim([0,yhei*(((sqrt((dfPitchType_1.BallPercentage[0]/dfPitchType_1.BallPercentage[i])*100))*10)/100)])
                yheif=yhei*(((sqrt((dfPitchType_1.BallPercentage[0]/dfPitchType_1.BallPercentage[i])*100))*10)/100)
            if i ==0:
                velohigh=yhei
            axesL[i].patch.set_alpha(0.01)
            axesL[i].spines['bottom'].set_color(colorTx(dfPitchType_1.PitchType[i]))
            TagB=list(dfPitchTypex_1.PitchType)[i]
            BallsUseP=list(dfPitchTypex_1.BallP)[i]
            AvgVel=list(dfPitchTypex_1.BallV)[i]
            axesL[i].text(100,yheif*0.5, '\n'.join(PTran(TagB)), ha='center', va='center',fontsize=30,fontproperties=simsun,c='black',zorder=90)
            axesL[i].text(106,yheif, '%', ha='center', va='center',fontsize=22,fontproperties=simsun,c='black',zorder=90)
            axesL[i].text(113,yheif, '均速', ha='center', va='center',fontsize=22,fontproperties=simsun,c='black',zorder=90)
            axesL[i].text(106,yheif*0.4, BallsUseP, ha='center', va='center',fontsize=24,fontproperties=simsun,c='black',zorder=90)
            axesL[i].text(113,yheif*0.4, AvgVel, ha='center', va='center',fontsize=24,fontproperties=simsun,c='black',zorder=90)
        except:
            pass
    for i in range(len(dfPitchType_1),5):
        try:
            axesL[i].get_xaxis().set_visible(False)
            axesL[i].get_yaxis().set_visible(False)
            axesL[i].spines['top'].set_visible(False)
            axesL[i].spines['right'].set_visible(False)
            axesL[i].spines['bottom'].set_visible(False)
            axesL[i].spines['left'].set_visible(False)
            axesL[i].set_xlim([100,170])
            x, y = axesL[i].get_children()[0].get_paths()[0].vertices.T
            maxid = y.argmax()
            yhei=y[maxid]
            axesL[i].set_ylim([0,yhei*(dfPitchType_1.BallPercentage[i]/dfPitchType_1.BallPercentage[i])])
            axesL[i].patch.set_alpha(0.01)
            axesL[i].spines['bottom'].set_color(colorTx(dfPitchType_1.PitchType[i]))

        except:
            pass
    axesL[len(dfPitchType_1)-1].set_xlim([100,170])
    axesL[len(dfPitchType_1)-1].get_xaxis().set_visible(True)
    axesL[len(dfPitchType_1)-1].tick_params(axis='x', colors='black',labelsize=20,width=5,length=10)
    return fig