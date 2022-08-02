import freetype
import numpy

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders

from render import MAX_HEIGHT, BLACK
from render.physics import Particle

font = freetype.Face("font.ttf")
chars = [{} for i in range(MAX_HEIGHT+1)]
vao = None
vbo = None
shader_program = None

vertex_shader_text = """
#version 330 core
layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>
out vec2 TexCoords;

uniform mat4 projection;

void main()
{
    gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
    TexCoords = vertex.zw;
}
"""

fragment_shader_text = """
#version 330 core
in vec2 TexCoords;
out vec4 color;

uniform sampler2D text;
uniform vec3 textColor;

void main()
{    
    vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
    color = vec4(textColor, 1.0) * sampled;
}
"""

class Character:
    def __init__(self, texture, width, height, bearingX, bearingY, advance):
        self.texture = texture
        self.width = width
        self.height = height
        self.bearingX = bearingX
        self.bearingY = bearingY
        self.advance = advance.x

# https://learnopengl.com/In-Practice/Text-Rendering #
def init():
    global chars, vao, vbo, shader_program

    # characters
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

    # blending
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # shaders
    vertex_shader = shaders.compileShader(vertex_shader_text, GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(fragment_shader_text, GL_FRAGMENT_SHADER)
    shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

    # buffers
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    float_size = numpy.dtype("float32").itemsize
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, float_size * 6 * 4, None, GL_DYNAMIC_DRAW)
    glVertexAttribPointer(0, 4, GL_FLOAT, False, 4 * float_size, None)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

class Word(Particle):
    def set_metrics(self):
        self.height = 0
        self.width = 0
        for c in self.word:
            self.height = max(self.height, chars[self.mass][c].bearingY)
            self.width += chars[self.mass][c].advance
        self.width += -chars[self.mass][self.word[-1]].advance + chars[self.mass][self.word[-1]].width

    def __init__(self, x, y, vx = 0, vy = 0, mass = 5, fixed = False, word=".", color=BLACK):
        super().__init__(x, y, vx, vy, mass, fixed)
        global chars
        self.word = word
        self.color = color
        self.set_metrics()
    
    def apply_tick(self, dt):
        super().apply_tick(dt)
        self.set_metrics()

    def draw_rect(self):
        x = int(self.x)
        y = int(self.y)

        s = self.width // 64 // 2
        t = self.height // 2

        glColor3f(*self.color)
        
        glBegin(GL_QUADS)
        glVertex2f(x-s, y-t)
        glVertex2f(x+s, y-t)
        glVertex2f(x+s, y+t)
        glVertex2f(x-s, y+t)
        glEnd()

    def draw(self):
        global chars, shader_program

        x = int(self.x)-self.width // 128
        y = int(self.y)-self.height // 2
        pt = self.mass

        glUseProgram(shader_program)
        glUniform3f(glGetUniformLocation(shader_program, "textColor"), *self.color)
        glActiveTexture(GL_TEXTURE0)
        glBindVertexArray(vao)

        for c in self.word:
            ch = chars[pt][c]
            w = ch.width
            h = ch.height
            
            xx = x + ch.bearingX
            yy = y - (ch.height - ch.bearingY)

            vertices = numpy.array([
                xx,     yy + h, 0.0, 0.0,
                xx,     yy,     0.0, 1.0,
                xx + w, yy,     1.0, 1.0,

                xx,     yy + h, 0.0, 0.0,
                xx + w, yy,     1.0, 1.0,
                xx + w, yy + h, 1.0, 0.0
            ], dtype=numpy.float32)

            float_size = vertices.itemsize
            glBindTexture(GL_TEXTURE_2D, ch.texture)
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferSubData(GL_ARRAY_BUFFER, 0, float_size * vertices.size, vertices)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

            glDrawArrays(GL_TRIANGLES, 0, 6)

            x += ch.advance // 64

        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
