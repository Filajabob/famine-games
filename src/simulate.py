import json
import utils
from player import Player, load
from game import Game

players = []

utils.typewriter_print("Welcome to the Famine Games Simulator!")
iterations = int(utils.typewriter_input("Iterations: "))

utils.typewriter_print("Loading students...")
with open("assets/custom_roster/students/names.json", 'r') as f:
    names = json.load(f)  # sussy amogus

for player_name in names:
    players.append(load(json_file="assets/custom_roster/students/data.json", player_name=player_name))

for i in range(0, iterations):
    game = Game(players)

    while game.can_run():
        game.rotate()

    game.finish_game()
    utils.typewriter_print(f"The game has finished! The winner is {game.players[0].name}!", delay=0.05)
