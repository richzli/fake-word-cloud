import random, math
from render import BLACK
from render.word import Word

WALL_WT = 20
F_COEFF = 40000
DRAG_COEFF = 0.05
RNDM_COEFF = 100
SECS_PER_SEC = 1

def sign(x):
    if x == 0:
        return 0
    return x/abs(x)

class Universe:
    def __init__(self, x, y):
        self.maxx = x
        self.maxy = y
        self.ids = 0
        self.words = {}
    
    def add_word(self, p, w, c=BLACK):
        self.ids += 1
        self.words[self.ids] = Word(p, w, c)
    
    def shrink_points(self):
        for i in self.words:
            if self.words[i].point.mass > 5:
                self.words[i].point.mass -= 2

    def calculate_forces(self):
        for i in self.words:
            if not self.words[i].exists:
                continue
            p = self.words[i].point
            for j in self.words:
                q = self.words[j].point
                if i != j and self.words[j].exists:
                    p.forces.append(p.force(q))
        
            if p.mass > 5:
                p.forces.append(p.wall_force("x", WALL_WT, 0))
                p.forces.append(p.wall_force("x", WALL_WT, self.maxx))
                p.forces.append(p.wall_force("y", WALL_WT, 0))
                p.forces.append(p.wall_force("y", WALL_WT, self.maxy))

            p.forces.extend([p.drag_force(), p.random_force()])
    
    def calculate_tick(self, dt):
        self.calculate_forces()
        for i in list(self.words.keys()):
            p = self.words[i].point
            p.apply_tick(dt)
            if not (0 <= p.x <= self.maxx and 0 <= p.y <= self.maxy):
                p.exists = False
                del self.words[i]
            else:
                p.point = True

class Particle:
    def __init__(self, x, y, vx = 0, vy = 0, mass = 5, fixed = False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.fixed = fixed
        self.forces = []

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
        return (-self.vx*abs(self.vx)*DRAG_COEFF, -self.vy*abs(self.vy)*DRAG_COEFF)

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

