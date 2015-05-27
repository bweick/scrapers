import json
from time import strftime
import scrape_tools

def exceptions(name):
    if name == 'John Ryan Murphy':
        new = 'J.R. Murphy'
    elif name == 'Steven Geltz':
        new = 'Steve Geltz'
    elif name == 'Nathan Karns':
        new = 'Nate Karns'
    elif name == 'Steven Tolleson':
        new = 'Steve Tolleson'
    elif name == 'Phil Gosselin':
        new = 'Philip Gosselin'
    elif name == 'Eric Young Jr.':
        new = 'Eric Young'
    elif name == 'Michael Morse':
        new = 'Mike Morse'
    elif name == 'Jonathon Niese':
        new = 'Jon Niese'
    elif name == 'John Mayberry Jr.':
        new = 'John Mayberry'
    elif name == 'Kris Negron':
        new = 'Kristopher Negron'
    elif name == 'Samuel Deduno':
        new = 'Sam Deduno'
    elif name == 'Matt Joyce':
        new = 'Matthew Joyce'
    elif name == 'Delino DeShields Jr.':
        new = 'Delino DeShields'
    else:
        new = name
    return new

stime = strftime("%Y-%m-%d %H:%M:%S")
print stime

#set espn link and filepath to save dict
espnlink = 'http://scores.espn.go.com/mlb/teams'
filepath = '...\\Player Dictionaries\\MLB\\baseball_attrib.json'

#open dict with names and individ bballref links - from baseball_player_info
json_file = open('...\\Player Dictionaries\\MLB\\namelinks.json')
json_str = json_file.read()
names = json.loads(json_str)
json_file.close()

#get links for each team's page on espn
soup = scrape_tools.urlsoup(espnlink)
rosterlink = []
for h in soup.findAll('h5'):
    front = str(h)[:52]
    front = front.split('"')[3]
    back = str(h)[52:]
    back = back.split('"')[0]
    link = front + 'roster/' + back
    rosterlink.append(link)

info_dict = {}
for link in rosterlink:
    soupy = scrape_tools.urlsoup(link)
    tabs = soupy.findAll('table')
    for tr in tabs[0].findAll('tr')[:39]:
        row = [td.getText() for td in tr.findAll('td')]
        if len(row) < 4 or row[1] == u'NAME':
            row = []
        else:
            name = row[1] # get player name
            team = link.split('/')[8] #get player's team
            if names.get(name) == None: # check if espn player name matches with bbref
                newname = exceptions(name) #pass to manually coded exceptions
                if names.get(newname) == None: # if not in exceptions print name so it can be manually added
                    print name
                else:
                    blink = names[newname] #get bbref link
            else:
                blink = names[name] #get bbref link
            row.append(team.upper()) #add team name to player info
            row.append(blink) # add bbref link to player info
            info_dict.update({name:row})

# place for extra exceptions that get through first exception loop
info_dict['Norichika Aoki'] = info_dict['Nori Aoki']
del info_dict['Nori Aoki']

#save dictionary of player attributes
with open(filepath, 'wb') as fp:
    json.dump(info_dict, fp)
fp.close()

etime = strftime("%Y-%m-%d %H:%M:%S")
