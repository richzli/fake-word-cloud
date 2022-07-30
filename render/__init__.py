import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

BLACK = (0.0, 0.0, 0.0)
PURP_1 = (148/0xff, 131/0xff, 192/0xff)
PURP_2 = (209/0xff, 199/0xff, 235/0xff)
PINK = (236/0xff, 173/0xff, 206/0xff)

MAX_HEIGHT = 50
SECONDS_PER_WORD = 2

from render.physics import Particle, Universe
from render.word import *
from data.generate import generate_word

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
        glutReshapeFunc(self.resize)
        glutMainLoop()

    def resize(self, ww, hh):
        self.w = ww
        self.h = hh
        self.univ.maxx = ww
        self.univ.maxy = hh

    def iterate(self):
        glViewport(0, 0, self.w, self.h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.w, 0.0, self.h, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def showScreen(self):
        glClearColor(245/0xff, 241/0xff, 255/0xff, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.iterate()

        for p in self.univ.points:
            p.draw()
        now = glutGet(GLUT_ELAPSED_TIME)
        if self.lastframe != -1:
            self.univ.calculate_tick((now-self.lastframe)/1000)
        if self.lastword == -1 or (now-self.lastword)/1000 > SECONDS_PER_WORD:
            self.univ.shrink_points()
            self.univ.add_point(
                Word((self.w+random.random()*20)//2, (self.h+random.random()*20)//2, 
                    mass=50,
                    vx=random.randint(-5, 5),
                    vy=random.randint(-5, 5),
                    fixed=False,
                    word=generate_word(),
                    color=random.choice((BLACK, PURP_1, PURP_2, PINK))
                )
            )
            self.lastword = now
        self.lastframe = now

        self.tick += 1

        glutSwapBuffers()
