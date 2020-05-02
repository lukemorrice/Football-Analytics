import requests
from bs4 import BeautifulSoup
import pandas as pd

 # player_name MUST be exact, i.e. include all hyphens and accents where required
def get_player_url_page(player_name):
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
def get_df_of_player_stats(player_name):
    # get the URL of player and create a BeautifulSoup object
    r = requests.get(get_player_url_page(player_name))
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table", id="stats_standard_ks_dom_lg")

    # convert to a pandas DataFrame
    df = pd.read_html(str(table))[0]

    # drop unnecessary rows and columns
    req_rows = len(list(table.find("tbody").find_all("tr")))
    df = df.iloc[:req_rows]
    df.drop(df.columns[[1, 3, 5, 28]], axis=1, inplace=True)

    # reformat the DataFrame's columns for multilevl indexing
    columns = [ ('Details', t2) for (t1, t2) in df.columns.values[:3] ] + list(df.columns.values[3:])
    df.columns = pd.MultiIndex.from_tuples(columns)

    df = df.set_index([("Details", "Season")])
    df.index.names = ['Season']

    return(df)