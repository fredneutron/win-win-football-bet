import requests
from datetime import datetime, timezone, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def getDataFromApi():
    logger.info("Fetching data from SportyBet API")
    
    # set request details
    url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    payload = [{
        "sportId": "sr:sport:1",
        "marketId": "1,18,10,29,11,26,36,14",
        "tournamentId": [[
            "sr:tournament:8", "sr:tournament:17", "sr:tournament:19",
            "sr:tournament:23", "sr:tournament:34", "sr:tournament:35",
            "sr:tournament:54", "sr:tournament:329", "sr:tournament:182"
        ]]
    }]
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.33.0"
    }

    try:
        # Make API request
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        response_data = response.json()
        # Validate response structure
        if not isinstance(response_data, dict):
            raise ValueError("API response is not a dictionary")
            
        if 'data' not in response_data:
            raise KeyError("Response missing 'data' key")
            
        response = response_data['data']
        if not isinstance(response, list):
            raise ValueError("Response data is not a list")

        data = []
        # Process response data
        for league in response:
            if not isinstance(league, dict):
                logger.warning(f"Skipping invalid league data: {league}")
                continue
                
            league_name = league.get('name')
            events = league.get('events', [])

            if not league_name:
                logger.warning("Skipping league with no name")
                continue
            # rearrange response
            for event in events:
                try:
                    # Convert timestamp
                    timestamp = event.get("estimateStartTime", 0) / 1000   # Convert Unix timestamp milliseconds to seconds
                    utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)  # Create a datetime object in UTC
                    wat_datetime = utc_datetime + timedelta(hours=1)  # Add the West Africa Time (WAT) offset of UTC+1
                    formatted_wat_datetime = wat_datetime.strftime('%Y-%m-%d %H:%M:%S')   # Format the result
                    # Create event data object
                    data_object = {
                        'league': league_name,
                        'home': event.get('homeTeamName', 'Unknown'),
                        'away': event.get('awayTeamName', 'Unknown'),
                        'time': str(formatted_wat_datetime)
                    }
                    # Process markets
                    markets = event.get("markets", [])
                    market_limit = min(15, len(markets))
                    
                    for market in markets[:market_limit]:
                        market_name = market.get("name")
                        if market_name in ["1X2", "Double Chance"]:
                            outcomes = market.get("outcomes", [])
                            if len(outcomes) >= 3:
                                data_object[market_name] = [
                                    outcomes[0].get("odds"),
                                    outcomes[1].get("odds"),
                                    outcomes[2].get("odds")
                                ]
                    
                    data.append(data_object)
                except Exception as e:
                    logger.error(f"Error processing event: {e}")
                    continue
        
        logger.info(f"Successfully processed {len(data)} events")
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise

def searchDataByDate(date):
    data = getDataFromApi()
    result = [item for item in data if date in item['time']]
    logger.info(f"Found {len(result)} matches for date {date}")
    return result