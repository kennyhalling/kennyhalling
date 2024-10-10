# This section of the program holds functions to roll a die of various sides.
import random

class Dice:
    # initialize number of sides on a dice
    def __init__(self, sides):
        if sides <= 0:
            raise ValueError("The number of sides must be greater than 0")
        self._sides = sides
    
    # roll the dice
    def roll(self):
        return random.randrange(1, self._sides + 1)
    
    #get number of sides
    def get_sides(self):
        return self._sides
    
    #set number of sides to a different number
    def set_sides(self, sides):
        if sides <= 0:
            raise ValueError("The number of sides must be greater than 0")
        self._sides = sides
