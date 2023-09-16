import json
import os
import utils
from player import Player, load
from game import Game

players = []

utils.typewriter_print("Welcome to the Famine Games Simulator!")
iterations = int(utils.typewriter_input("Iterations: "))

roster_name = utils.typewriter_input("Input a roster name: ")
roster_fp = f"assets/custom_roster/{roster_name}"

if len(roster_fp) != 0:
    if not os.path.exists(roster_fp):
        raise KeyError("Roster does not exist.")

    utils.typewriter_print("Loading roster...")
    roster_data = roster_fp + "/data.json"

    with open(roster_data, 'r') as f:
        names = json.load(f)  # sussy amogus

    for player_name in names:
        players.append(load(json_file=roster_data, player_name=player_name))

for i in range(0, iterations):
    game = Game(players)

    while game.can_run():
        game.rotate()

    game.finish_game()
    print(f"The game has finished! The winner is {game.players[0].name}!", delay=0.05)
