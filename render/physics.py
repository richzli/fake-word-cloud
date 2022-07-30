import random, math

from OpenGL.GL import *

WALL_WT = 20
F_COEFF = 40000
DRAG_COEFF = 0.001
RNDM_COEFF = 400
SECS_PER_SEC = 1

def sign(x):
    if x == 0:
        return 0
    return x/abs(x)

class Universe:
    def __init__(self, x, y):
        self.maxx = x
        self.maxy = y
        self.points = []
    
    def add_point(self, p):
        self.points.append(p)
    
    def shrink_points(self):
        for p in self.points:
            if p.mass > 5:
                p.mass -= 2

    def calculate_forces(self):
        for p in self.points:
            for q in self.points:
                if q.exists:
                    p.forces.append(p.force(q))
        
            if p.mass > 5:
                p.forces.append(p.wall_force("x", WALL_WT, 0))
                p.forces.append(p.wall_force("x", WALL_WT, self.maxx))
                p.forces.append(p.wall_force("y", WALL_WT, 0))
                p.forces.append(p.wall_force("y", WALL_WT, self.maxy))

            p.forces.extend([p.drag_force(), p.random_force()])
    
    def calculate_tick(self, dt):
        self.calculate_forces()
        for p in self.points:
            p.apply_tick(dt)
            if not (0 <= p.x <= self.maxx and 0 <= p.y <= self.maxy):
                p.exists = False
            else:
                p.exists = True
        
        self.points = list(filter(lambda p: p.exists, self.points))

class Particle:
    def __init__(self, x, y, vx = 0, vy = 0, mass = 5, fixed = False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.fixed = fixed
        self.forces = []
        self.exists = True

    def dx(self, p):
        return self.x - p.x

    def dy(self, p):
        return self.y - p.y

    def dist(self, p):
        return (self.dx(p)**2 + self.dy(p)**2)**0.5
    
    def force(self, p):
        if self.dist(p) == 0:
            return (0, 0) # hmm
        magnitude = F_COEFF * self.mass * p.mass / self.dist(p)**2
        return (self.dx(p)*magnitude/self.dist(p), self.dy(p)*magnitude/self.dist(p))
    
    def wall_force(self, axis, wt, pos):
        if axis == "x" and self.x != pos:
            return (F_COEFF * sign(self.x-pos) * self.mass * wt / (self.x - pos)**2, 0)
        elif axis == "y" and self.y != pos:
            return (0, F_COEFF * sign(self.y-pos) * self.mass * wt / (self.y - pos)**2)
        else:
            return (0, 0)

    def drag_force(self):
        return (-self.vx*self.mass*min(abs(self.vx)*DRAG_COEFF, 1), -self.vy*self.mass*min(abs(self.vy)*DRAG_COEFF, 1))

    def random_force(self):
        magnitude = random.random() * self.mass * RNDM_COEFF
        angle = random.random() * 2 * math.pi
        return (math.cos(angle)*magnitude, math.sin(angle)*magnitude)

    def apply_tick(self, dt):
        if not self.fixed:
            t_norm = dt / SECS_PER_SEC
            f_tot = tuple(map(sum, zip((0, 0), *self.forces)))

            self.x += (0.5*f_tot[0]/self.mass*t_norm + self.vx)*t_norm
            self.y += (0.5*f_tot[1]/self.mass*t_norm + self.vy)*t_norm

            self.vx += f_tot[0]/self.mass*t_norm
            self.vy += f_tot[1]/self.mass*t_norm
        else:
            self.vx = 0
            self.vy = 0

        self.forces.clear()

    def draw(self):
        glColor3f(0, 0, 0)
        
        glBegin(GL_QUADS)
        glVertex2f(self.x-self.mass, self.y-self.mass)
        glVertex2f(self.x+self.mass, self.y-self.mass)
        glVertex2f(self.x+self.mass, self.y+self.mass)
        glVertex2f(self.x-self.mass, self.y+self.mass)
        glEnd()