from func import *
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import seaborn as sns

# class Slgmap:

    # def __init__(self):
    #     pass    
def heatmapScenario(df, scenario):
    scenario = scenario
    dft = df
#安打
    if scenario == '安打':
        dft=dft[dft['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR'])]
#Ground pop
    elif scenario == 'GB':
        dft=dft[dft['HitType'].isin(['GROUND'])]
#FLY
    elif scenario == 'FLY':
        dft=dft[dft['HitType'].isin(['FLYB','LINE'])]
#POP
    elif scenario == 'POP':
        dft=dft[dft['HitType'].isin(['POPB'])]
#Miss
    elif scenario == 'Miss':
        dft=dft[dft['PitchCode'].isin(['Strk-S'])]
#Swing
    elif scenario == 'Swing':
        dft = dft[dft['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play'])]  
#超過200英尺
    elif scenario == 'FAR':
        dft = dft[dft['HitType'].isin(['FLYB','LINE'])&(dft['ExitDistance']>=300)]  



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
        plot=sns.kdeplot(data = dft ,x = 'APP_KZoneY',y = 'APP_KZoneZ',shade=True, cmap='coolwarm', shade_lowest=False, n_levels=9,bw_adjust=0.65,alpha=0.75,thresh=0.24,ax=ax1,zorder=90)
    else:
        
        ax1.scatter(x1,y1,c='r',s=20*20,edgecolors='black')
    ax1.set_xlim(-33,33)
    ax1.set_ylim(-6,66)
    ax1.axis('off')
    axes1.scatter(x1,y1,c=colorC(dft),s=8*8,edgecolors='black',zorder=100,alpha=0.5)
    axes1.set_xlim(-33,33)
    axes1.set_ylim(-6,66)
    axes1.axis('off')
    return fig
     