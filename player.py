from web_scraper import get_df_of_player_stats

class Player(str):

    def __init__(self, player_name):
        self.name = player_name
        self.df = get_df_of_player_stats(player_name)
        self.league = self.get_league()
        
    def get_league(self):
        league = self.df['Details']['Comp'].iloc[-1]
        return league[3:]