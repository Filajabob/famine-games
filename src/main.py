from player import Player
from game import Game
import time

word = "Welcome to Famine Games! The totally original and not overused game idea since 1969!"
for letter in list(word):
    print(letter, end='', flush=True)
    time.sleep(0.1)

student_num = input("How many students do you want to got to hell- I mean the Famine Games.")
