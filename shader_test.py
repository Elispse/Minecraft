import pyglet
import shader
import ctypes
import sys
from pyglet.gl import *

window = pyglet.window.Window(width=400, height=300)
glDisable(GL_DEPTH_TEST)
glClearColor(0.2,0.3,0.3,1.0)

# Shader sources
vertexSource = """
#version 330\n
layout(location = 0) in vec3 vertices;\n
layout(location = 1) in vec4 color;\n

out vec4 newColor;\n

void main()\n
{\n
    float ambientStrength = 0.9;\n
    vec3 result = ambientStrength * color.rgb;\n
    newColor = vec4(result, 1.0);\n
    
    gl_Position = vec4(vertices.x, vertices.y, 0.0, 1.0);
}\n  
"""

fragmentSource = """
#version 330\n

in vec4 newColor;\n

out vec4 fragColor;\n

void main()\n
{\n
    fragColor = newColor;\n
}\n
"""
program = shader.loadProgram(vertexSource, fragmentSource)


# Create Vertex Data
vertex_data = [
    0.0, 0.5, 0.0,
    -0.5, -0.5, 0.0,
    0.5, -0.5, 0.0,
]

color_data = [
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.0, 0.0, 1.0, 1.0,
]

index_data = [0, 1, 2]

vertex_buffer = GLuint()
glGenBuffers(1, ctypes.byref(vertex_buffer))
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
glBufferData(GL_ARRAY_BUFFER, len(vertex_data) * 4, (GLfloat * len(vertex_data))(*vertex_data), GL_STATIC_DRAW)

color_buffer = GLuint()
glGenBuffers(1, ctypes.byref(color_buffer))
glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
glBufferData(GL_ARRAY_BUFFER, len(color_data) * 4, (GLfloat * len(color_data))(*color_data), GL_STATIC_DRAW)

index_buffer = GLuint()
glGenBuffers(1, ctypes.byref(index_buffer))
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(index_data) * 4, (GLuint * len(index_data))(*index_data), GL_STATIC_DRAW)

@window.event
def on_draw():
    window.clear()
    glUseProgram(program)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Bind Vertex Buffer
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0,3, GL_FLOAT, GL_FALSE, 0, 0)
    
    # Bind Color Buffer
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1,4,GL_FLOAT, GL_FALSE,0,0)
        
    # Bind Index Buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer)
    
    glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, 0)
    
    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    

pyglet.app.run()