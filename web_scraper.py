import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml.html as lh
from tabulate import tabulate

class WebScraper():

    # player_name MUST be exact, i.e. include all hyphens and accents where required
    def get_player_url_page(self, player_name):
        # converts to the form: forename-surname
        formatted_name = player_name.split(' ')[0] + '-' + player_name.split(' ')[1]
        base_url = "https://fbref.com"
        search_extension = base_url + "/en/search/search.fcgi?search="
        r = requests.get(search_extension + formatted_name)
        soup = BeautifulSoup(r.content, "html.parser")

        # After we have queried the webpage, we have two possible results:
        # 1. We go directly to the player's webpage e.g. "Lionel Messi"
        # 2. We go to a page of search results e.g. "Gabriel Jesus"

        # 1. Check if we are looking at search results
        if not soup.find('h1', text=player_name):
            player_link = soup.find('a', text=player_name)
            page = base_url + player_link['href']
            return(page)
        # 2. Otherwise, we have been directly transferred to the player's stats page
        else:
            return(r.url)

    # Returns a multiindex column of statistics for a given player
    def get_df_of_player_stats(self, player_name):
        r = requests.get(self.get_player_url_page(player_name))
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table", id="stats_standard_ks_dom_lg")
        req_rows = len(list(table.find("tbody").find_all("tr")))
        df = pd.read_html(str(table))[0]
        row_count = df.shape[0]
        df.drop(df.columns[[1, 3, 5, 28]], axis=1, inplace=True)
        drop_count = row_count - req_rows
        df = df.iloc[:drop_count-1]
        columns = [ ('Details', t2) for (t1, t2) in df.columns.values[:3] ] + list(df.columns.values[3:])
        df.columns = pd.MultiIndex.from_tuples(columns)
        return(df)