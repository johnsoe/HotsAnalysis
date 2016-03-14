from lxml import html, cssselect
import requests
from profile import HeroStats, MapStats, EnemyHeroStats
from HotslogsIds import HotslogsIds

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
    allHeroStats = [];
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
    allMapStats = [];
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
    allEnemyStats = [];
    allEnemies = pageContent.get_element_by_id(HotslogsIds.enemyHeroesId).cssselect("tbody tr")
    for enemyElement in allEnemies:
        cols = enemyElement.cssselect("td")
        enemyStat = EnemyHeroStats(cols[1][0].text)
        enemyStat.gamesPlayed = cols[2].text
        enemyStat.winrate = cols[3].text[:-1]
        allEnemyStats.append(enemyStat)
    return allEnemyStats

# printPlayerStats("ralphstew_1376")
# printPlayerStats("schweik_1154")
# printPlayerStats("appleeater_1151")

# Update the number here to get a different player's profile
playerPage = getFullPageStats("5032724")
heroStatsList = getHeroesStats(playerPage)
print "Player heroes"
for hero in heroStatsList:
    print hero
print ""
print "Map Stats"
mapStatsList = getMapStats(playerPage)
for aMap in mapStatsList:
    print aMap
print ""
print "Opposing Heroes"
enemyHeroesStatsList = getWinratesAgainstHeroes(playerPage)
for enemy in enemyHeroesStatsList:
    print enemy
