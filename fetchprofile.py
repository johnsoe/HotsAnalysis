from lxml import html, cssselect
from profile import HeroStats, MapStats, EnemyHeroStats, Profile
from hotslogsids import HotslogsIds
from pymongo import MongoClient
from datetime import datetime
import requests
import threadtask

# print the MMR of the given player in all leagues
def print_player_stats(player):
    response = requests.get('http://www.hotslogs.com/API/Players/1/' + player)
    print response.json()

# return full profile of requested player
def get_full_page_stats(playerId):
    response = requests.get("http://www.hotslogs.com/Player/Profile?PlayerID=" + playerId)
    return html.fromstring(response.content)

# parse the given page for all player's hero statistics
def get_heroes_stats(pageContent):
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
def get_map_stats(pageContent):
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
def get_winrates_against_heroes(pageContent):
    allEnemyStats = []
    allEnemies = pageContent.get_element_by_id(HotslogsIds.enemyHeroesId).cssselect("tbody tr")
    for enemyElement in allEnemies:
        cols = enemyElement.cssselect("td")
        enemyStat = EnemyHeroStats(cols[1][0].text)
        enemyStat.gamesPlayed = cols[2].text
        enemyStat.winrate = cols[3].text[:-1]
        allEnemyStats.append(enemyStat)
    return allEnemyStats

def fetch_profile (profileId):
    profile = Profile(str(profileId))
    playerPage = get_full_page_stats(profile.hotslogsId)
    profile.heroes = get_heroes_stats(playerPage)
    profile.maps = get_map_stats(playerPage)
    profile.enemies = get_winrates_against_heroes(playerPage)
    return profile.toJSON()


def store_profiles_in_db (profile_ids):
    client = MongoClient('localhost', 4321)
    db = client.hots;
    profiles = []
    def db_check (q):
        while True:
            item = q.get()
            if db.profiles.find({"hotslogsId": str(item)}).count() == 0:
                profiles.append(fetch_profile(item))
            q.task_done()

    print "Checking DB for ids and getting profiles " + str(datetime.now().time())
    threadtask.execute_task(db_check, profile_ids)
    print "repeat profile count: " + str(len(profile_ids) - len(profiles))

    print "Profiles Loaded " + str(datetime.now().time())
    if profiles and len(profiles) > 0:
        db.profiles.insert_many(profiles)
        print "Profiles stored remotely " + str(datetime.now().time())
