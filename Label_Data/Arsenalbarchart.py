from func import *
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties

   
def arsenalCount( df, scenario):
    scenario = scenario
#見逃  
    if scenario == 'Call' :
        dfB_Call=df[(df['PitchCode']=='Strk-C')]
    elif scenario == 'Miss':
        dfB_Call=df[(df['PitchCode']=='Strk-S')]
    elif scenario == 'In-Play':
        dfB_Call=df[(df['PitchCode']=='In-Play')]
    else :
        dfB_Call=df[~(df['PitchCode']=='')]
    
    bgc='#FFFFFF' 
    simsun =FontProperties(fname=r'C:/Users/clayt/OneDrive/桌面/CPBLREPORT/Label_Data/msjh.ttc', size=10)   
    if len(dfB_Call)>0:
        fig = plt.figure(figsize=(12,12),facecolor=bgc)
        axes7 = fig.add_axes([0.6, 0.105, 0.02, 0.28],facecolor=bgc,zorder=20)
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
        axes8 = fig.add_axes([0.65, 0.105, 0.02, 0.28],facecolor=bgc,zorder=20)
        highT=0
        for i in range(len(df_Ta_C)):
            if i==0:
                highTT=LiC[0]/200
            else:
                highT+=LiC[i-1]/100
                highTT=highT+LiC[i]/200
            axes8.text(0.01,highTT,str(LiT[i])+":"+str(LiC[i])+"%",ha='center', va='center',fontsize=12,fontproperties=simsun)
        axes8.axis('off')
        return fig
    else:
        fig = plt.figure(figsize=(12,12),facecolor=bgc)
        return fig