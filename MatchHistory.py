import requests
from BeautifulSoup import BeautifulSoup
import csv


url = 'http://www.hotslogs.com/Player/MatchHistory?PlayerID=5434184'
response = requests.get(url)
html = response.content
#print html
#soup = BeautifulSoup(html)
#print soup.prettify()

soup = BeautifulSoup(html)
#table = soup.find('table', attrs={'id': 'DataTables_Table_0'})
table = soup.find('table', attrs={'class': 'rgMasterTable'})
#print table.prettify()
list_of_rows = []

for row in table.findAll('tr'):
    list_of_cells = []
    #print row.prettify()
    for cell in row.findAll('td'):
        #print cell.text.replace('<td style="display:none;">', '')
        cell2=cell.text.replace('</td>', '')
        text = cell2.replace('&nbsp;','')
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)
        #cell=cell.text.replace('&nbsp;','')
    	#print "row"
        #print cell.prettify()
        #print cell.text
print list_of_rows
#print '<td style="display:none;">'

outfile = open("./output.csv", "wb")
writer = csv.writer(outfile)
writer.writerows(list_of_rows)

