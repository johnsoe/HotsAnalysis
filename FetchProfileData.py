from lxml import html, cssselect
import requests
from profile import HeroStats, MapStats, EnemyHeroStats, Profile
from HotslogsIds import HotslogsIds
from pymongo import MongoClient

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
    return profile


#ssh -L 4321:localhost:27017 root@159.203.241.78 -f -N I have setup a local alias to hit the server
#need ssh key to work
client = MongoClient('localhost', 4321)
#default db- we would want to create our own but wouldn't do that here
db = client.hots;

# Normally this would be called after the match is parsed with all the match player profiles. 
matchProfiles = [5032724, 5434184, 5559464]

#TODO: check DB first to make sure we don't already have that data.
#profileData = [db.profiles.find({"hotslogsId": hotsId}) for hotsId in matchProfiles]
profiles = [fetchProfile(pId) for pId in matchProfiles]
profilesAsJSON = [profile.toJSON() for profile in profiles]
if profilesAsJSON:
    db.profiles.insert_many(profilesAsJSON)