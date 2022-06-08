import json


class Player:
    def __init__(self, name: str, offense: int = 0, defense: int = 0, json_file: str = None, stats: dict = None):
        """
        Object that holds data for a certain someone in a src.game.Game
        When Player is initialized via __init__, it will be assumed that this player is a new player. Load from
        Player.load() to load from a dict

        :param name: str: The name of the player
        :param offense: int: How good their offense is. High scores make the player more likely to successfully attack
        :param defense: int: How good their defense is. Similar to the above, except for defense
        :param json_file: str: Protected parameter determining which JSON file provided data for the player
        """

        self.name = name
        self.offense = offense
        self.defense = defense

        self.json_file = json_file

        if not stats:
            self.stats = {
                "total_kills": 0,  # total kills
                "successful_defenses": 0,  # amount of times this player survived an attack
                "attempted_attacks": 0,
                "attempted_defenses": 0,
                "kills_off_attacks": 0,  # amount of kills from attacks
                "kills_off_defenses": 0,  # amount of kills from self-defense (defending)
                "kills_off_interventions": 0,  # amount of kills from interventions,
                "rounds_survived": 0,  # amount of rounds survived
                "wins": 0,  # total wins
                "total_games": 0  # total games played
            }
        else:
            self.stats = stats

    def serialize(self, file):
        if not file:
            return

        with open(file, 'r+') as f:
            data = json.load(f)
            data[self.name] = {
                "name": self.name,
                "offense": self.offense,
                "defense": self.defense,
                "stats": self.stats
            }

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()


def load(data: dict = None, *, json_file: str = None, player_name: str = None):
    """
    Loads a player from a dict or JSON file
    If player is loaded into the parameter 'data', no other arguments should be passed. If not, json_file and
    player_name must have arguments passed to them. If all are passed, the data will be loaded from json_file.

    :param data: dict: Dict containing all player data. Defaults to None
    :param json_file: JSON file containing relevant data. Defaults to None
    :param player_name: The player's name. Defaults to None
    :return: src.player.Player
    """

    if json_file and player_name:
        with open(json_file, 'r') as f:
            data = json.load(f)[player_name]
        data["json_file"] = json_file
    elif player_name and not json_file:
        raise TypeError("json_file was passed, missing player_name")

    return Player(**data)
