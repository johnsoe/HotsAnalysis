# HotsAnalysis
A simple repo to scrape HotsLogs for data and try to predict who will win a match

### Using Python 2.7.11
Required Python modules - requests, lxml, cssselect, BeautifulSoup, pymongo

### Verify it is working
open a new mongodb connection locally from command line by running - 'mongod'
Then from a separate console, run 'mongo'
This will connect to your local instance you opened and will allow you to interact
db.profiles.findOne() should return a single profile after running FetchProfileData
db.profiles.count() should be 3. 