# from pyglet.graphics.shader import Shader, ShaderProgram  | this shit doesn't exist >:() because old pyglet version :|
from pyglet.gl import *
import pyglet.graphics
import ctypes
#import pyglet.gl.gl
#import pyglet.gl.glu
import math

# Shader sources
vertexSource = """
#version 330
layout(location = 0) in vec2 vertices;
layout(location = 1) in vec4 lightColor(1.0f);
layout(location = 1) in vec4 color;

out vec4 newColor;

void main()
{
    float ambientStrength = 0.9;
    vec3 ambient = ambientStrength * lightColor;

    vec3 result = ambient * color;
    newColor = vec4(result, 1.0);
}  

"""

fragmentSource = """
#version 330

in vec4 newColor;

out vec4 outColor;

void main()
{
    outColor = newColor;
}
"""
    
def updateSky():
    glClearColor(99, 175, 255,1)

def loadShader(shader_type, source):
    shader = glCreateShader(shader_type)
    
    if shader == 0:
        return 0
    
    # Encode the string to bytes
    encoded_string = source.encode('utf-8')
    
    # Create a char pointer
    char_p = ctypes.c_char_p(encoded_string)
    
    # Create a pointer to the char pointer
    char_pp = ctypes.cast(ctypes.pointer(char_p), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
    
    
    glShaderSource(shader, 1, char_pp, None)
    glCompileShader(shader)
    
    # if (glGetShaderiv(shader, GL_COMPILE_STATUS, None)) == GL_FALSE:
    
    # Create an integer to store compilation status
    compileStatus = ctypes.c_int()

    # Pass a pointer to compile_status
    glGetShaderiv(shader, GL_COMPILE_STATUS, ctypes.byref(compileStatus))

    # Check if compilation failed
    # if compile_status.value == GL_FALSE:
    #     infoLog = ctypes.create_string_buffer(512)
    #     infoLog = glGetShaderInfoLog(shader, 512, None, infoLog)
    #     print(infoLog)
    #     glDeleteShader(shader)
    #     return 0
    
    return shader

def loadProgram(vertexSource, fragmentSource):
    vertexShader = loadShader(GL_VERTEX_SHADER, vertexSource)
    
    if not glIsShader(vertexShader):
        print("Error: Invalid shader object before retrieving log.")
        return 0

    if vertexShader == 0:
        return 0
    
    fragmentShader = loadShader(GL_FRAGMENT_SHADER, fragmentSource)
    
    if fragmentShader == 0:
        return 0
    
    program = glCreateProgram()
    
    if program == 0:
        return 0
    
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    
    glLinkProgram(program)
    
    linkStatus = ctypes.c_int()
    
    if (glGetProgramiv(program, GL_LINK_STATUS, ctypes.byref(linkStatus))) == GL_FALSE:
        infoLog = ctypes.create_string_buffer(512)
        glGetProgramInfoLog(program, 512, None, infoLog)
        print("Shader Program Linking Error:", infoLog.value.decode("utf-8"))
        glDeleteProgram(program)
        return 0
    print ("LINKED!")
    return program

program = loadProgram(vertexSource, fragmentSource)
# This causes an error right now
# glUseProgram(program)

batch = pyglet.graphics.Batch()

glEnable(GL_DEPTH_TEST)


def draw():
    batch.draw()

