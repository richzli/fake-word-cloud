import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

BLACK = (0.0, 0.0, 0.0)
PURP_1 = (0xac/0xff, 0x91/0xff, 0xf7/0xff)
PURP_2 = (0xd1/0xff, 0xc7/0xff, 0xeb/0xff)

from render.physics import Particle, Universe

class Renderer:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.tick = 0

        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(self.w, self.h)
        self.window = glutCreateWindow("fake word cloud")

        self.univ = Universe(self.w, self.h)
        for i in range(5):
            for j in range(5):
                self.univ.add_point(
                    Particle(100+50*i, 100+50*j, 
                        mass=random.randint(5, 20),
                        fixed=False
                    ),
                    random.choice((BLACK, PURP_1, PURP_2))
                )
        
        glutDisplayFunc(self.showScreen)
        glutIdleFunc(self.showScreen)
        glutMainLoop()

    def point(self, p, color):
        x = int(p.x)
        y = int(p.y)

        s = p.mass//2

        glColor3f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x-s, y-s)
        glVertex2f(x+s, y-s)
        glVertex2f(x+s, y+s)
        glVertex2f(x-s, y+s)
        glEnd()

    def iterate(self):
        glViewport(0, 0, self.w, self.h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def showScreen(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.iterate()
        for i in range(len(self.univ.points)):
            self.point(self.univ.points[i], self.univ.colors[i])
        self.univ.calculate_tick(0.01)
        self.tick += 1
        #if self.tick % 1000 == 0:
        #    self.univ.shrink_points()
        glutSwapBuffers()
