# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 18:27:05 2015

@author: Brian
"""
import json
import pandas as pd
from time import strftime 
import numpy as np
import scrape_tools

def main():
    print 'Running Ratio Batter'
    stime = strftime("%Y-%m-%d %H:%M:%S")
    print stime
    
    #open dict with batters only relevant for today
    json_file = open('C:\\Users\\Brian\\Documents\\Player Dictionaries\\MLB\\batters.json')
    json_str = json_file.read()
    batters = json.loads(json_str)
    json_file.close()
    
    filepath = 'C:\\Users\\Brian\\Documents\\Player Dictionaries\\MLB\\ratio_batter.json'
    bblink = 'http://www.baseball-reference.com/'
    
    #create link for each player
    full_batters = {}
    for batter in batters:
        letter = str(batters[batter][6])[0]
        newlink = bblink + 'players/' + letter + '/' + batters[batter][6] + '-bat.shtml'
        full_batters.update({batter:newlink})
    
    #create dataframe    
    batstat = {}
    for name in full_batters:
        print name
        url = full_batters[name]
        soup = scrape_tools.urlsoup(url)
        
        stats = soup.findAll('table', id = 'batting_ratio')
        
        if not stats:
            None
        else:
            header = []
            for th in stats[0].findAll('th'):
                if not th.getText() in header:
                    header.append(th.getText())
            
            header = filter(None, header)
            reg = scrape_tools.TableToFrame(stats, header)
            reg = reg.reset_index(drop=True)
            if reg.empty:
                None
        batstat.update({name:reg})

    #clean up dataframe
    clean_player = {}
    for key in batstat:
        print key
        df = batstat[key]
        df = df.reindex(columns = ['Year', 'Tm', 'PA', 'HR%', 'SO%', 'BB%', 'XBH%', 'X/H%', 'SO/W', 'AB/SO',
                                   'AB/HR', 'AB/RBI', 'GB/FB', 'GO/AO', 'IP%', 'LD%', 'HR/FB', 'IF/FB'])
#        if key == 'Torii Hunter':
#            df = df[:-3]
#        df = df[:-2]
        df = df[np.isnan(df['AB/HR']) == False]
        df['GB/FB'] = df['GB/FB'].astype(float)
        df['LD%'] = pd.Series([(float(str(l)[:-1]))/100 for l in df['LD%']], index = df.index)
        df['HR/FB'] = pd.Series([(float(str(l)[:-1]))/100 for l in df['HR/FB']], index = df.index)
        df['IP%'] = pd.Series([(float(str(l)[:-1]))/100 for l in df['IP%']], index = df.index)
        df['IF/FB'] = pd.Series([(float(str(l)[:-1]))/100 for l in df['IF/FB']], index = df.index)
        df['GB%'] = df['GB/FB']/(1 + df['GB/FB'])
        df['FB%'] = 1 - df['GB%'] - df['LD%']
        clean_player.update({key:df})
   
    #convert dataframes into json and save as dictionary
    jsplayer_data = scrape_tools.jsondump(clean_player)
    
    with open(filepath, 'wb') as fp:
        json.dump(jsplayer_data, fp)
    fp.close()
    
    return clean_player
    etime = strftime("%Y-%m-%d %H:%M:%S")
    print etime
if __name__ == "__main__":
    main()
    