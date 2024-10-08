# This section of the program holds functions to roll a die of various sides.
import random

class Dice:
    def roll(sides):
        print(random.randrange(1, sides))