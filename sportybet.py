import requests
from datetime import datetime, timezone, timedelta


def getDataFromApi():
    print("\n\nSportyBet.com\n")
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
                    "sr:tournament:54",
                    "sr:tournament:329",
                    "sr:tournament:182"
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
    data = []
    # rearrange response
    for i in range(len(response)):
        leagueName = response[i]['name']
        leagueEvents = response[i]['events']
        for j in range(len(leagueEvents)):
            leagueEvent = leagueEvents[j]
            leagueMarkets = leagueEvent["markets"]
            # Convert Unix timestamp milliseconds to seconds
            timestamp = leagueEvent["estimateStartTime"] / 1000
            # Create a datetime object in UTC
            utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
            # Add the West Africa Time (WAT) offset of UTC+1
            wat_offset = timedelta(hours=1)
            wat_datetime = utc_datetime + wat_offset
            # Format the result
            formatted_wat_datetime = wat_datetime.strftime('%Y-%m-%d %H:%M:%S')
            # create a data object for the data
            dataObject = {
                'league': leagueName,
                'home': leagueEvent['homeTeamName'],
                'away': leagueEvent['awayTeamName'],
                'time' : str(formatted_wat_datetime)
            }
            # set odds
            l = len(leagueMarkets)
            l =  15 if 15 < l else l
            for x in range(l):
                leagueMarket = leagueMarkets[x]
                if (leagueMarket["name"] == "1X2" or leagueMarket["name"] == "Double Chance"):
                    # add odds to the data object
                    dataObject.update({ leagueMarket["name"] : [
                        leagueMarket["outcomes"][0]["odds"],
                        leagueMarket["outcomes"][1]["odds"],
                        leagueMarket["outcomes"][2]["odds"]
                    ]})
            # add data object to the container array
            data.append(dataObject)
    
    return data


def searchDataByDate(date):
    data = getDataFromApi()
    result = []
    for i in range(len(data)):
        # search for the input date
        if (date in data[i]['time']):
            result.append(data[i])
    print("\n\nData length is "+ str(len(result)))
    return result