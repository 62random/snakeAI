import __future__
import random
import curses
from snake import *
import subprocess
import sys
import turtle

class Game:
    def __init__(self):

        self.rendering = False
        self.sh = 15
        self.sw = 15
        self.steps = 0

        self.snake = Snake(self.sh - 1, self.sw - 1)
        self.food = Food(self.sh - 1, self.sw - 1)

        while self.food.position in self.snake.parts:
            self.food = Food(self.sh, self.sw)


        self.action = 2 #move right

    def _render(self, bool):
        self.rendering = bool
        if bool:
            loadWindow = turtle.Screen()
            turtle.speed(0)
            turtle.delay(0)
            turtle.hideturtle()
            turtle.colormode(255)
            turtle.pencolor((255,255,255))
            turtle.setpos(0, 0)
            turtle.pensize(5)

            for i in range(0, self.sw):
                for j in range(0, self.sh):
                    if i in [0, self.sw - 1] or j in [0, self.sh -1]:
                        self.draw(i,j, (0,0,0))

            turtle.setup(750, 750)
        elif self.rendering == True:
            self.rendering = True
            for i in range(0, self.sw):
                for j in range(0, self.sh):
                    if i in [0, self.sw - 1] or j in [0, self.sh -1]:
                        self.draw(i,j, (255,255,255))

            for p in self.snake.parts:
                self.draw(p[0], p[1], (255,255,255))
            self.draw(self.food.position[0], self.food.position[1], (255,255,255))
            self.rendering = False


    def _reset(self):
        self.steps = 0

        for p in self.snake.parts:
            self.draw(p[0], p[1], (255,255,255))
        self.draw(self.food.position[0], self.food.position[1], (255,255,255))

        self.snake = Snake(self.sh - 1, self.sw - 1)
        self.food = Food(self.sh - 1, self.sw - 1)

        while self.food.position in self.snake.parts:
            self.food = Food(self.sh, self.sw)

        self.draw(self.food.position[0], self.food.position[1], (100,100,100))

        self.action = 2 #move right


        return self.state()



    def _step(self, action):
        self.steps += 1
        if(self.snake.parts[0][0] in [1, self.sh - 1] or self.snake.parts[0][1]) in [1, self.sw - 1] or self.snake.parts[0] in self.snake.parts[1:]:
            #print("Snake died with size " + str(len(self.snake.parts)))
            #self._render(False)
            return self.state(), -100, True, len(self.snake.parts)

        if self.steps == 50:
            return self.state(), 0, True, len(self.snake.parts)

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
            r = 400
            self.food = None
            while self.food is None:
                nf = Food(self.sh, self.sw)
                if nf.position not in self.snake.parts:
                    self.food = nf
            self.draw(self.food.position[0], self.food.position[1], (100, 100, 100))
        else:
            tail = self.snake.parts.pop()
            self.draw(tail[0], tail[1], (255,255,255))
        self.draw(self.snake.parts[0][0], self.snake.parts[0][1], (0,0,0))


        return self.state(), r - 1, False, len(self.snake.parts)

    def state(self):
        dist_wall_right = self.sw - 1 - self.snake.parts[0][1]
        dist_wall_left = self.snake.parts[0][1] - 1
        dist_wall_down = self.sh - 1 - self.snake.parts[0][0]
        dist_wall_up = self.snake.parts[0][0] - 1

        dist_food_right = self.food.position[1] - self.snake.parts[0][1]
        dist_food_down = self.food.position[0] - self.snake.parts[0][0]

        a = [self.sh] #right
        b = [self.sh] #left
        c = [self.sh] #down
        d = [self.sh] #up
        e = [self.sh] #ne
        f = [self.sh] #nw
        g = [self.sh] #se
        h = [self.sh] #sw

        x = self.snake.parts[0][1]
        y = self.snake.parts[0][0]
        for i in range(self.sh, 0, -1):
            if (y, x + i) in self.snake.parts: #right
                a.append(i)
            if (y, x - i) in self.snake.parts: #left
                b.append(i)
            if (y + i, x) in self.snake.parts: # down
                c.append(i)
            if (y - i, x) in self.snake.parts: # up
                d.append(i)
            if (y + i, x + i) in self.snake.parts: #se
                e.append(i)
            if (y - i, x + i) in self.snake.parts: #ne
                f.append(i)
            if (y + i, x - i) in self.snake.parts: #sw
                g.append(i)
            if (y - i, x - i) in self.snake.parts: #nw
                h.append(i)

        ret = [
                    dist_wall_right, dist_wall_left, dist_wall_down, dist_wall_up,      #wall
                    dist_food_right, dist_food_down,      #food
                    min(a), min(b), min(c), min(d), min(e), min(f), min(g), min(h)                                      #snake body
                ]
        #print(ret)
        return  ret

    def draw(self, i,j, color):
        if self.rendering:
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
