from pprint import pprint
import gameplay
import sportybet
import sporty
import game

# enter game odds in this order
# gameOdds = [
#     {
#         '1X2': [2.5, 3.2, 2.8],
#         'Double Chance': [1.4, 1.3, 1.5],
#         'league': 'Premier League',
#         'home': 'Team A',
#         'away': 'Team B',
#         'time': '2024-10-26 15:00:00'
#     },
# ]
# get data from sportbet.com
# data = sportybet.getDataFromApi()
# data = sporty.getDataFromApi()
date = '2024-10-26'
# data = sportybet.searchDataByDate(date)
data = sporty.searchDataByDate(date)
amount = float(input("\nPlease enter the amount for data analyse :    "))
# pprint(data)
# analyse the selected games for a win win goal
# gameplay.gameplays(data, amount)
game.analyze_multiple_games(data, amount)

