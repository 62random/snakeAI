import random
import curses
from snake import *
import subprocess
import sys
import turtle

class Game:
    def __init__(self):

        #loadWindow = turtle.Screen()
        #turtle.speed(0)
        #turtle.delay(0)
        #turtle.hideturtle()
        #turtle.colormode(255)
        #turtle.pencolor((255,255,255))
        #turtle.setpos(0, 0)
        #turtle.pensize(5)

        self.sh = 30
        self.sw = 30
        self.steps = 0

        #for i in range(0, self.sw):
            #for j in range(0, self.sh):
                #if i in [0, self.sw - 1] or j in [0, self.sh -1]:
                    ##draw(i,j, (0,0,0))

        #turtle.setup(750, 750)

        self.snake = Snake(self.sh - 1, self.sw - 1)
        self.food = Food(self.sh - 1, self.sw - 1)

        while self.food.position in self.snake.parts:
            self.food = Food(self.sh, self.sw)

        #draw(self.food.position[0], self.food.position[1], (100,100,100))

        self.action = 2 #move right



    def _reset(self):
        self.steps = 0
        #for p in self.snake.parts:
            #draw(p[0], p[1], (255,255,255))
        #draw(self.food.position[0], self.food.position[1], (255,255,255))


        #for i in range(0, self.sw):
            #for j in range(0, self.sh):
                #if i in [0, self.sw - 1] or j in [0, self.sh -1]:
                    #draw(i,j, (0,0,0))

        #turtle.setup(750, 750)

        self.snake = Snake(self.sh - 1, self.sw - 1)
        self.food = Food(self.sh - 1, self.sw - 1)

        while self.food.position in self.snake.parts:
            self.food = Food(self.sh, self.sw)

        #draw(self.food.position[0], self.food.position[1], (100,100,100))

        self.action = 2 #move right


        return self.state()



    def _step(self, action):
        self.steps += 1
        if(self.snake.parts[0][0] in [1, self.sh - 1] or self.snake.parts[0][1]) in [1, self.sw - 1] or self.snake.parts[0] in self.snake.parts[1:]:
            print("Snake died with size " + str(len(self.snake.parts)))
            return self.state(), -100, True, True

        r = 0

        self.action = action
        new_head = (self.snake.parts[0][0], self.snake.parts[0][1])
        if self.action == 0:
            new_head = (new_head[0] + 1 , new_head[1])
        if self.action == 1:
            new_head = (new_head[0] - 1 , new_head[1])
        if self.action == 2:
            new_head =  (new_head[0], new_head[1] + 1)
        if self.action == 3:
            new_head = (new_head[0], new_head[1] - 1)

        self.snake.parts.insert(0, new_head)

        if self.snake.parts[0] == self.food.position:
            r += 10
            self.food = None
            while self.food is None:
                nf = Food(self.sh, self.sw)
                if nf.position not in self.snake.parts:
                    self.food = nf
            #draw(self.food.position[0], self.food.position[1], (100, 100, 100))
        else:
            tail = self.snake.parts.pop()
            #draw(tail[0], tail[1], (255,255,255))
        #draw(self.snake.parts[0][0], self.snake.parts[0][1], (0,0,0))

        return self.state(), r + 1, False, True

    def state(self):
        dist_wall_right = self.sw - 1 - self.snake.parts[0][1]
        dist_wall_left = self.snake.parts[0][1] - 1
        dist_wall_down = self.sh - 1 - self.snake.parts[0][0]
        dist_wall_up = self.snake.parts[0][0] - 1

        dist_food_right = self.food.position[1] - self.snake.parts[0][1]
        dist_food_left =  self.snake.parts[0][1] - self.food.position[1]
        dist_food_down = self.food.position[0] - self.snake.parts[0][0]
        dist_food_up =  self.snake.parts[0][0] - self.food.position[0]

        a = [100] #right
        b = [100] #left
        c = [100] #down
        d = [100] #up
        for p in self.snake.parts[1:]:
            a.append(p[1] - self.snake.parts[0][1])
            b.append(self.snake.parts[0][1] - p[1])
            c.append(p[0] - self.snake.parts[0][0])
            d.append(self.snake.parts[0][0] - p[0])


        return  [
                    dist_wall_right, dist_wall_left, dist_wall_down, dist_wall_up,      #wall
                    dist_food_right, dist_food_left, dist_food_down, dist_food_up,      #food
                    min(a), min(b), min(c), min(d)                                      #snake body
                ]

def draw(i,j, color):
    turtle.penup()
    turtle.pencolor(color)
    turtle.setpos(i*10, j*10)
    turtle.pendown()
    turtle.forward(10)
    turtle.left(90)
    turtle.forward(10)
    turtle.left(90)
    turtle.forward(10)
    turtle.left(90)
    turtle.forward(10)
    turtle.left(90)
    turtle.pencolor((0,0,0))
