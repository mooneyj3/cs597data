import requests, json, csv
from bs4 import BeautifulSoup
from collections import defaultdict
UpperBound = 9
outputFormat = "json"
outFile = "../cs597data/PlayerData." + outputFormat

data = defaultdict(dict)

def addRowToDictionary(row, week):
    firstCol = row.find('td', {'class': 'playertablePlayerName'})
    lastCol = row.find('td', {'class': 'appliedPoints'})
    playerId = row.get('id')
    name = firstCol.find('a').text
    firstCol.a.decompose()
    contents = firstCol.text.replace(',', '').replace('*','').split()
    
    if 'D/ST' in name:
        team = name.replace('D/ST','').strip()
        position = 'D/ST'
    else:
        team = contents[0]
        position = contents[1]
    
    projectedPoints = lastCol.text
    
    if name not in data:
        data[name] = {
            'Id' : playerId,
            'Team' : team,
            'Posistion' : position,
            'Weeks' : []
        }
    Weekdata = {
        'Week' : week,
        'ProjectedPoints' : projectedPoints
    }
    data[name]['Weeks'].append(Weekdata)
    

def addPointsToDictionary(row, week):
    firstCol = row.find('td', {'class': 'playertablePlayerName'})
    lastCol = row.find('td', {'class': 'appliedPoints'})
    name = firstCol.find('a').text
    scoredPoints = lastCol.text
    data[name]['Weeks'][week - 1]["AppliedPoints"] = scoredPoints

def findProjectionData(uri, week):
    response = requests.get(uri)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'playerTableTable tableBody', 'id': 'playertable_0'})
    rows = table.find_all('tr', {'class': 'pncPlayerRow'})
    for child in rows:
        addRowToDictionary(child, week)

    navigationHeader = soup.find('div', {'class': 'paginationNav'})
    links = navigationHeader.find_all('a')

    for link in links:
        if 'NEXT' in link.text:
            nextLink = link['href']
            findProjectionData(nextLink, week)
    
def findFantasyPointsData(uri, week):
    response = requests.get(uri)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', {'class' : 'playerTableTable'})
    for table in tables:
        rows = table.find_all('tr', {'class': 'pncPlayerRow'})
        for row in rows:
            addPointsToDictionary(row, week)

    navigationHeader = soup.find('div', {'class': 'paginationNav'})
    links = navigationHeader.find_all('a')

    for link in links:
        if 'NEXT' in link.text.upper():
            nextLink = link['href']
            findFantasyPointsData(nextLink, week)

def CalculatePercentError(week):
    weekIndex = week - 1
    for key in data:
        AppliedPoints = data[key]['Weeks'][weekIndex]["AppliedPoints"]
        ProjectedPoints = data[key]['Weeks'][weekIndex]["ProjectedPoints"]
        if AppliedPoints != "0" and AppliedPoints != "--" and ProjectedPoints != "--":
            PercentError = abs((float(ProjectedPoints)-float(AppliedPoints))/float(AppliedPoints))*100
        else:
            PercentError = "--"
        data[key]['Weeks'][weekIndex]["PercentError"] = PercentError
        
def CalculateRunningPercentError(week):
    weekIndex = week - 1
    for key in data:
        RunningError = 0.0
        Count = 0
        for i in range(week):
            PercentError = data[key]['Weeks'][i]["PercentError"]
            if(PercentError != "--"):
                RunningError += float(PercentError)
                Count += 1
        if(Count != 0):
            data[key]['Weeks'][weekIndex]["RunningError"] = RunningError/Count
        else:
            data[key]['Weeks'][weekIndex]["RunningError"] = "--"

for i in range(1, UpperBound):
    currentWeek = i
    print("Collecting week " + str(currentWeek) + " projections...")
    findProjectionData("http://games.espn.com/ffl/tools/projections?&scoringPeriodId=" + str(i) + "&seasonId=2018", currentWeek)
    print("Collecting week " + str(currentWeek) + " points...")
    findFantasyPointsData("http://games.espn.com/ffl/leaders?&scoringPeriodId=" + str(i) + "&seasonId=2018", currentWeek)
    print("Calculating Percent Error")
    CalculatePercentError(currentWeek)
    print("Calculating RunningPercent Error")
    CalculateRunningPercentError(currentWeek)

with open(outFile, 'w') as outFile:
    json.dump(data, outFile)