from pprint import pprint
import gameplay
import webscraber

#enter game odds in this order
# gameOdds = [
# {'1X2': ['5.17', '4.42', '1.67'],
#   'Double Chance': ['2.20', '1.23', '1.19'],
#   'away': 'Man City', #61
#   'home': 'Newcastle',
#   'league': 'Premier League',
#   'time': '2024-01-13 18:30:00'},
#  {'1X2': ['1.37', '5.73', '8.84'],
#   'Double Chance': ['1.09', '1.16', '3.00'],
#   'away': 'US Salernitana', #65
#   'home': 'Napoli',
#   'league': 'Serie A',
#   'time': '2024-01-13 15:00:00'},
#  {'1X2': ['2.58', '3.47', '2.90'],
#   'Double Chance': ['1.43', '1.33', '1.52'],
#   'away': 'Villarreal', #62
#   'home': 'UD Las Palmas',
#   'league': 'LaLiga',
#   'time': '2024-01-13 14:00:00'},
#  {'1X2': ['6.78', '4.63', '1.52'],
#   'Double Chance': ['2.50', '1.21', '1.13'],
#   'away': 'Inter', #65
#   'home': 'AC Monza',
#   'league': 'Serie A',
#   'time': '2024-01-13 20:45:00'},
#  {'1X2': ['2.10', '3.49', '3.89'],
#   'Double Chance': ['1.28', '1.33', '1.74'],
#   'away': 'Real Sociedad', #64
#   'home': 'Athletic Bilbao',
#   'league': 'LaLiga',
#   'time': '2024-01-13 18:30:00'}
# ]
amount = 500
# get data from sportbet.com
data = webscraber.getDataFromApi()
date = '2024-01-14'
result = webscraber.searchDataByDate(data, date)
# pprint(result)
# analyse the selected games for a win win goal
gameplay.gameplays(result, amount)

