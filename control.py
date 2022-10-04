import math

class PBC:
    k = 0.005

    def mod(self, v):
        return math.sqrt(v.x**2+v.y**2)
    
    def dot(self, v, u):
        return v.x*u.x+v.y*u.y
    
    def angleWith(self, v, u):
        return math.acos(self.dot(v, u)/(self.mod(v)*self.mod(u)+0.0001))
    
    def rotate(self, v, theta):
        temp = v.x
        v.x = math.cos(theta)*v.x + math.sin(theta)*v.y
        v.y = math.cos(theta)*v.y - math.sin(theta)*temp

    def getAction(self,env):
        l = Vector((env.t-env.p)[0],(env.p-env.t)[1])
        v = Vector(env.p.vx,env.p.vy)

        beta = self.angleWith(v,l)
        action = 0

        self.rotate(v,self.k*beta)
        if(beta<self.angleWith(v,l)):
            self.rotate(v,-2*self.k*beta)
            action = 2
        
        if beta<math.pi/36 and beta>-math.pi/36:
            action=1
        
        return action
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y