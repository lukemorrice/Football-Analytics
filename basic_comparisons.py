import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd


def xG_xA():
    # name, league, xG, xA
    players = [("Gabriel Jesus", 'Premier League', 0.84, 0.10),
                ("Erling Haland", 'Bundesliga', 0.85, 0.06), 
                ("Marcus Rashford", 'Premier League', 0.4, 0.13), 
                ("Kylian Mbappe", 'Ligue 1', 0.99, 0.51), 
                ("Joao Felix", 'La Liga', 0.35, 0.14), 
                ("Lautaro Martinez", 'Serie A', 0.53, 0.09), 
                ("Timo Werner", 'Bundesliga', 0.62, 0.27)]

    df = pd.DataFrame(players, columns=['name', 'league', 'xG', 'xA'])    
    ax = sns.scatterplot(x="xG", y="xA", hue="league", data=df, s=100)

    for player in range(0, df.shape[0]):
        ax.text(df.xG[player]+0.01, df.xA[player]+0.01, df.name[player].split(' ')[1], fontsize=12)

    ax.set(xlabel='Expected Goals', ylabel='Expected Assists')
    h, l = ax.get_legend_handles_labels()
    plt.legend(h[1:], l[1:])
    ax.set_title('Player Comparison: xG vs xA')   
    plt.show()


def touches_inpenbox():
    # name, league, touches, % in penalty box (not normalised)
    players = [("Gabriel Jesus", 'Premier League', 588, round(144/588, 4)),
                ("Erling Haland", 'Bundesliga', 192, round(38/192, 4)), 
                ("Marcus Rashford", 'Premier League', 854, round(115/854, 4)), 
                ("Kylian Mbappe", 'Ligue 1', 904, round(208/904, 4)), 
                ("Joao Felix", 'La Liga', 582, round(65/582, 4)), 
                ("Lautaro Martinez", 'Serie A', 610, round(151/610, 4)), 
                ("Timo Werner", 'Bundesliga', 1014, round(200/1014, 4))]
    
    df = pd.DataFrame(players, columns=['name', 'league', 'touches', 'perc_in_box'])
    df['perc_in_box'] = df['perc_in_box'] * 100
    ax = sns.scatterplot(x=df.perc_in_box, y="touches", hue="league", data=df, s=100)

    for player in range(0, df.shape[0]):
        if (df.name[player].split(' ')[1] == 'Jesus'):
            ax.text(df.perc_in_box[player]+0.25, df.touches[player]-25, df.name[player].split(' ')[1], fontsize=10)
        else:
            ax.text(df.perc_in_box[player]+0.25, df.touches[player]+0.5, df.name[player].split(' ')[1], fontsize=10)

    ax.set(ylabel='Number of Touches', xlabel='Percentage of Touches in Opposition Box')
    h, l = ax.get_legend_handles_labels()
    plt.legend(h[1:], l[1:], loc='lower left')
    ax.set_title('Unnormalised: Touches vs Percentage of Touches in Opposition Box')
    plt.show()

touches_inpenbox()