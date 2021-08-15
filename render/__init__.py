import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

BLACK = (0.0, 0.0, 0.0)
PURP_1 = (148/0xff, 131/0xff, 192/0xff)
PURP_2 = (209/0xff, 199/0xff, 235/0xff)
PINK = (236/0xff, 173/0xff, 206/0xff)

SECONDS_PER_WORD = 2

from render.physics import Particle, Universe
from generate import generate_word

class Renderer:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.tick = 0
        self.lastframe = -1
        self.lastword = -1

        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(self.w, self.h)
        self.window = glutCreateWindow("fake word cloud")

        self.univ = Universe(self.w, self.h)
        
        glutDisplayFunc(self.showScreen)
        glutIdleFunc(self.showScreen)
        glutMainLoop()

    def point(self, wd):
        p = wd.point
        color = wd.color

        x = int(p.x)
        y = int(p.y)

        s = p.mass*len(wd.word)//6
        t = p.mass//2

        glColor3f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x-s, y-t)
        glVertex2f(x+s, y-t)
        glVertex2f(x+s, y+t)
        glVertex2f(x-s, y+t)
        glEnd()

    def iterate(self):
        glViewport(0, 0, self.w, self.h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def showScreen(self):
        glClearColor(245/0xff, 241/0xff, 255/0xff, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.iterate()

        for i in self.univ.words:
            self.point(self.univ.words[i])
        now = glutGet(GLUT_ELAPSED_TIME)
        if self.lastframe != -1:
            self.univ.calculate_tick((now-self.lastframe)/1000)
        if self.lastword == -1 or (now-self.lastword)/1000 > SECONDS_PER_WORD:
            self.univ.shrink_points()
            self.univ.add_word(
                Particle((self.w+random.random()*20)//2, (self.h+random.random()*20)//2, 
                    mass=random.randint(10, 50),
                    vx=random.randint(-5, 5),
                    vy=random.randint(-5, 5),
                    fixed=False
                ),
                generate_word(),
                random.choice((BLACK, PURP_1, PURP_2, PINK))
            )
            self.lastword = now
        self.lastframe = now

        self.tick += 1

        glutSwapBuffers()
