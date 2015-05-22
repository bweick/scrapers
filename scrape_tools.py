from bs4 import BeautifulSoup
import urllib
import pandas as pd
from pandas import DataFrame

def TableToFrame(table_soup, header):
    if not table_soup:
        return None
    else:
        rows = table_soup[0].findAll('tr')[1:]
        rows = [r for r in rows if not len(r.findAll('td')) > 29]
        if len(rows) == 0:
            d = {}
            return DataFrame(d)
        else:
            parsed_table = [[col.getText() for col in row.findAll('td')] for row in rows]
            return pd.io.parsers.TextParser(parsed_table, names = header, index_col = 0, parse_dates = True).get_chunk()

def urlsoup(url):
    file_pointer = urllib.urlopen(url)
    soup = BeautifulSoup (file_pointer)
    return soup

def jsondump(clean_player):    
    jsplayer_data = {}
    for player in clean_player:
        df = clean_player[player]
        jsdf = df.to_json()
        jsplayer_data.update({player:jsdf})
    return jsplayer_data
