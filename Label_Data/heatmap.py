from func import *
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import seaborn as sns

class heatmap:

    def __init__(self):
        pass        
    
#scenario: 安打, GB+POP, Call, Miss, In-Play, 首球出棒, Swing, 打者領先, 投手領先, 平手, 首球
    def heatScenario(self, df, scenario):
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
            dft=df[df['HitType'].isin(['GROUND', 'POPB'])]
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
            plot=sns.kdeplot(data = dft ,x = 'APP_KZoneY',y = 'APP_KZoneZ',shade=True, cmap='coolwarm', shade_lowest=False, n_levels=9,bw_adjust=0.65,alpha=0.5,thresh=0.24,ax=ax1,zorder=90)
        else:
            
            ax1.scatter(x1,y1,c='r',s=20*20,edgecolors='black')
        ax1.set_xlim(-33,33)
        ax1.set_ylim(-6,66)
        ax1.axis('off')
        return fig
        




   