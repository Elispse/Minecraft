# from pyglet.graphics.shader import Shader, ShaderProgram  | this shit doesn't exist >:() because old pyglet version :|
from pyglet.gl import *
import pyglet.graphics
import ctypes
import block
#import pyglet.gl.gl
#import pyglet.gl.glu
import math

FaceNormals = [
        ( 0, 1, 0),
        ( 0,-1, 0),
        (-1, 0, 0),
        ( 1, 0, 0),
        ( 0, 0, 1),
        ( 0, 0,-1),
    ]

# Shader sources
vertexSource = """
#version 330
layout(location = 0) in vec3 vertexPosition;
layout(location = 1) in vec3 vertexNormal;
layout(location = 2) in vec2 vertexTextureCoord;

out vec3 diffuseLight;
out vec2 textureCoord;

uniform vec3 Ld; // light intensity

uniform mat4 MVP;
uniform mat3 normalMatrix;
uniform vec4 lightPosition;

void main()
{
    vec3 tNorm = normalize( normalMatrix * vertexNormal );
    vec3 s = normalize(vec3(lightPosition));
    
    diffuseLight = Ld * max( dot (s , tNorm), 0.0 );
    textureCoord = vertexTextureCoord;
    gl_Position = MVP * vec4(vertexPosition,1.0);
}
"""

fragmentSource = """
#version 330\n

in vec3 diffuseLight;
in vec2 textureCoord;

layout (location = 0) out vec4 fragColor;

uniform sampler2D textureSampler;

void main()
{
    vec4 texColor = texture(textureSampler, textureCoord);
    fragColor = vec4(1, 0, 0, 1); //vec4(diffuseLight, 1.0) * texColor;
}
"""

def updateSky():
    glClearColor(0, 0.1, 0.1, 1)

def loadShader(shader_type, source):
    
    shader = glCreateShader(shader_type)
    
    if shader == 0:
        return 0
    
    # Print GLSL Errors
    
    encoded_string = source.encode('utf-8')
    char_p = ctypes.c_char_p(encoded_string)
    char_pp = ctypes.cast(ctypes.pointer(char_p), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))

    # Pass shader source and compile
    glShaderSource(shader, 1, char_pp, None)
    glCompileShader(shader)

    # Get compilation status
    compile_status = ctypes.c_int()
    glGetShaderiv(shader, GL_COMPILE_STATUS, ctypes.byref(compile_status))

    # If compilation failed, print the error log
    if compile_status.value == GL_FALSE:
        info_log = ctypes.create_string_buffer(1024)
        glGetShaderInfoLog(shader, 1024, None, info_log)
        print(f"❌ Shader Compilation Failed ({'Vertex' if shader_type == GL_VERTEX_SHADER else 'Fragment'} Shader):")
        print(info_log.value.decode('utf-8'))  # Print readable error log
        glDeleteShader(shader)
        return 0
    else:
        print(f"✅ Shader Compiled Successfully ({'Vertex' if shader_type == GL_VERTEX_SHADER else 'Fragment'} Shader)")
    
    
    # Encode the string to bytes
    encoded_string = source.encode('utf-8')
    
    # Create a char pointer
    char_p = ctypes.c_char_p(encoded_string)
    
    # Create a pointer to the char pointer
    char_pp = ctypes.cast(ctypes.pointer(char_p), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
    
    print(GL_VERSION)
    
    glShaderSource(shader, 1, char_pp, None)
    glCompileShader(shader)
    
    # if (glGetShaderiv(shader, GL_COMPILE_STATUS, None)) == GL_FALSE:
    
    # Create an integer to store compilation status
    compileStatus = ctypes.c_int()
    
    glGetShaderiv(shader, GL_COMPILE_STATUS, ctypes.byref(compileStatus))
    
    # Check if compilation failed
    if  compileStatus.value == GL_FALSE:
        infoLog = ctypes.create_string_buffer(512)
        infoLog = glGetShaderInfoLog(shader, 512, None, infoLog)
        print("Compilation Failure: " + str(infoLog))
        glDeleteShader(shader)
        return 0
    print("COMPILED")
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
    
    glGetProgramiv(program, GL_LINK_STATUS, ctypes.byref(linkStatus))
    
    if linkStatus.value == GL_FALSE:
        infoLog = ctypes.create_string_buffer(512)
        glGetProgramInfoLog(program, 512, None, infoLog)
        print("Shader Program Linking Error:", infoLog.value.decode("utf-8"))
        glDeleteProgram(program)
        return 0
    print ("LINKED!")
    return program

def loadTexture(imagePath):
    texture_id = GLuint()
    glGenTextures(1, ctypes.byref(texture_id))
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    # Loading Image
    image = pyglet.image.load(imagePath) # <---
    image_data = image.get_data("RGB", image.width * 3) # Mess with this stuff maybe fellas
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    return texture_id

glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)
#glMatrixMode(GL_PROJECTION)
#glMatrixMode(GL_MODELVIEW)
gluPerspective(45, 800/600, 0.1, 100)
glLoadIdentity()

program = loadProgram(vertexSource, fragmentSource)
texture = loadTexture("texture.png")
buffers = {}

# ------------------ suffering

def render_faces(faceVerts, faceNormals, texData):
    # Create Vertex Data
    for index, vertData in enumerate(faceVerts):
        vertex_data = vertData
        normal_data = faceNormals[index]
        
        # textureCoords = block.GRASS
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
            
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers["index_buffer"])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(index_data) * 4, (GLuint * len(index_data))(*index_data), GL_STATIC_DRAW)
        
        glUseProgram(program)
        
        # Texture
        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        # -- UNIFORMS
        status = ctypes.c_long(-1)
        glGetProgramiv(program, GL_ACTIVE_UNIFORMS, status)
        length = ctypes.c_long(-1)
        glGetProgramiv(program, GL_ACTIVE_UNIFORM_MAX_LENGTH, length)
        
        # for i in range(length.value):
        #     name_buffer = ctypes.create_string_buffer(str(status.value))
        #     size = GLint()
        #     type = GLenum()
        #     glGetActiveUniform(program, i, length.value, None, size, type, name_buffer.value)
        #     print(f"Uniform {i}: {name_buffer.value}")
        
        location_textureSampler = glGetUniformLocation(program, b"textureSampler")
        glUniform1i(location_textureSampler, 0) # Change which texture is bound based on block face and normal?
        
        # Get uniform locations
        ctypes.c_char_p("".encode('utf-8'))
        location_lightPos = glGetUniformLocation(program, b"lightPosition")
        location_Ld = glGetUniformLocation(program, b"Ld")
        location_MVP = glGetUniformLocation(program, b"MVP")
        location_normalMatrix = glGetUniformLocation(program, b"normalMatrix")
        
        # Upload light position
        glUniform4f(location_lightPos, 0.0, 50.0, 0.0, 1.0)

        # Upload light intensity
        glUniform3f(location_Ld, 1000.0, 0.0, 0.0)

        # Upload Transformation Matrices
        MVP_matrix = [1.0 if i % 5 == 0 else 0.0 for i in range(16)]
        modelView_matrix = MVP_matrix
        normal_matrix = [1.0 if i % 4 == 0 else 0.0 for i in range(9)]

        glUniformMatrix4fv(location_MVP, 1, GL_FALSE, (GLfloat * 16)(*MVP_matrix))
        glUniformMatrix3fv(location_normalMatrix, 1, GL_FALSE, (GLfloat * 9)(*normal_matrix))
        
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
        
        glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, 0)
        
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

# ------------------
