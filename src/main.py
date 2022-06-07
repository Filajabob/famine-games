import time
import random
import json
import argparse

from player import Player
from game import Game
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--students', action=argparse.BooleanOptionalAction)
args = parser.parse_args()

utils.typewriter_print("Welcome to the starvation games!")
amount_of_players = int(utils.typewriter_input("How many players should we have? "))
utils.typewriter_print(f"Good. We'll have {amount_of_players} players. What will their names be?")

players = []

for i in range(1, amount_of_players + 1):
    name = utils.typewriter_input(f"Player #{i}: ")
    players.append(Player(name))

utils.typewriter_print("Good! Time to start!")

game = Game(players)

# Load texts that we will print for different game components

with open("assets/game/sightings.json", 'r') as f:
    sightings = json.load(f)

with open("assets/game/attacks.json", 'r') as f:
    attacks = json.load(f)

with open("assets/game/turn_results.json", 'r') as f:
    turn_results_texts = json.load(f)

while game.can_run():
    turn_results = game.rotate()

    # Print sighting (cosmetic)
    utils.typewriter_print(
        utils.replace_with_players(
            random.choice(sightings), turn_results["attacker"], turn_results["defender"]
        )
    )

    # Print attack (cosmetic)
    utils.typewriter_print(
        utils.replace_with_players(
            random.choice(attacks), turn_results["attacker"], turn_results["defender"]
        )
    )

    # Print results (necessary)
    utils.typewriter_print(
        utils.replace_with_players(
            random.choice(turn_results_texts[str(turn_results["case"])]), turn_results["attacker"],
            turn_results["defender"]
        )
    )

    time.sleep(1)
