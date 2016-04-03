from lxml import html, cssselect
import requests
from profile import HeroStats, MapStats, EnemyHeroStats, Profile
from HotslogsIds import HotslogsIds
from pymongo import MongoClient
from datetime import datetime
import threadtask

# print the MMR of the given player in all leagues
def printPlayerStats(player):
    response = requests.get('http://www.hotslogs.com/API/Players/1/' + player)
    print response.json()

# return full profile of requested player
def getFullPageStats(playerId):
    response = requests.get("http://www.hotslogs.com/Player/Profile?PlayerID=" + playerId)
    return html.fromstring(response.content)

# parse the given page for all player's hero statistics
def getHeroesStats(pageContent):
    allHeroStats = []
    allPlayedHeroes = pageContent.get_element_by_id(HotslogsIds.heroTableId).cssselect("tbody tr")
    for heroElement in allPlayedHeroes:
        cols = heroElement.cssselect("td")
        hero = HeroStats(cols[2][0].text)
        hero.level = cols[3].text
        hero.gamesPlayed = cols[4].text
        hero.winrate = cols[6].text[:-1]
        allHeroStats.append(hero)
    return allHeroStats

# parse the given page for all map statistics
def getMapStats(pageContent):
    allMapStats = []
    allMaps = pageContent.get_element_by_id(HotslogsIds.mapTableId).cssselect("tbody tr")
    for mapElement in allMaps:
        cols = mapElement.cssselect("td")
        mapStat = MapStats(cols[3].text)
        mapStat.gamesPlayed = cols[4].text
        mapStat.winrate = cols[6].text[:-1]
        allMapStats.append(mapStat)
    return allMapStats

# parse the given page for all opposing hero winrates
def getWinratesAgainstHeroes(pageContent):
    allEnemyStats = []
    allEnemies = pageContent.get_element_by_id(HotslogsIds.enemyHeroesId).cssselect("tbody tr")
    for enemyElement in allEnemies:
        cols = enemyElement.cssselect("td")
        enemyStat = EnemyHeroStats(cols[1][0].text)
        enemyStat.gamesPlayed = cols[2].text
        enemyStat.winrate = cols[3].text[:-1]
        allEnemyStats.append(enemyStat)
    return allEnemyStats

def fetchProfile (profileId):
    profile = Profile(str(profileId))
    playerPage = getFullPageStats(profile.hotslogsId)
    profile.heroes = getHeroesStats(playerPage)
    profile.maps = getMapStats(playerPage)
    profile.enemies = getWinratesAgainstHeroes(playerPage)
    return profile.toJSON()


def storeProfilesInDB (profileIds):

    #ssh -L 4321:localhost:27017 root@159.203.241.78 -f -N 
    #I have setup a local alias to hit the server
    #need ssh key to work
    client = MongoClient('localhost', 4321)
    #default db- we would want to create our own but wouldn't do that here
    db = client.hots;
    profiles = []
    def dbCheck (q):
        while True:
            item = q.get()
            if db.profiles.find({"hotslogsId": str(item)}).count() == 0:
                profiles.append(fetchProfile(item))
            q.task_done()

    print "Checking DB for ids " + str(datetime.now().time())
    threadtask.executeTask(dbCheck, profileIds)
    print "repeat profile count: " + str(len(profileIds) - len(profiles))

    print "Profiles Loaded " + str(datetime.now().time())
    if profiles and len(profiles) > 0:
        db.profiles.insert_many(profiles)
        print "Profiles stored remotely " + str(datetime.now().time())
