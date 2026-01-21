from func import *
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
def Runchart(df):
    taggedpitchtype_color = {
        'FB': '#FF0000',
        'CB': '#0080FF',
        'CH': '#007500',
        'FT': '#b62170',
        'SL': '#FFFF37',
        'SP': '#FF8000',
        'CT': '#613030',
        'SFF': '#D94600',
        'SC': "#00f2ff",
        'KN': '#6F00D2'
    }
    taggedpitchtype = list(set(df['TaggedPitchType']))

    x = list(set(df['Date']))
    x.sort()
    x1 = []
    for i in range(0, len(x)):
        x_date = datetime.strptime(x[i], '%Y-%m-%d')
        x1.append(x_date.strftime('%m/%d'))
    df_arsenal = {'GameNo': x}
    df_arsenal = pd.DataFrame(df_arsenal)
    try:
        taggedpitchtype.remove('?')
    except:
        pass
    try:
        taggedpitchtype.remove('')
    except:
        pass
    try:
        taggedpitchtype.remove('UN')
    except:
        pass
    try:
        taggedpitchtype.remove('OT')
    except:
        pass
    arsenal_list = []
    
    for i in range(0, len(taggedpitchtype)):
        new_list = []
        for gameno in  range(0, len(x)):
            new_list.append(round(len(df[(df['TaggedPitchType'] == taggedpitchtype[i]) & (df['Date'] == x[gameno])]) * 100 / len(df[df['Date'] == x[gameno]]), 1))

        arsenal_list.append(new_list)
    for i in range(0, len(taggedpitchtype)):
        df_arsenal.insert(i, str(taggedpitchtype[i]), arsenal_list[i])
    df_arsenal = df_arsenal.sort_values(by = ['GameNo'])
    bgc = '#FFFFFF'
    fig = plt.figure(figsize=(11.69, 4.135),facecolor=bgc)
    axes1 = fig.add_axes([0, 0, 1, 1],facecolor=bgc,zorder=20)
    for i in range(0, len(taggedpitchtype)):
        plt.plot(x1,df_arsenal.iloc[:, i], linestyle="-", linewidth="1", markersize="12", marker=".", color = taggedpitchtype_color[taggedpitchtype[i]])
    plt.xticks(fontsize = 8)
    return fig
