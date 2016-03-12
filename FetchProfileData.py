from lxml import html
import requests

def printPlayerStats(player):
    response = requests.get('http://www.hotslogs.com/API/Players/1/' + player)
    print response.json()

def getFullPageStats(playerId):
    response = requests.get("http://www.hotslogs.com/Player/Profile?PlayerID=" + playerId);
    return html.fromstring(response.content)

def getHeroStats(pageContent):
    pass
    #TODO parse the page to find winrates, lvl, games played etc.

def getMapStats(pageContent):
    pass
    #TODO parse the page to find all map winrates and games played

def getWinratesAgainstHeroes(pageContent):
    pass
    #TODO parse the page to find winrates against other heroes


printPlayerStats("ralphstew_1376")
printPlayerStats("schweik_1154")
#printPlayerStats("appleeater") Need battletag
