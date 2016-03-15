

import requests
from bs4 import BeautifulSoup
import re
import csv


gamenumber=63328771

url = 'http://www.hotslogs.com/Player/MatchSummaryAjax?ReplayID=' + str(gamenumber)
#url = 'http://www.hotslogs.com/Player/MatchHistory?PlayerID=5434184'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html,"lxml")

#f1=open('./testfile', 'w+')

player=[];
table = soup.find('table', attrs={'class': 'rgMasterTable'})
#Find Player ID's
for a in table.find_all('a'):
    t= re.findall('(?<=Profile\?PlayerID\=)\d*',a['href'])
    if t:
        player.append(t[0])

print player
#Find Match Details

list_of_rows = []
ind=-1
for row in table.findAll('tr'):
    list_of_cells = []
    print 'newline'
    for cell in row.findAll('td'):
    	#Converts Soup format into text, converts to ascii, and remvoes nbsp
    	#Non-ascii characters will retain their identification
        text=cell.text.encode("ascii","xmlcharrefreplace").replace('&#160;','')
        
        list_of_cells.append(text)
    
    if len(list_of_cells)>2:
    	ind=ind+1
        del list_of_cells[5:12]
        del list_of_cells[2]
        list_of_cells[0]=player[ind]
        print list_of_cells
        list_of_rows.append(list_of_cells)
    #del list_of_cells[1]
outfile = open("./output.csv", "wb")
writer = csv.writer(outfile)
writer.writerows(list_of_rows)
#id="MatchSummary_h3MapName"
