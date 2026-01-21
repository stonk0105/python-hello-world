from func import *
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt


class platelocation:

    def __init__(self):
        pass

    def plateCount(self, dft, counts):
        counts = counts

        dft=dft[dft['BS'].isin(counts)]

        bgc = "#FFFFFF"
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
        
        x1=dft['APP_KZoneY']
        y1=dft['APP_KZoneZ']
        axes1.add_line(Line2D(line6_xs, line6_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line7_xs, line7_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line8_xs, line8_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line9_xs, line9_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        axes1.scatter(x1,y1,c=colorC(dft),s=15*15,edgecolors='black')
        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        return fig
    
    def plateTaggedPitchType(self, dft, pt):
        pt = pt

        dft=dft[dft['TaggedPitchType'].isin(pt)]

        bgc = "#FFFFFF"
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
        
        x1=dft['APP_KZoneY']
        y1=dft['APP_KZoneZ']
        axes1.add_line(Line2D(line6_xs, line6_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line7_xs, line7_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line8_xs, line8_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line9_xs, line9_ys, linewidth=1, color='red',zorder=90))
        axes1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        axes1.scatter(x1,y1,c=colorC(dft),s=15*15,edgecolors='black')
        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        return fig
    
#scenario: 安打, GB+POP, Call, Miss, In-Play, 首球出棒, Swing
    def plateScenario(self, dft, scenario):
        scenario = scenario
#安打
        if scenario == '安打':
            dft=dft[dft['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR'])]
#直球安打
        if scenario == '直球安打':
            dft=dft[(dft['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR']))&(dft['TaggedPitchType'].isin(['FT','FB']))]
#變化球安打
        if scenario == '變化球安打':
            dft=dft[dft['PA_Result'].isin(['1B', '2B', '3B', 'HR', 'IHR'])&(~(dft['TaggedPitchType'].isin(['FT','FB'])))]
#Ground pop
        elif scenario == 'GB+POP':
            dft=dft[dft['HitType'].isin(['GROUND', 'POPB'])]
#FLY
        elif scenario == 'FLY':
            dft=dft[dft['HitType'].isin(['FLYB'])]
#Call
        elif scenario == 'Call':
            dft=dft[dft['PitchCode'].isin(['Strk-C'])]
#Miss
        elif scenario == 'Miss':
            dft=dft[dft['PitchCode'].isin(['Strk-S'])]
#In-Play
        elif scenario == 'In-Play':
            dft=dft[dft['PitchCode'].isin(['In-Play'])]
#首球出棒
        elif scenario == "首球出棒":
            dft=dft[(dft['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play'])) & (dft['BS'].isin(['0-0']))] 
#三振
        elif scenario == '三振':
            dft = dft[dft['PA_Result'].isin(['K', 'Ks', 'K-DO', 'K-BS', 'K-BF', 'K-DS','K-SF'])]
#Swing
        elif scenario == 'Swing':
            dft = dft[dft['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play'])]
#Swing
        elif scenario == 'O-Swing':
            dft = dft[(dft['PitchCode'].isin(['Strk-S', 'Foul', 'In-Play']))& (dft['Zone'] == 0)]
#Total  
        elif scenario == 'Total':
            dft = dft[~(dft['TaggedPitchType'].isnull())]
#出局
        elif scenario == '出局':
            dft=dft[dft['PA_Result'].isin(['DP','F','FC','FOT','G','G-','GT','IF','E-C','E-T','K', 'Ks', 'K-DO', 'K-BS', 'K-BF', 'K-DS','K-SF'])]
       
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

        x1=dft['APP_KZoneY']
        y1=dft['APP_KZoneZ']
        axes1.add_line(Line2D(line6_xs, line6_ys, linewidth=1.5, color='red',zorder=90))
        axes1.add_line(Line2D(line7_xs, line7_ys, linewidth=1.5, color='red',zorder=90))
        axes1.add_line(Line2D(line8_xs, line8_ys, linewidth=1.5, color='red',zorder=90))
        axes1.add_line(Line2D(line9_xs, line9_ys, linewidth=1.5, color='red',zorder=90))
        axes1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        axes1.scatter(x1,y1,c=colorC(dft),s=15*15,edgecolors='black')
        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        return fig
    def plate_sequence(self, df):
        bgc = "#FFFFFF"
        fig = plt.figure(figsize=(6.6,7.2),facecolor=bgc)
        axes1 = fig.add_axes([0, 0, 1, 1],facecolor=bgc,zorder=23)
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
        axes1.add_line(Line2D(line10_xs, line10_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        axes1.add_line(Line2D(line11_xs, line11_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        axes1.add_line(Line2D(line12_xs, line12_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        axes1.add_line(Line2D(line13_xs, line13_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
#外虛線
        axes1.add_line(Line2D(line14_xs, line14_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        axes1.add_line(Line2D(line15_xs, line15_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        axes1.add_line(Line2D(line16_xs, line16_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        axes1.add_line(Line2D(line17_xs, line17_ys, linewidth=1, color='black',zorder=90, linestyle = (0, (5,10))))
        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        ball_num = 0
        while True:
            if ball_num > len(df) - 1:
                # print(pa, ball_num, len(df))
                break
            if df.at[ball_num, 'PA_Result'] == 0:
                # print(df.at[ball_num + pa_start_num, 'PA_Result'])
                x = df.at[ball_num, 'APP_KZoneY']
                y = df.at[ball_num, 'APP_KZoneZ']
                color = df.at[ball_num, 'color']
                axes1.scatter(x, y, c = color, s=28*28, edgecolors='black')
                axes1.text(x-0.1, y-1, str(ball_num + 1),size = 23,ha='center')
                ball_num += 1
            else:
                # print(str(pa) + df.at[ball_num, 'PA_Result'])
                x = df.at[ball_num, 'APP_KZoneY']
                y = df.at[ball_num, 'APP_KZoneZ']
                color = df.at[ball_num, 'color']
                axes1.scatter(x, y, c = color, s=28*28, edgecolors='black')
                axes1.text(x-0.1, y-1, str(ball_num + 1), size = 23,ha='center')
                ball_num += 1
                break
        return fig