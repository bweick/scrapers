import json
import string
import scrape_tools

bblink = 'http://www.baseball-reference.com/'
year = 'Career'
filepath = '...\\Player Dictionaries\\MLB\\namelinks.json'
filepath2 = '...\\Player Dictionaries\\MLB\\all_pitchers.json'
filepath3 = '...\\Player Dictionaries\\MLB\\all_batters.json'

#initialize dictionaries
names = {}
all_pitcher = {}
all_batter = {}

#cycle through player lists
for letter in string.ascii_lowercase:
    url = bblink + 'players/' + letter + '/'
    soup = scrape_tools.urlsoup(url)
    
    block = soup.findAll('blockquote')
    for n in block:
        athletes = n.findAll('b') #find bold players - bold denotes active
        for athlete in athletes:
            #grab links associated with each player
            name = str(athlete).split("<")[2]
            name = name.split(">")[1]
            print name
            link = str(athlete).split('"')[1]
            link = link.split("/")[3]
            link = link.split("shtm")[0]
            link = link[:-1]
            #go to player page to separate into pitcher or batter
            newsoup = scrape_tools.urlsoup('http://www.baseball-reference.com/players/gl.cgi?id=' + link +'&t=b&year=2014')
            span = newsoup.findAll('span', itemprop='role')
            if str(span[0].getText()) == 'Pitcher':
                all_pitcher.update({name:link})
            else:
                all_batter.update({name:link})
            names.update({name:link})
                
print len(names) #how many players you've found links for

#save all three dictionaries
with open(filepath, 'wb') as fp1:
    json.dump(names, fp1)
fp1.close()

with open(filepath2, 'wb') as fp2:
    json.dump(all_pitcher, fp2)
fp1.close()

with open(filepath3, 'wb') as fp3:
    json.dump(all_batter, fp3)
fp1.close()
