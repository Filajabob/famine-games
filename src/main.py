import time
from player import Player
from game import Game
import utils

utils.typewriter_print("Welcome to the starvation games!")
amount_of_players = int(utils.typewriter_input("How many players should we have? "))
utils.typewriter_print(f"Good. We'll have {amount_of_players} players. What will their names be?")

players = []

for i in range(1, amount_of_players + 1):
    name = utils.typewriter_input(f"Player #{i}: ")
    players.append(Player(name))

utils.typewriter_print("Good! Time to start!")

game = Game(players)

while game.can_run():
    turn_results = game.rotate()
    utils.typewriter_print(f"{turn_results['attacker'].name} attacks {turn_results['defender'].name}")

    try:
        utils.typewriter_print(f"{turn_results['winner'].name} wins.")
    except AttributeError:
        utils.typewriter_print("No one wins")

    time.sleep(1)
