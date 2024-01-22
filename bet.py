from pprint import pprint
import gameplay
import sportybet

# enter game odds in this order
# gameOdds = [
# {'1X2': ['5.17', '4.42', '1.67'],
#   'Double Chance': ['2.20', '1.23', '1.19'],
#   'away': 'Man City', #61
#   'home': 'Newcastle',
#   'league': 'Premier League',
#   'time': '2024-01-13 18:30:00'},
#  {'1X2': ['2.10', '3.49', '3.89'],
#   'Double Chance': ['1.28', '1.33', '1.74'],
#   'away': 'Real Sociedad', #64
#   'home': 'Athletic Bilbao',
#   'league': 'LaLiga',
#   'time': '2024-01-13 18:30:00'}
# ]
# get data from sportbet.com
# data = sportybet.getDataFromApi()
date = '2024-01-22'
data = sportybet.searchDataByDate(date)
amount = float(input("\nPlease enter the amount for data analyse :    "))
# pprint(data)
# analyse the selected games for a win win goal
gameplay.gameplays(data, amount)

