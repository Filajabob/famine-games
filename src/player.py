class Player:
    def __init__(self, name: str, offense: int=0, defense: int=0):
        """
        Object that holds data for a certain someone in a src.game.Game

        :param name: str: The name of the player
        :param offense: int: How good their offense is. High scores make the player more likely to successfully attack
        :param defense: How good thier defense is. Similar to the above, except for defense
        """

        self.name = name
        self.offense = offense
        self.defense = defense
