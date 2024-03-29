import random
import fractions
from player import Player
from constants import Constants
from event import Event, NoEvent


class Game:
    def __init__(self, players: list, *, intervention_rate: float = Constants.INTERVENTION_RATE):
        """
        A game where all the fun stuff happens
        :param players: list: A list of src.player.Player objects
        :param intervention_rate: float: The rate that an intervention will occur in a single turn.
                                         Default: Constants.INTERVENTION_RATE
        """

        self.players = players  # A simple list of players, not including any stats (see src.game.Game.stats)
        self.player_archive = self.players  # A list of players that is not changed, so we can do cool statistics stuff
        # and other things.
        self.intervention_rate = intervention_rate
        self.stats = {}  # Only accounting for this game
        self.manually_finished = False

        for player in self.players:
            self.stats[player.name] = {
                "total_kills": 0,  # total kills
                "successful_defenses": 0,  # amount of times this player survived an attack
                "attempted_attacks": 0,
                "attempted_defenses": 0,
                "attempted_interventions": 0,
                "kills_off_attacks": 0,  # amount of kills from attacks, also the amount of successful attacks
                "kills_off_defenses": 0,  # amount of kills from self-defense (defending)
                "kills_off_interventions": 0,  # amount of kills from interventions,
                "rounds_survived": 0,  # amount of rounds survived
                "alive": True,  # if the player is alive,
                "total_games": 0,
                "wins": 0
            }

    def can_run(self):
        """
        Checks if the game can still go on.

        :return: bool: True if the game can continue, and False otherwise
        """

        return len(self.players) > 1 and not self.manually_finished

    def eliminate_player(self, player: Player):
        """
        Eliminate a player and add to stats. Alternative to self.player.remove(player) and switching alive to False in
        self.stats
        :param player: src.player.Player: The player to eliminate
        :return: None
        """

        self.players = [_player for _player in self.players if _player.name != player.name]
        self.stats[player.name]["alive"] = False

    def eliminate_players(self, *players: Player):
        for player in players:
            self.eliminate_player(player)

    def update_stats(self, player: Player, stat_name: str, change: float = None, *, value=None):
        if change:
            self.stats[player.name][stat_name] += change
            player.stats[stat_name] += change
        elif value:
            self.stats[player.name][stat_name] = value
            player.stats[stat_name] = value

    def finish_game(self):
        """
        Serialize all stats and finish the game.

        :return: None
        """

        self.update_stats(self.players[0], "wins", 1)

        for player in self.player_archive:
            self.update_stats(player, "total_games", 1)
            player.serialize(file=player.json_file)

        self.manually_finished = True

    def rotate(self, offensive_player: Player = None, defensive_player: Player = None):
        """
        Rotate to the next "turn"

        :param offensive_player: src.player.Player: The offending (or attacking) player
        :param defensive_player: src.player.Player: The defending (or the attacked) player
        :return: dict: A dictionary with all the events that occurred during the turn.
            The case is an integer, which is like an exit code, that describes what happened.
            Positive is something involving the two parties, and negative is something involving more or none of them.
                -5: No one dies (with intervener)
                -4: Intervener gets killed by the offender and the defender
                -3: Intervener kills the offender (attacker)
                -2: Intervener kills the defender
                -1: Intervener kills everyone
                0: No one dies (nothing happened besides stat updates)
                1: The attacker eliminates the defender
                2: The defender eliminates the attacker
                3: Everyone is eliminated
        """

        # --- Choosing/checking the two parties involved ---

        if (offensive_player and defensive_player) and offensive_player == defensive_player:
            # Avoid weird scenarios by watching for self-attacks
            raise ValueError("Offensive player and defensive player cannot be the same.")

        # Generate offensive and defensive players if none are provided
        if offensive_player is None:
            offensive_player = random.choice(self.players)
        if defensive_player is None:
            defensive_player = random.choice(self.players)

            # Ensure we don't get self-battles
            while defensive_player == offensive_player:
                defensive_player = random.choice(self.players)

        # --- Actual battle logic ---

        if random.randint(1, Constants.EVENT_RATE.as_integer_ratio()[1]) == 1 and len(self.players) > 4:
            event = Event(self.players, random.random())
            event.choose_eliminated_players()

        # We ask for a random int between 1 and the second int in the ratio form of self.intervention_rate
        elif random.randint(1, self.intervention_rate.as_integer_ratio()[1]) == 1 and len(self.players) > 2:
            # Someone will intervene!
            event = None
            intervener = random.choice(self.players)

            # Ensure the intervener is not one of the parties already "in combat"
            while intervener in (offensive_player, defensive_player):
                intervener = random.choice(self.players)

            result_num = random.randint(1, 100)

            # Case -1: Intervener kills everyone
            if result_num <= 20 + intervener.intervention_score - \
                    ((offensive_player.defense + defensive_player.defense) / 2):

                # Update stats

                # Update attacker defense score
                offensive_player.defense -= round(random.uniform(0.05, 0.2), 2)
                # Update defensive defense score
                defensive_player.defense -= round(random.uniform(0.05, 0.2), 2)
                # Update intervener intervention score
                intervener.intervention_score += round(random.uniform(0.25, 0.75), 2)

                # Update stats
                self.update_stats(intervener, "total_kills", 2)
                self.update_stats(intervener, "attempted_interventions", 1)
                self.update_stats(intervener, "kills_off_interventions", 2)

                self.update_stats(offensive_player, "attempted_defenses", 1)
                self.update_stats(defensive_player, "attempted_defenses", 1)

                # Eliminate players
                self.eliminate_players(offensive_player, defensive_player)

                winner = intervener
                case = -1

            # Case -2: The intervener kills the defender
            elif result_num <= 40 + intervener.intervention_score - defensive_player.defense:

                # Update defender defense score
                defensive_player.defense -= round(random.uniform(0.05, 0.2), 2)
                # Update intervener intervention score
                intervener.intervention_score += round(random.uniform(0.25, 0.75), 2)

                # Update stats
                self.update_stats(intervener, "total_kills", 1)
                self.update_stats(intervener, "attempted_interventions", 1)
                self.update_stats(intervener, "kills_off_interventions", 1)

                self.update_stats(defensive_player, "attempted_defenses", 1)

                # Eliminate defender
                self.eliminate_player(defensive_player)

                winner = intervener
                case = -2

            # Case -3: The intervener kills the attacker
            elif result_num <= 60 + intervener.intervention_score - offensive_player.defense:
                # Update defender defense score
                offensive_player.defense -= round(random.uniform(0.05, 0.2), 2)
                # Update intervener intervention score
                intervener.intervention_score += round(random.uniform(0.25, 0.75), 2)

                # Update stats
                self.update_stats(intervener, "total_kills", 1)
                self.update_stats(intervener, "attempted_interventions", 1)
                self.update_stats(intervener, "kills_off_interventions", 1)

                self.update_stats(offensive_player, "attempted_defenses", 1)

                # Eliminate defender
                self.eliminate_player(offensive_player)

                winner = intervener
                case = -3

            # Case -4: The intervener gets killed by the offensive player and defensive player
            elif result_num <= 80 - intervener.intervention_score + \
                (offensive_player.defense + defensive_player.defense) / 2:

                # Update scores
                intervener.intervention_score -= round(random.uniform(0.05, 0.2), 2)
                offensive_player.defense += round(random.uniform(0.25, 0.75), 2)
                defensive_player.defense += round(random.uniform(0.25, 0.75), 2)

                # Update stats
                self.update_stats(intervener, "attempted_interventions", 1)

                self.update_stats(offensive_player, "successful_defenses", 1)
                self.update_stats(offensive_player, "attempted_defenses", 1)
                self.update_stats(offensive_player, "kills_off_defenses", 1)

                self.update_stats(defensive_player, "successful_defenses", 1)
                self.update_stats(defensive_player, "attempted_defenses", 1)
                self.update_stats(defensive_player, "kills_off_defenses", 1)

                self.eliminate_player(intervener)

                winner = (offensive_player, defensive_player)
                case = -4

            # Case -5: No one dies
            else:
                self.update_stats(offensive_player, "attempted_defenses", 1)
                self.update_stats(offensive_player, "successful_defenses", 1)

                self.update_stats(defensive_player, "attempted_defenses", 1)
                self.update_stats(defensive_player, "successful_defenses", 1)

                self.update_stats(intervener, "attempted_interventions", 1)

                winner = None
                case = -5

        else:
            event = None
            # No intervener this turn
            intervener = None

            # If the random int between 1 and 100 is less than 25 + attacker's attack score - defender's defend score,
            # than the attacker wins.
            result_num = random.randint(1, 100)

            # Case 1: the attacker wins and eliminates the defender
            if result_num <= 25 + offensive_player.offense - defensive_player.defense:
                # Eliminate the defensive player (aka defender or victim)
                self.eliminate_player(defensive_player)

                # Update stats
                self.update_stats(offensive_player, "total_kills", 1)
                self.update_stats(offensive_player, "attempted_attacks", 1)
                self.update_stats(offensive_player, "kills_off_attacks", 1)

                # Update attacker attack score
                offensive_player.offense += round(random.uniform(0.25, 0.75), 2)

                # Update defensive defense score
                defensive_player.defense -= round(random.uniform(0.05, 0.2), 2)

                winner = offensive_player
                case = 1

            # Case 2: the defender wins and eliminates the attacker
            elif result_num <= 50 - offensive_player.offense + defensive_player.defense:
                # Eliminate the offensive player (aka attacker)
                self.eliminate_player(offensive_player)

                # Update stats
                self.update_stats(defensive_player, "total_kills", 1)
                self.update_stats(defensive_player, "successful_defenses", 1)
                self.update_stats(defensive_player, "attempted_defenses", 1)
                self.update_stats(defensive_player, "kills_off_defenses", 1)

                # Update attacker attack score
                defensive_player.defense += round(random.uniform(0.25, 0.75), 2)

                # Update defensive defense score
                offensive_player.offense -= round(random.uniform(0.05, 0.2), 2)

                winner = defensive_player
                case = 2

            # Case 3: everyone dies
            elif result_num <= 75 and len(self.players) > 2:
                # Eliminate offensive and defensive players
                self.eliminate_player(offensive_player)
                self.eliminate_player(defensive_player)

                # Update stats
                self.update_stats(offensive_player, "attempted_attacks", 1)
                self.update_stats(defensive_player, "attempted_defenses", 1)

                # Update attacker offense score
                offensive_player.offense -= round(random.uniform(0.05, 0.2), 2)

                # Update defensive defense score
                defensive_player.defense -= round(random.uniform(0.05, 0.2), 2)

                winner = None
                case = 3

            # Case 0: no one dies (note we went back to 0)
            # This is also to ensure that something happens in this turn, instead of not fitting a condition and having
            # nothing happen
            else:
                # Update stats
                self.update_stats(offensive_player, "attempted_attacks", 1)
                self.update_stats(defensive_player, "attempted_defenses", 1)

                winner = None
                case = 0

        # Increase amount of rounds survived by 1
        for player in self.players:
            self.update_stats(player, "rounds_survived", 1)

        return {
            "attacker": offensive_player,
            "defender": defensive_player,
            "intervener": intervener,
            "case": case,
            "winner": winner,
            "event": event
        }
