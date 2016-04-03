from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import csv
import fetchprofile
import threading
import threadtask

outfile = open("./outputA.csv", "a")
writer = csv.writer(outfile)
unique_player_ids = []
match_ids = range(68703332, 68708332)
csv_write_lock = threading.Lock()
print "Starting game load " + str(datetime.now().time())

def parse_match(q):
    while True:
        url = 'http://www.hotslogs.com/Player/MatchSummaryAjax?ReplayID=' + str(q.get())
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html,"lxml")

        player=[];
        map_name = soup.find('h3', attrs={'id': "MatchSummary_h3MapName"}).text
        table = soup.find('table', attrs={'class': 'rgMasterTable'})
        
        #Sometimes there is no html on page
        if not table:
            q.task_done()
            continue

        #Find Player ID's    
        for a in table.find_all('a'):
            t = re.findall('(?<=Profile\?PlayerID\=)\d*',a['href'])
            if t and t[0]:
                player.append(t[0])

        #Make sure there are ten players with profiles in the game, otherwise ignore game
        if len(player) != 10:
            q.task_done()
            continue
        else:
            for player_id in player:
                if player_id not in unique_player_ids:
                    unique_player_ids.append(player_id)

        #Find Match Details
        list_of_rows = [map_name]
        ind=-1
        for row in table.findAll('tr'):
            list_of_cells = []
            for cell in row.findAll('td')[:-1]:
                #Converts Soup format into text, converts to ascii, and remvoes nbsp
                #Non-ascii characters will retain their identification
                text=cell.text.encode("ascii","xmlcharrefreplace").replace('&#160;','')
                list_of_cells.append(text)
            
            if len(list_of_cells)>2:
                ind=ind+1
                del list_of_cells[5:12]
                del list_of_cells[2]
                list_of_cells[0]=player[ind]
                for i in range(0, len(list_of_cells)):
                    list_of_rows.append(list_of_cells[i])
        with csv_write_lock:
            writer.writerow(list_of_rows)
        q.task_done()

threadtask.execute_task(parse_match, match_ids)
outfile.close()
print "Ending game load " + str(datetime.now().time())
fetchprofile.store_profiles_in_db(unique_player_ids)
