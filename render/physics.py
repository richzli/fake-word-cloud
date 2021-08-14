import random, math
from render import BLACK

WALL_WT = 20
F_COEFF = 1000
DRAG_COEFF = 0.005
RNDM_COEFF = 0.1
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
        self.colors = []
        self.exists = []
    
    def add_point(self, p, c=BLACK):
        self.points.append(p)
        self.colors.append(c)
        self.exists.append(True)
    
    def shrink_points(self):
        for i in range(len(self.points)):
            if self.points[i].mass > 1:
                self.points[i].mass -= 1

    def calculate_forces(self):
        for i in range(len(self.points)):
            if not self.exists[i]:
                continue
            p = self.points[i]
            for j in range(len(self.points)):
                q = self.points[j]
                if i != j and self.exists[j]:
                    p.forces.append(p.force(q))
        
            if p.mass > 3:
                p.forces.append(p.wall_force("x", WALL_WT, 0))
                p.forces.append(p.wall_force("x", WALL_WT, self.maxx))
                p.forces.append(p.wall_force("y", WALL_WT, 0))
                p.forces.append(p.wall_force("y", WALL_WT, self.maxy))

            p.forces.extend([p.drag_force(), p.random_force()])
    
    def calculate_tick(self, dt):
        self.calculate_forces()
        for i in range(len(self.points)):
            p = self.points[i]
            p.apply_tick(dt)
            if not (0 <= p.x <= self.maxx and 0 <= p.y <= self.maxy):
                self.exists[i] = False
            else:
                self.exists[i] = True

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
        if axis == "x":
            return (F_COEFF * sign(self.x-pos) * self.mass * wt / (self.x - pos)**2, 0)
        elif axis == "y":
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

