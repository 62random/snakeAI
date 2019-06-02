import curses
import random

DIRECTIONS = {
                "RIGHT":  curses.KEY_RIGHT,
                "LEFT": curses.KEY_LEFT,
                "UP":   curses.KEY_UP,
                "DOWN": curses.KEY_DOWN
        }

class Snake:
    def __init__(self, y, x):
        self.parts = [
                        (y/2, x/4),
                        (y/2, x/4 - 1),
                        (y/2, x/4 - 2)
                ]

class Food:
    def __init__(self, y, x):
        self.position = (random.randint(2, y - 3), random.randint(2, x - 3))
