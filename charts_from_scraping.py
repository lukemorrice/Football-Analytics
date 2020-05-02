import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd
from player import Player

class ChartMaker(list):

    def __init__(self, players_list):
        self.players = []
        for player in players:
            pl = Player(player)
            self.players.append(pl)

    def expected_goals_assists(self, season):
        
        data = []
        for player in self.players:
            row = []
            xG = float(player.df[player.df.index == season]['Per 90 Minutes']['xG'].iloc[0])
            xA = float(player.df[player.df.index == season]['Per 90 Minutes']['xA'].iloc[0])
            row = (player.name, player.league, xG, xA)
            data.append(row)
        
        df = pd.DataFrame(data, columns=['name', 'league', 'xG', 'xA'])        
        ax = sns.scatterplot(x="xG", y="xA", hue="league", data=df, s=100)

        for player in range(0, df.shape[0]):
            ax.text(df.xG[player]+0.01, df.xA[player]+0.01, df.name[player].split(' ')[1], fontsize=12)

        ax.set(xlabel='Expected Goals', ylabel='Expected Assists')
        h, l = ax.get_legend_handles_labels()
        plt.legend(h[1:], l[1:])
        ax.set_title('Player Comparison: xG vs xA')   
        plt.show()


players = ["Gabriel Jesus", "Kylian Mbappé", "Timo Werner", "Marcus Rashford", "Lionel Messi",
            "João Félix", "Lautaro Martínez", "Tammy Abraham", "Cristiano Ronaldo"]
season = '2019-2020'
chart = ChartMaker(players)
chart.expected_goals_assists(season)