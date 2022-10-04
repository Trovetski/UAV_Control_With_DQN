import numpy as np
from math import sin, cos, pi

SIN5 = sin(5*pi/180)
COS5 = cos(5*pi/180)

class Agent:
    def __init__(self,size):
        self.x = np.random.randint(1,size*0.9)
        self.y = np.random.randint(1,size*0.9)

        self.size = size

        self.th = 2*pi*np.random.random()

        self.vx = 0.9*size*cos(self.th)/200
        self.vy = 0.9*size*sin(self.th)/200

    #overwriting special funciton for simpler code
    def __str__(self):
        return f"Agent ({self.x}, {self.y})"

    def __add__(self,other):
        return (self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def isOutOfBounds(self):
        if self.x < 0 or self.y < 0:
            return True
        if self.x > self.size or self.y > self.size:
            return True
        return False
    
    def isCapturedBy(self, other):
        if sum(np.abs(self - other))<self.size/20:
            return True
        return False

    def move(self, delTh):
        #update velocity
        if delTh != 0:
            temp = self.vx
            self.vx = self.vx*COS5 - delTh*self.vy*SIN5
            self.vy = self.vy*COS5 + delTh*temp*SIN5

            self.th += 5*pi/180
            if self.th<0:
              self.th = 2*pi
            if self.th>2*pi:
              self.th=0

        #update position
        self.x += self.vx
        self.y += self.vy
