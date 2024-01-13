import requests
from datetime import datetime, timezone, timedelta


def getDataFromApi():
    # set request details
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = [
        {
            "sportId": "sr:sport:1",
            "marketId": "1,18,10,29,11,26,36,14",
            "tournamentId": [
                [
                    "sr:tournament:8",
                    "sr:tournament:17",
                    "sr:tournament:19",
                    "sr:tournament:23",
                    "sr:tournament:34",
                    "sr:tournament:35",
                    "sr:tournament:54"
                ]
            ]
        }
    ]
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.33.0"
    }
    # requests
    response = requests.post(url, json = payload, headers=headers)
    response = response.json()['data']
    data = {}
    # rearrange response
    for i in range(len(response)):
        leagueName = response[i]['name']
        leagueEvents = response[i]['events']
        # add leagueName key to data dictionary
        data.update({leagueName : []})
        for j in range(len(leagueEvents)):
            leagueEvent = leagueEvents[j]
            leagueMarkets = leagueEvent["markets"]
            # create empty shell for event data
            # new
            data[leagueName].append({
                'home': leagueEvent['homeTeamName'],
                'away': leagueEvent['awayTeamName']
            })
            # old
            # data[leagueName].append([])

            # data[leagueName][j].append([
            #     leagueEvent['homeTeamName'],
            #     leagueEvent['awayTeamName']
            # ])
            # Convert Unix timestamp milliseconds to seconds
            timestamp = leagueEvent["estimateStartTime"] / 1000
            # Create a datetime object in UTC
            utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
            # Add the West Africa Time (WAT) offset of UTC+1
            wat_offset = timedelta(hours=1)
            wat_datetime = utc_datetime + wat_offset
            # Format the result
            formatted_wat_datetime = wat_datetime.strftime('%Y-%m-%d %H:%M:%S')
            # add formated time to new array
            # new
            data[leagueName][j].update({ 'time' : str(formatted_wat_datetime) })
            # old
            # data[leagueName][j].append([
            #     'time: '+str(formatted_wat_datetime)
            # ])
            # set odds
            l = len(leagueMarkets)
            l =  15 if 15 < l else l
            for x in range(l):
                leagueMarket = leagueMarkets[x]
                if (leagueMarket["name"] == "1X2" or leagueMarket["name"] == "Double Chance"):
                    data[leagueName][j].update({ leagueMarket["name"] : [
                        leagueMarket["outcomes"][0]["odds"],
                        leagueMarket["outcomes"][1]["odds"],
                        leagueMarket["outcomes"][2]["odds"]
                    ]})
    
    return data


def searchDataByDate(data, date):
    # get the properties keys in the dictionary
    # propertyKeys = data
    result = []
    for i, k in data.items():
        # get league name
        league = i
        # get league array of data
        namedObject = k
        for j in range(len(namedObject)):
            # search for the input date
            if (date in namedObject[j]['time']):
                n = namedObject[j]
                n.update({ 'league' : league })
                result.append(n)
    print("data length is "+ len(result))
    return result