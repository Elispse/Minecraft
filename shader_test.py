import pyglet
import shader
import ctypes
import sys
from pyglet.gl import *

window = pyglet.window.Window(width=400, height=300)
glDisable(GL_DEPTH_TEST)
glClearColor(0.2,0.3,0.3,1.0)

buffers = {}

# Shader sources
vertexSource = """
#version 330
layout(location = 0) in vec3 vertexPosition;
layout(location = 1) in vec3 vertexNormal;
layout(location = 2) in vec2 vertexTextureCoord;

out vec4 newColor;

void main()
{

    
    vec3 diffuseLight = {0.9, 0.9, 0.9};
    vec4 gl_Position = vec4(vertexPosition,1.0);
}
"""

fragmentSource = """
#version 330
in vec3 diffuseLight;
in vec2 textureCoord;

layout (location = 0) out vec4 fragColor;

void main()
{
    fragColor = vec4(diffuseLight, 1.0);
}
"""
program = shader.loadProgram(vertexSource, fragmentSource)

vertex_data = [
    0.5, 0.5, 0.0,
    -0.5, 0.5, 0.0,
    0.5, -0.5, 0.0,
    -0.5, -0.5, 0.0
]

normal_data = [0,1,0]

textureCoords = [
    0.0, 0.0,  # Bottom-left
    1.0, 0.0,  # Bottom-right
    1.0, 1.0,  # Top-right
    0.0, 1.0   # Top-left
]

index_data = [0, 1, 2, 0, 2, 3]

if "vertex_buffer" not in buffers:
    buffers["vertex_buffer"] = GLuint()
    glGenBuffers(1, ctypes.byref(buffers["vertex_buffer"]))

glBindBuffer(GL_ARRAY_BUFFER, buffers["vertex_buffer"])
glBufferData(GL_ARRAY_BUFFER, len(vertex_data) * 4, (GLfloat * len(vertex_data))(*vertex_data), GL_STATIC_DRAW)

if "normal_buffer" not in buffers:
    buffers["normal_buffer"] = GLuint()
    glGenBuffers(1, ctypes.byref(buffers["normal_buffer"]))
    
glBindBuffer(GL_ARRAY_BUFFER, buffers["normal_buffer"])
glBufferData(GL_ARRAY_BUFFER, len(normal_data) * 4, (GLfloat * len(normal_data))(*normal_data), GL_STATIC_DRAW)

if "texture_buffer" not in buffers:
    buffers["texture_buffer"] = GLuint()
    glGenBuffers(1, ctypes.byref(buffers["texture_buffer"]))

glBindBuffer(GL_ARRAY_BUFFER, buffers["texture_buffer"])
glBufferData(GL_ARRAY_BUFFER, len(textureCoords) * 4, (GLfloat * len(textureCoords))(*textureCoords), GL_STATIC_DRAW)

if "index_buffer"  not in buffers:
    buffers["index_buffer"] = GLuint()
    glGenBuffers(1, ctypes.byref(buffers["index_buffer"]))

@window.event
def on_draw():
    window.clear()
    glUseProgram(program)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Clear and enable stuffs
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Bind Vertex Buffer
    glBindBuffer(GL_ARRAY_BUFFER, buffers["vertex_buffer"])
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0,3, GL_FLOAT, GL_FALSE, 0, 0)
    
    # Bind Normal Buffer
    glBindBuffer(GL_ARRAY_BUFFER, buffers["normal_buffer"])
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1,3,GL_FLOAT, GL_FALSE,0,0)
    
    # Bind Texture Buffer
    glBindBuffer(GL_ARRAY_BUFFER, buffers['texture_buffer'])
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2,2, GL_FLOAT, GL_FALSE, 0, 0)
    
    # Bind Index Buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers["index_buffer"])
    
    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    

pyglet.app.run()