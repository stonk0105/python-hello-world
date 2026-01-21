from func import *
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

class Zonethirteen:
    def __init__(self):
        pass
    def zonePitch(self,dft, pitchtype):
        pitchtype = pitchtype
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
            'size':20,
        }
        font_low={
            'weight':'black',
            'size':15,
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
        axes1.text(0,43,str(Z2p)+"%",fontdict=font,c=PiW((Z2p)),ha='center',zorder=100)
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
            ) )
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
        
        axes1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        return fig
    
    def zoneAVG_B(self, dft, pitchtype):

        pitchtype = pitchtype
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

        if pitchtype == "Total":
            PA = dft[dft['PA_Result'].isin([ 'G', '3B', 'K', 'FC', 'K-DO', 'LO', 'K-SF', 'K-DS', 'FOT', 'E-SHC', '1B', 'IF', '2B', 'G-', 'INT', 'HR', 'K-BS', 'E-C', 'GT', 'IHR', 'K-BF', 'Ks', 'DP','E-T', 'F'])]
            hit = dft[dft['PA_Result'].isin(['3B', '2B', 'HR', '1B', 'IHR'])]
        elif pitchtype == "Fastball":
            dft = dft[(dft['TaggedPitchType'].isin(['FB', 'FT']))]
            PA = dft[dft['PA_Result'].isin([ 'G', '3B', 'K', 'FC', 'K-DO', 'LO', 'K-SF', 'K-DS', 'FOT', 'E-SHC', '1B', 'IF', '2B', 'G-', 'INT', 'HR', 'K-BS', 'E-C', 'GT', 'IHR', 'K-BF', 'Ks', 'DP','E-T', 'F'])]
            hit = dft[dft['PA_Result'].isin(['3B', '2B', 'HR', '1B', 'IHR'])]
        elif pitchtype == 'Non-Fastball':
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
            'size':20,
        }
        font_low={
            'weight':'black',
            'size':15,
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
        axes1.text(-10, 43, str(Z1p), fontdict=font,ha='center', zorder=100)
        axes1.text(-10,39,"("+str(Count_hit[0]) + "/" + str(Count_PA[0])+")",fontdict=font_low,ha='center',zorder=100)
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
        axes1.text(0,43,str(Z2p),fontdict=font,ha='center',zorder=100)
        axes1.text(0,39,"("+str(Count_hit[1]) + "/" + str(Count_PA[1])+")",fontdict=font_low,ha='center',zorder=100)

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
        axes1.text(10,43,str(Z3p),fontdict=font,ha='center',zorder=100)
        axes1.text(10,39,"("+str(Count_hit[2]) + "/" + str(Count_PA[2])+")",fontdict=font_low,ha='center',zorder=100)
        
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
        axes1.text(-10,31,str(Z4p),fontdict=font,ha='center',zorder=100)
        axes1.text(-10,27,"("+str(Count_hit[3]) + "/" + str(Count_PA[3])+")",fontdict=font_low,ha='center',zorder=100)
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
        axes1.text(0,31,str(Z5p),fontdict=font,ha='center',zorder=100)
        axes1.text(0,27,"("+str(Count_hit[4]) + "/" + str(Count_PA[4])+")",fontdict=font_low,ha='center',zorder=100)
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
        axes1.text(10,31,str(Z6p),fontdict=font,ha='center',zorder=100)
        axes1.text(10,27,"("+str(Count_hit[5]) + "/" + str(Count_PA[5])+")",fontdict=font_low,ha='center',zorder=100)
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
        axes1.text(-10,19,str(Z7p),fontdict=font,ha='center',zorder=100)
        axes1.text(-10,15,"("+str(Count_hit[6]) + "/" + str(Count_PA[6])+")",fontdict=font_low,ha='center',zorder=100)
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
        axes1.text(0,19,str(Z8p),fontdict=font,ha='center',zorder=100)
        axes1.text(0,15,"("+str(Count_hit[7]) + "/" + str(Count_PA[7])+")",fontdict=font_low,ha='center',zorder=100)
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
        axes1.text(10,19,str(Z9p),fontdict=font,ha='center',zorder=100)
        axes1.text(10,15,"("+str(Count_hit[8]) + "/" + str(Count_PA[8])+")",fontdict=font_low,ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c11,
                fill=True
            ) )
        axes1.text(-15,50,str(Z11p),fontdict=font,ha='center',zorder=100)
        axes1.text(-9,50,"("+str(Count_hit[9]) + "/" + str(Count_PA[9])+")",fontdict=font_low,zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c13,
                fill=True
            ) )
        axes1.text(-15,8,str(Z13p),fontdict=font,ha='center',zorder=100)
        axes1.text(-9,8,"("+str(Count_hit[11]) + "/" + str(Count_PA[11])+")",fontdict=font_low,zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                20,
                24,
                edgecolor = 'black',
                facecolor = c12,
                fill=True
            ) )
        axes1.text(5,50,str(Z12p),fontdict=font,ha='center',zorder=100)
        axes1.text(11,50,"("+str(Count_hit[10]) + "/" + str(Count_PA[10])+")",fontdict=font_low,zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                20,
                24,
                edgecolor = 'black',
                facecolor = c14,
                fill=True
            ) )
        axes1.text(5,8,str(Z14p),fontdict=font, ha='center', zorder=100)
        axes1.text(11,8,"("+str(Count_hit[12]) + "/" + str(Count_PA[12])+")",fontdict=font_low,zorder=100)
        


        axes1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        return fig
    
    def zoneSWING(self, dft, swing_type):
                swing_type = swing_type
                bgc='#FFFFFF'
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
                    swing = dft[dft['PitchCode'].isin(["Strk-S", "Foul","In-Play"])]
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
                    'size':20,
                }
                font_low={
                    'weight':'black',
                    'size':15,
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
                axes1.text(-10,43,str(Z1p)+"%",fontdict=font,c=SwingW((Z1p)),ha='center',zorder=100)
                axes1.text(-10,39,"("+str(Count_son[0]) + '/' + str(Count_mom[0]) + ")",fontdict=font_low,c=SwingW((Z1p)),ha='center',zorder=100)
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
                axes1.text(0,43,str(Z2p)+"%",fontdict=font,c=SwingW((Z2p)),ha='center',zorder=100)
                axes1.text(0,39,"("+str(Count_son[1]) + '/' + str(Count_mom[1])+")",fontdict=font_low,c=SwingW((Z2p)),ha='center',zorder=100)

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
                axes1.text(10,43,str(Z3p)+"%",fontdict=font,c=SwingW((Z3p)),ha='center',zorder=100)
                axes1.text(10,39,"("+str(Count_son[2]) + '/' + str(Count_mom[2])+")",fontdict=font_low,c=SwingW((Z3p)),ha='center',zorder=100)
                
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
                axes1.text(-10,31,str(Z4p)+"%",fontdict=font,c=SwingW((Z4p)),ha='center',zorder=100)
                axes1.text(-10,27,"("+str(Count_son[3]) + '/' + str(Count_mom[3])+")",fontdict=font_low,c=SwingW((Z4p)),ha='center',zorder=100)
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
                axes1.text(0,31,str(Z5p)+"%",fontdict=font,c=SwingW((Z5p)),ha='center',zorder=100)
                axes1.text(0,27,"("+str(Count_son[4]) + '/' + str(Count_mom[4])+")",fontdict=font_low,c=SwingW((Z5p)),ha='center',zorder=100)
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
                axes1.text(10,31,str(Z6p)+"%",fontdict=font,c=SwingW((Z6p)),ha='center',zorder=100)
                axes1.text(10,27,"("+str(Count_son[5]) + '/' + str(Count_mom[5])+")",fontdict=font_low,c=SwingW((Z6p)),ha='center',zorder=100)
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
                axes1.text(-10,19,str(Z7p)+"%",fontdict=font,c=SwingW((Z7p)),ha='center',zorder=100)
                axes1.text(-10,15,"("+str(Count_son[6]) + '/' + str(Count_mom[6])+")",fontdict=font_low,c=SwingW((Z7p)),ha='center',zorder=100)
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
                axes1.text(0,19,str(Z8p)+"%",fontdict=font,c=SwingW((Z8p)),ha='center',zorder=100)
                axes1.text(0,15,"("+str(Count_son[7]) + '/' + str(Count_mom[7])+")",fontdict=font_low,c=SwingW((Z8p)),ha='center',zorder=100)
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
                axes1.text(10,19,str(Z9p)+"%",fontdict=font,c=SwingW((Z9p)),ha='center',zorder=100)
                axes1.text(10,15,"("+str(Count_son[8]) + '/' + str(Count_mom[8])+")",fontdict=font_low,c=SwingW((Z9p)),ha='center',zorder=100)


                axes1.add_patch(
                    patches.Rectangle(
                        (0, 30),
                        -20,
                        24,
                        edgecolor = 'black',
                        facecolor = c11,
                        fill=True
                    ) )
                axes1.text(-15,50,str(Z11p)+"%",fontdict=font,c=SwingW((Z11p)),ha='center',zorder=100)
                axes1.text(-10.5,50,"("+str(Count_son[9]) + '/' + str(Count_mom[9])+")",fontdict=font_low,c=SwingW((Z11p)),zorder=100)
                axes1.add_patch(
                    patches.Rectangle(
                        (0, 6),
                        -20,
                        24,
                        edgecolor = 'black',
                        facecolor = c13,
                        fill=True
                    ) )
                axes1.text(-15,8,str(Z13p)+"%",fontdict=font,c=SwingW((Z13p)),ha='center',zorder=100)
                axes1.text(-10.5,8,"("+str(Count_son[11]) + '/' + str(Count_mom[11])+")",fontdict=font_low,c=SwingW((Z13p)),zorder=100)
                axes1.add_patch(
                    patches.Rectangle(
                        (0, 30),
                        20,
                        24,
                        edgecolor = 'black',
                        facecolor = c12,
                        fill=True
                    ) )
                axes1.text(5,50,str(Z12p)+"%",fontdict=font,c=SwingW((Z12p)),ha='center',zorder=100)
                axes1.text(9.5,50,"("+str(Count_son[10]) + '/' + str(Count_mom[10])+")",fontdict=font_low,c=SwingW((Z12p)),zorder=100)

                axes1.add_patch(
                    patches.Rectangle(
                        (0, 6),
                        20,
                        24,
                        edgecolor = 'black',
                        facecolor = c14,
                        fill=True
                    ) )
                axes1.text(5,8,str(Z14p)+"%",fontdict=font, ha='center', c=SwingW((Z14p)),zorder=100)
                axes1.text(9.5,8,"("+str(Count_son[12]) + '/' + str(Count_mom[12])+")",fontdict=font_low,c=SwingW((Z14p)),zorder=100)
                
                axes1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
                axes1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
                axes1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
                axes1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
                axes1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
                axes1.set_xlim(-33,33)
                axes1.set_ylim(-6,66)
                axes1.axis('off')
                return fig
    
    def zoneSLG_B(self, dft, pitchtype):

        pitchtype = pitchtype
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

        if pitchtype == "Total":
            df_AB = dft[dft['PA_Result'].isin([ 'G', '3B', 'K', 'FC', 'K-DO', 'LO', 'K-SF', 'K-DS', 'FOT', 'E-SHC', '1B', 'IF', '2B', 'G-', 'INT', 'HR', 'K-BS', 'E-C', 'GT', 'IHR', 'K-BF', 'Ks', 'DP',  'E-T', 'F'])]
            df_1B=dft[dft['PA_Result']=='1B']
            df_2B=dft[dft['PA_Result']=='2B']
            df_3B=dft[dft['PA_Result']=='3B']
            df_HR=dft[dft['PA_Result'].isin(['HR','IHR'])]
        elif pitchtype == "Fastball":
            df_AB = dft[dft['PA_Result'].isin([ 'G', '3B', 'K', 'FC', 'K-DO', 'LO', 'K-SF', 'K-DS', 'FOT', 'E-SHC', '1B', 'IF', '2B', 'G-', 'INT', 'HR', 'K-BS', 'E-C', 'GT', 'IHR', 'K-BF', 'Ks', 'DP',  'E-T', 'F'])]
            df_1B=dft[dft['PA_Result']=='1B']
            df_2B=dft[dft['PA_Result']=='2B']
            df_3B=dft[dft['PA_Result']=='3B']
            df_HR=dft[dft['PA_Result'].isin(['HR','IHR'])]
        elif pitchtype == 'Non-Fastball':
            df_AB = dft[dft['PA_Result'].isin([ 'G', '3B', 'K', 'FC', 'K-DO', 'LO', 'K-SF', 'K-DS', 'FOT', 'E-SHC', '1B', 'IF', '2B', 'G-', 'INT', 'HR', 'K-BS', 'E-C', 'GT', 'IHR', 'K-BF', 'Ks', 'DP',  'E-T', 'F'])]
            df_1B=dft[dft['PA_Result']=='1B']
            df_2B=dft[dft['PA_Result']=='2B']
            df_3B=dft[dft['PA_Result']=='3B']
            df_HR=dft[dft['PA_Result'].isin(['HR','IHR'])]   

        try:
            Z1p='%.3f'%((len(df_1B[df_1B['OZone']==1])+2*len(df_2B[df_2B['OZone']==1])+3*len(df_3B[df_3B['OZone']==1])+4*len(df_HR[df_HR['OZone']==1]))/len(df_AB[df_AB['OZone']==1]))
        except:
            Z1p='--'
        try:
            Z2p='%.3f'%((len(df_1B[df_1B['OZone']==2])+2*len(df_2B[df_2B['OZone']==2])+3*len(df_3B[df_3B['OZone']==2])+4*len(df_HR[df_HR['OZone']==2]))/len(df_AB[df_AB['OZone']==2]))
        except:
            Z2p='--'
        try:
            Z3p='%.3f'%((len(df_1B[df_1B['OZone']==3])+2*len(df_2B[df_2B['OZone']==3])+3*len(df_3B[df_3B['OZone']==3])+4*len(df_HR[df_HR['OZone']==3]))/len(df_AB[df_AB['OZone']==3]))
        except:
            Z3p='--'
        try:
            Z4p='%.3f'%((len(df_1B[df_1B['OZone']==4])+2*len(df_2B[df_2B['OZone']==4])+3*len(df_3B[df_3B['OZone']==4])+4*len(df_HR[df_HR['OZone']==4]))/len(df_AB[df_AB['OZone']==4]))
        except:
            Z4p='--'
        try:
            Z5p='%.3f'%((len(df_1B[df_1B['OZone']==5])+2*len(df_2B[df_2B['OZone']==5])+3*len(df_3B[df_3B['OZone']==5])+4*len(df_HR[df_HR['OZone']==5]))/len(df_AB[df_AB['OZone']==5]))
        except:
            Z5p='--'
        try:
            Z6p='%.3f'%((len(df_1B[df_1B['OZone']==6])+2*len(df_2B[df_2B['OZone']==6])+3*len(df_3B[df_3B['OZone']==6])+4*len(df_HR[df_HR['OZone']==6]))/len(df_AB[df_AB['OZone']==6]))
        except:
            Z6p='--'
        try:
            Z7p='%.3f'%((len(df_1B[df_1B['OZone']==7])+2*len(df_2B[df_2B['OZone']==7])+3*len(df_3B[df_3B['OZone']==7])+4*len(df_HR[df_HR['OZone']==7]))/len(df_AB[df_AB['OZone']==7]))
        except:
            Z7p='--'
        try:
            Z8p='%.3f'%((len(df_1B[df_1B['OZone']==8])+2*len(df_2B[df_2B['OZone']==8])+3*len(df_3B[df_3B['OZone']==8])+4*len(df_HR[df_HR['OZone']==8]))/len(df_AB[df_AB['OZone']==8]))
        except:
            Z8p='--'
        try:
            Z9p='%.3f'%((len(df_1B[df_1B['OZone']==9])+2*len(df_2B[df_2B['OZone']==9])+3*len(df_3B[df_3B['OZone']==9])+4*len(df_HR[df_HR['OZone']==9]))/len(df_AB[df_AB['OZone']==9]))
        except:
            Z9p='--'
        try:
            Z11p='%.3f'%((len(df_1B[df_1B['OZone']==11])+2*len(df_2B[df_2B['OZone']==11])+3*len(df_3B[df_3B['OZone']==11])+4*len(df_HR[df_HR['OZone']==11]))/len(df_AB[df_AB['OZone']==11]))
        except:
            Z11p='--'
        try:
            Z12p='%.3f'%((len(df_1B[df_1B['OZone']==12])+2*len(df_2B[df_2B['OZone']==12])+3*len(df_3B[df_3B['OZone']==12])+4*len(df_HR[df_HR['OZone']==12]))/len(df_AB[df_AB['OZone']==12]))
        except:
            Z12p='--'
        try:
            Z13p='%.3f'%((len(df_1B[df_1B['OZone']==13])+2*len(df_2B[df_2B['OZone']==13])+3*len(df_3B[df_3B['OZone']==13])+4*len(df_HR[df_HR['OZone']==13]))/len(df_AB[df_AB['OZone']==13]))
        except:
            Z13p='--'
        try:
            Z14p='%.3f'%((len(df_1B[df_1B['OZone']==14])+2*len(df_2B[df_2B['OZone']==14])+3*len(df_3B[df_3B['OZone']==14])+4*len(df_HR[df_HR['OZone']==14]))/len(df_AB[df_AB['OZone']==14]))
        except:
            Z14p='--'
        c1=HitCSLG((Z1p))
        c2=HitCSLG((Z2p))
        c3=HitCSLG((Z3p))
        c4=HitCSLG((Z4p))
        c5=HitCSLG((Z5p))
        c6=HitCSLG((Z6p))
        c7=HitCSLG((Z7p))
        c8=HitCSLG((Z8p))
        c9=HitCSLG((Z9p))
        c11=HitCSLG((Z11p))
        c12=HitCSLG((Z12p))
        c13=HitCSLG((Z13p))
        c14=HitCSLG((Z14p))
        font={
            'weight':'black',
            'size':20,
        }
        font_low={
            'weight':'black',
            'size':15,
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
        axes1.text(-10, 43, str(Z1p), fontdict=font,ha='center', zorder=100)
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
        axes1.text(0,43,str(Z2p),fontdict=font,ha='center',zorder=100)

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
        axes1.text(10,43,str(Z3p),fontdict=font,ha='center',zorder=100)
        
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
        axes1.text(-10,31,str(Z4p),fontdict=font,ha='center',zorder=100)
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
        axes1.text(0,31,str(Z5p),fontdict=font,ha='center',zorder=100)
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
        axes1.text(10,31,str(Z6p),fontdict=font,ha='center',zorder=100)
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
        axes1.text(-10,19,str(Z7p),fontdict=font,ha='center',zorder=100)
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
        axes1.text(0,19,str(Z8p),fontdict=font,ha='center',zorder=100)
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
        axes1.text(10,19,str(Z9p),fontdict=font,ha='center',zorder=100)
        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c11,
                fill=True
            ) )
        axes1.text(-15,50,str(Z11p),fontdict=font,ha='center',zorder=100)

        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                -20,
                24,
                edgecolor = 'black',
                facecolor = c13,
                fill=True
            ) )
        axes1.text(-15,8,str(Z13p),fontdict=font,ha='center',zorder=100)
    
        axes1.add_patch(
            patches.Rectangle(
                (0, 30),
                20,
                24,
                edgecolor = 'black',
                facecolor = c12,
                fill=True
            ) )
        axes1.text(5,50,str(Z12p),fontdict=font,ha='center',zorder=100)
        

        axes1.add_patch(
            patches.Rectangle(
                (0, 6),
                20,
                24,
                edgecolor = 'black',
                facecolor = c14,
                fill=True
            ) )
        axes1.text(5,8,str(Z14p),fontdict=font, ha='center', zorder=100)
    
        


        axes1.add_line(Line2D(line1_xs, line1_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line2_xs, line2_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line3_xs, line3_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line4_xs, line4_ys, linewidth=1, color='black',zorder=90))
        axes1.add_line(Line2D(line5_xs, line5_ys, linewidth=1, color='black',zorder=90))
        axes1.set_xlim(-33,33)
        axes1.set_ylim(-6,66)
        axes1.axis('off')
        return fig