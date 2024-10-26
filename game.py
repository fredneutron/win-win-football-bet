from typing import Dict, Union, List, Tuple
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BettingOdds:
    """Data class to store and validate betting odds"""
    home: float
    draw: float
    away: float
    home_or_draw: float
    home_or_away: float
    away_or_draw: float
    league: str
    home_team: str
    away_team: str
    time: str

    @classmethod
    def from_dict(cls, odds_dict: Dict) -> 'BettingOdds':
        """Create BettingOdds instance from dictionary"""
        try:
            return cls(
                home=float(odds_dict['1X2'][0]),
                draw=float(odds_dict['1X2'][1]),
                away=float(odds_dict['1X2'][2]),
                home_or_draw=float(odds_dict['Double Chance'][0]),
                home_or_away=float(odds_dict['Double Chance'][1]),
                away_or_draw=float(odds_dict['Double Chance'][2]),
                league=str(odds_dict['league']),
                home_team=str(odds_dict['home']),
                away_team=str(odds_dict['away']),
                time=str(odds_dict['time'])
            )
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error creating BettingOdds: {e}")
            raise ValueError(f"Invalid odds dictionary format: {e}")

@dataclass
class BettingResult:
    """Data class to store betting analysis results"""
    winning_chance: float
    first_bet: Tuple[str, float, float, float]  # (name, odds, amount, potential_earning)
    second_bet: Tuple[str, float, float, float]
    is_profitable: bool
    total_amount: float

    def format_output(self) -> str:
        """Format betting results for display"""
        output = [
            "\nGamePlay Analysis",
            "-" * 50,
            f"Winning Chance: {self.winning_chance:.1f}%",
            "\nBet Details:",
            f"{self.first_bet[0]:<15} {self.first_bet[1]:>6.2f} * {self.first_bet[2]:>8.2f} = {self.first_bet[3]:>10.2f}",
            f"{self.second_bet[0]:<15} {self.second_bet[1]:>6.2f} * {self.second_bet[2]:>8.2f} = {self.second_bet[3]:>10.2f}",
            "-" * 50,
            f"{'Recommendation:':<15} {'PROFITABLE' if self.is_profitable else 'NOT RECOMMENDED'}",
            "=" * 50
        ]
        return "\n".join(output)

def round_up_to_10(amount: float) -> int:
    """Round up to nearest 10"""
    return int(Decimal(str(amount)).quantize(Decimal('10'), rounding=ROUND_CEILING))

def calculate_bet_distribution(amount: float, odds1: float, odds2: float) -> Tuple[float, float]:
    """Calculate optimal bet distribution between two odds"""
    total_odds = odds1 + odds2
    if odds1 > odds2:
        bet1 = round_up_to_10(amount * (odds2 / total_odds))
        bet2 = amount - bet1
    else:
        bet2 = round_up_to_10(amount * (odds1 / total_odds))
        bet1 = amount - bet2
    return bet1, bet2

def analyze_gameplay(odds: Dict, amount: float, strict: bool = False) -> BettingResult:
    """Analyze betting options and return optimal strategy"""
    try:
        betting_odds = BettingOdds.from_dict(odds)
        # Log basic game information
        logger.info(f"Analyzing {betting_odds.home_team} vs {betting_odds.away_team}")
        logger.info(f"League: {betting_odds.league}, Time: {betting_odds.time}")

        if strict:
            # Double chance analysis
            bet1_amount, bet2_amount = calculate_bet_distribution(amount, betting_odds.home_or_draw, betting_odds.away_or_draw)
            result = BettingResult(
                winning_chance=100.0,
                first_bet=("Home/Draw", betting_odds.home_or_draw, bet1_amount, 
                          bet1_amount * betting_odds.home_or_draw),
                second_bet=("Away/Draw", betting_odds.away_or_draw, bet2_amount, 
                          bet2_amount * betting_odds.away_or_draw),
                is_profitable=True,
                total_amount=amount
            )
        elif betting_odds.draw < betting_odds.home and betting_odds.draw < betting_odds.away:
            # Draw or any team analysis
            bet1_amount, bet2_amount = calculate_bet_distribution(amount, betting_odds.home_or_away, betting_odds.draw)
            result = BettingResult(
                winning_chance=100.0,
                first_bet=("Any Team", betting_odds.home_or_away, bet1_amount, 
                          bet1_amount * betting_odds.home_or_away),
                second_bet=("Draw", betting_odds.draw, bet2_amount, 
                          bet2_amount * betting_odds.draw),
                is_profitable=True,
                total_amount=amount
            )
        else:
            # Straight winning analysis
            bet1_amount, bet2_amount = calculate_bet_distribution(amount, betting_odds.home, betting_odds.away)
            winning_chance = 100 - int(100 * (betting_odds.draw / (betting_odds.draw + betting_odds.home + betting_odds.away)))
            result = BettingResult(
                winning_chance=winning_chance,
                first_bet=("Home", betting_odds.home, bet1_amount, 
                          bet1_amount * betting_odds.home),
                second_bet=("Away", betting_odds.away, bet2_amount, 
                          bet2_amount * betting_odds.away),
                is_profitable=True,
                total_amount=amount
            )

        # Check profitability
        result.is_profitable = (result.first_bet[3] >= amount and result.second_bet[3] >= amount)
        
        return result
    except Exception as e:
        logger.error(f"Error in analyze_gameplay: {e}")
        raise

def analyze_multiple_games(games: List[Dict], amounts: Union[List[float], float], strict: bool = False) -> List[BettingResult]:
    """Analyze multiple games with corresponding amounts"""
    try:
        results = []
        for i, game in enumerate(games):
            amount = amounts[i] if isinstance(amounts, list) else float(amounts)
            result = analyze_gameplay(game, amount, strict)
            results.append(result)
            print(result.format_output())
        return results
    
    except Exception as e:
        logger.error(f"Error in analyze_multiple_games: {e}")
        raise