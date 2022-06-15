import random
import utils


class Event:
    def __init__(self, players: list = None, death_rate: float = None):
        self.players = players
        self.death_rate = death_rate
        self.eliminated_players = None

    def choose_eliminated_players(self):
        num_sections = round(100 / (self.death_rate * 100))
        random.shuffle(self.players)

        sections = utils.split_list(self.players, num_sections)

        self.eliminated_players = random.choice(sections)
        return self.eliminated_players

class NoEvent(Event):
    pass