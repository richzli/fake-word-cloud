import freetype
import numpy

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders

from render import MAX_HEIGHT, BLACK
from render.physics import Particle

font = freetype.Face("font.ttf")
chars = [{} for i in range(MAX_HEIGHT+1)]

class Character:
    def __init__(self, texture, width, height, bearingX, bearingY, advance):
        self.texture = texture
        self.width = width
        self.height = height
        self.bearingX = bearingX
        self.bearingY = bearingY
        self.advance = advance

class Word(Particle):
    def __init__(self, x, y, vx = 0, vy = 0, mass = 5, fixed = False, word=".", color=BLACK):
        super(Word, self).__init__(x, y, vx, vy, mass, fixed)
        global chars
        self.word = word
        self.color = color

        """
        self.height = 0
        for c in word:
            self.height = max(self.height, chars[self.mass][c].bearingY)

        self.width = len(word)
        for c in word:
            self.width += chars[self.mass][c].advance
        self.width += -chars[self.mass][word[-1]].advance + chars[self.mass][word[-1]].width
        """
    
    def draw(self):
        color = self.color

        x = int(self.x)
        y = int(self.y)

        s = self.mass*len(self.word)//4
        t = self.mass//2

        glColor3f(*color)
        
        glBegin(GL_QUADS)
        glVertex2f(x-s, y-t)
        glVertex2f(x+s, y-t)
        glVertex2f(x+s, y+t)
        glVertex2f(x-s, y+t)
        glEnd()

"""
# https://learnopengl.com/In-Practice/Text-Rendering #
# glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
glActiveTexture(GL_TEXTURE0)
for i in range(1, MAX_HEIGHT+1):
    font.set_pixel_sizes(0, i)
    for c in range(ord("a"), ord("z")+1):
        ch = chr(c)
        font.load_char(ch, freetype.FT_LOAD_RENDER)

        textureId = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RED,
            font.glyph.bitmap.width,
            font.glyph.bitmap.rows,
            0,
            GL_RED,
            GL_UNSIGNED_BYTE,
            font.glyph.bitmap.buffer
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        chars[i][ch] = Character(textureId,
            font.glyph.bitmap.width, font.glyph.bitmap.rows,
            font.glyph.bitmap_left, font.glyph.bitmap_top,
            font.glyph.advance
        )
"""