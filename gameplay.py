
import math #import math libray

def gameplay(odds, amount, strict = False):

    # odds
    home = float(odds['1X2'][0])
    draw = float(odds['1X2'][1])
    away = float(odds['1X2'][2])
    home_or_draw = float(odds['Double Chance'][0])
    home_or_away = float(odds['Double Chance'][1])
    away_or_draw = float(odds['Double Chance'][2])
    print("\nGamePlay")
    print("\nBetting League: ", odds['league'])
    print("\nBetting Teams:   "+str(odds['home'])+" vs "+str(odds['away']))
    print("\nBetting amount:    N"+str(amount))
    print("\n"+str(odds['time']))
    print("\nChoosing the bet between Draw or any Team wins Probabilities and Straight Winning Probabilities.....")
    presentaion = "\n\nGame----------- Odds ----------Amount --------- Earning "
    winning_chance = 0
    print("\nStrict Mode is "+str(strict))
    print("\nNote: if strict mode is True, then only double chance gameplay will be analysed")

    if (strict):
        # team win or draw check
        print("\n\nTeam win or draw Probabilities")
        winning_chance = 100
        print('\n'+str(winning_chance)+'% chance of winning')
        # analyse
        holder = analysed(amount, home_or_draw, away_or_draw)
        home_or_draw_amount = holder[0]
        away_or_draw_amount = holder[1]

        print(presentaion)
        print("\nHome win or draw :   "+ str(home_or_draw) +"    *   "+ str(home_or_draw_amount) +"    =    "+ str(home_or_draw_amount * home_or_draw))
        print("\nAway win or draw :   "+ str(away_or_draw) +"    *   "+ str(away_or_draw_amount) +"    =    "+ str(away_or_draw_amount * away_or_draw))
        profitOrLoss(amount, home_or_draw_amount * home_or_draw, away_or_draw_amount * away_or_draw)
        
    elif (draw < home and draw < away):
        # any team win or draw check
        print("\n\nDraw or any Team wins Probabilities")
        winning_chance = 100
        print('\n'+str(winning_chance)+'% chance of winning')
        # analyse
        holder = analysed(amount, home_or_away, draw)
        home_or_away_amount = holder[0]
        draw_amount = holder[1]

        print(presentaion)
        print("\nDraw win :   "+ str(draw) +"    *   "+ str(draw_amount) +"    =    "+ str(draw_amount * draw))
        print("\nAny Team win :   "+ str(home_or_away) +"    *   "+ str(home_or_away_amount) +"    =    "+ str(home_or_away_amount * home_or_away))
        profitOrLoss(amount, draw_amount * draw, home_or_away_amount * home_or_away)

    else:
        # straight winning check
        print("\n\nStraight Winning Probabilities")
        winning_chance = 100 - int(100 * (draw / (draw + home + away)))
        print('\n'+str(winning_chance)+'% chance of winning')
        # analyse
        holder = analysed(amount,home, away)
        home_amount = holder[0]
        away_amount = holder[1]

        print(presentaion)
        print("\nHome win   :    "+ str(home) +"    *     "+ str(home_amount) +"     =    "+ str(home_amount * home))
        print("\nAway win   :    "+ str(away) +"    *     "+ str(away_amount) +"     =    "+ str(away_amount * away))
        profitOrLoss(amount, home_amount * home, away_amount * away)

def roundup(num):
    return int(math.ceil(num / 10.0) * 10)

def analysed(amount, upPercent, downPercent):
    total = upPercent + downPercent
    if (upPercent > downPercent):
        upPercentHolder = roundup(amount * (downPercent/total))
        downPercentHolder = amount - upPercentHolder
        return [upPercentHolder, downPercentHolder]
    else:
        downPercentHolder = roundup(amount * (upPercent/total))
        upPercentHolder = amount - downPercentHolder
        return [upPercentHolder, downPercentHolder]


def profitOrLoss(amount, upperMargin, lowerMargin):
    if (upperMargin < amount or lowerMargin < amount):
        print("\nThe risk is too high, this betting is a loss waiting to happen! \nPlease do not play")
    print("\n=====================================================================================\n\n")


def gameplays(games, amount,strict = False):
    print("\n=====================================================================================\n")
    for i in range(len(games)):
        amount = amount[i] if isinstance(amount, list) else int(amount)
        gameplay(games[i], amount, strict)