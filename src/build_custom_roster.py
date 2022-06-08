import json
from player import Player

with open("assets/custom_roster/students/names.json", 'r') as f:
    students = json.load(f)

for student in students:
    player = Player(student)
    player.serialize("assets/custom_roster/students/data.json")
