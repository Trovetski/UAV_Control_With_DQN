from agent import Agent
from PIL import Image, ImageDraw
import numpy as np

class Obstacle:
    def __init__(self,size):
        self.x = np.random.randint(1,size-1)
        self.y = np.random.randint(1,size-1)

        self.radii = 25 + np.random.random()*5

        self.size = size
    
    def collision(self, agent):
        if sum(np.abs(agent-self)) < self.radii:
            return True
        return False

class Environment:
    SIZE = 600
    
    MOVE_REWARD = -1
    CAPTURE_REWARD = 150
    COLLISION_REWARD = -200

    def __init__(self):
        self.p = Agent(self.SIZE)
        self.t = Agent(self.SIZE)
        
        self.o1 = Obstacle(self.SIZE)
        self.o2 = Obstacle(self.SIZE)
        self.o3 = Obstacle(self.SIZE)
        self.o4 = Obstacle(self.SIZE)
        self.o5 = Obstacle(self.SIZE)

        self.episode_step = 0
    
    def reset(self):
        #pursuer and target agents
        self.p = Agent(self.SIZE)
        self.t = Agent(self.SIZE)

        self.episode_step = 0

        #initial obervation
        obs = np.array((self.p.x - self.t.x,self.p.y - self.t.y,self.p.vx*self.SIZE/6,self.p.vy*self.SIZE/6 ))/self.SIZE #for model 0
        #obs = np.array((self.p.x - self.t.x,self.p.y - self.t.y,self.p.x,self.p.y,self.p.vx*self.SIZE/6,self.p.vy*self.SIZE/6 ))/self.SIZE #for model 1
        return obs

    def step(self, action):
        self.episode_step += 1
        self.p.move(action-1)

        new_obs = np.array((self.p.x - self.t.x,self.p.y - self.t.y,self.p.vx*self.SIZE/6,self.p.vy*self.SIZE/6 ))/self.SIZE #for model 0
        #new_obs = np.array((self.p.x - self.t.x,self.p.y - self.t.y,self.p.x,self.p.y,self.p.vx*self.SIZE/6,self.p.vy*self.SIZE/6 ))/self.SIZE #for model 1

        iscap = self.t.isCapturedBy(self.p)
        isout = self.p.isOutOfBounds()

        reward = self.MOVE_REWARD + iscap*self.CAPTURE_REWARD + isout*self.COLLISION_REWARD

        done = False
        if reward > 5 or reward < -5 or self.episode_step > 200:
            if iscap:
                print("success")
            done = True
        
        return new_obs, reward, done
    def renderState(self):
        img = Image.fromarray(np.zeros((self.SIZE, self.SIZE, 3), dtype=np.uint8), 'RGB')
        draw = ImageDraw.Draw(img)

        draw.ellipse((self.p.x-8,self.p.y-8,self.p.x+8,self.p.y+8), fill=(255,0,0), outline=(200,200,200))
        draw.ellipse((self.t.x-8,self.t.y-8,self.t.x+8,self.t.y+8), fill=(0,255,0), outline=(200,200,200))
        draw.line((self.p.x,self.p.y,self.p.x+self.p.vx*20,self.p.y+self.p.vy*20),width=3)
        '''
        draw.ellipse((self.o1.x-self.o1.radii,self.o1.y-self.o1.radii,self.o1.x+self.o1.radii,self.o1.y+self.o1.radii), fill=(128,128,128),outline=(200,200,200))
        draw.ellipse((self.o2.x-self.o2.radii,self.o2.y-self.o2.radii,self.o2.x+self.o2.radii,self.o2.y+self.o2.radii), fill=(128,128,128),outline=(200,200,200))
        draw.ellipse((self.o3.x-self.o3.radii,self.o3.y-self.o3.radii,self.o3.x+self.o3.radii,self.o3.y+self.o3.radii), fill=(128,128,128),outline=(200,200,200))
        draw.ellipse((self.o4.x-self.o4.radii,self.o4.y-self.o4.radii,self.o4.x+self.o4.radii,self.o4.y+self.o4.radii), fill=(128,128,128),outline=(200,200,200))
        draw.ellipse((self.o5.x-self.o5.radii,self.o5.y-self.o5.radii,self.o5.x+self.o5.radii,self.o5.y+self.o5.radii), fill=(128,128,128),outline=(200,200,200))
'''
        return img