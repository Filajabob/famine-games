import random
import fractions
from player import Player
from constants import Constants

class Game:
    def __init__(self, players: list, *, intervention_rate: float=Constants.INTERVENTION_RATE):
        """
        A game where all the fun stuff happens
        :param players: list: A list of src.player.Player objects
        :param intervention_rate: float: The rate that an intervention will occur in a single turn.
                                         Default: Constants.INTERVENTION_RATE
        """

        self.players = players
        self.intervention_rate = intervention_rate

    def rotate(self, offensive_player: Player=None, defensive_player: Player=None):
        """
        Rotate to the next "turn"
        :param offensive_player: src.player.Player: The offending (or attacking) player
        :param defensive_player: src.player.Player: The defending (or the attacked) player
        :return:
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
            while defensive_player != offensive_player:
                defensive_player = random.choice(self.players)

        # --- Actual battle logic ---

        # Someone will intervene!
        # We ask for a random int between 1 and the second int in the ratio form of self.intervention_rate
        if random.randint(1, self.intervention_rate.as_integer_ratio()[1]) == 1:
            pass
