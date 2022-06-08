import random
import fractions
from player import Player
from constants import Constants


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
                "alive": True  # if the player is alive
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

        for player in self.player_archive:
            player.serialize(file=player.json_file)

        self.manually_finished = True

    def rotate(self, offensive_player: Player = None, defensive_player: Player = None):
        """
        Rotate to the next "turn"

        :param offensive_player: src.player.Player: The offending (or attacking) player
        :param defensive_player: src.player.Player: The defending (or the attacked) player
        :return: dict: A dictionary with all the events that occurred during the turn.
            The case is an integer, which is like an exit code, that describes what happened.
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

        # We ask for a random int between 1 and the second int in the ratio form of self.intervention_rate
        if random.randint(1, self.intervention_rate.as_integer_ratio()[1]) == 1:
            # Someone will intervene!
            intervener = random.choice(self.players)

            # Ensure the intervener is not one of the parties already "in combat"
            while intervener not in (offensive_player, defensive_player):
                intervener = random.choice(self.players)
        else:
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
            "winner": winner
        }
