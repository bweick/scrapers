import scrape_tools
import json
from time import strftime 

def main():
    print 'Running Batter Home/Away Splits'
    stime = strftime("%Y-%m-%d %H:%M:%S")
    print stime
    
    filepath = '...\\Player Dictionaries\\MLB\\bat_HA.json'
    
    json_file = open('...\\Player Dictionaries\\MLB\\all_batters.json')
    json_str = json_file.read()
    batters = json.loads(json_str)
    json_file.close()
    
    years = [2012, 2013, 2014, 2015]
    bblink = 'http://www.baseball-reference.com/'
    
    for yr in years:
        filepath = '...Player Dictionaries\\MLB\\bat_HA_' + yr + '.json'        
        
        full_batters = {}
        for batter in batters:
            newlink = bblink + 'players/split.cgi?id=' + batters[batter] + '&year=' + yr + '&t=b'
            full_batters.update({batter:newlink})
            
        batstat = {}
        for name in full_batters:
            print name
            url = full_batters[name]
            soup = scrape_tools.urlsoup(url)
            
            stats = soup.findAll('table', id = 'hmvis')
            
            if not stats:
                None
            else:
                header = []
                for th in stats[0].findAll('th'):
                    if not th.getText() in header:
                        header.append(th.getText())
                
                reg = scrape_tools.TableToFrame(stats, header)
                reg = reg.reset_index(drop=True)
                if reg.empty:
                    None
                batstat.update({name:reg})
        
        clean_player = {}
        for key in batstat:
            df = batstat[key]
            df = df.reindex(columns = ['Split', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR',
                                       'RBI', 'SB', 'SO', 'BB', 'OBP', 'SLG', 'OPS', 'TB', 'BAbip', 'tOPS+'])
            df['aTB/PA'] = (df['BB'] + df['TB']) / df['PA']
            df['1B'] = df['H'] - df['2B'] - df['3B'] - df['HR']
            df['BIP'] = df['AB'] - df['SO'] - df['HR']
            df['1B%'] = df['1B']/df['BIP']
            df['2B%'] = df['2B']/df['BIP']
            df['3B%'] = df['3B']/df['BIP']
            clean_player.update({key:df})
            
        #convert dataframes into json and save as dictionary
        jsplayer_data = scrape_tools.jsondump(clean_player)
        
        with open(filepath, 'wb') as fp:
            json.dump(jsplayer_data, fp)
        fp.close()
    
    etime = strftime("%Y-%m-%d %H:%M:%S")
    print etime

if __name__ == '__main__':
    main()
