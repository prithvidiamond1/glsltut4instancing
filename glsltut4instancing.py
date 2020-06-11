
import numpy as np
import time

import moderngl
import glfw
from glfw import GLFW

import glm

enable_query = False

glfw.init()

# setting context flags
glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
glfw.window_hint(glfw.RESIZABLE, True)
glfw.window_hint(glfw.DOUBLEBUFFER, True)
glfw.window_hint(glfw.DEPTH_BITS, 24)
glfw.window_hint(glfw.SAMPLES, 8)  # For MSAA*x where x is the integer > 0

width, height = 1920, 1080
window = glfw.create_window(width, height, 'GLSLtut', None, None)

glfw.make_context_current(window)

ctx = moderngl.create_context(require=330)

def window_quit(window, key, scancode, action, mods):
    if key == GLFW.GLFW_KEY_ESCAPE and action == GLFW.GLFW_PRESS:
        glfw.set_window_should_close(window, GLFW.GLFW_TRUE)

def window_resize(window, w, h):
    projection1 = np.array(glm.perspective(45.0, float(w/(h+0.00001)), 2.0, 200.0), 'f4')
    prog1['projection'].write(projection1)
    ctx.viewport = (0, 0, w, h)

glfw.set_key_callback(window, window_quit)
glfw.set_window_size_callback(window, window_resize)

glfw.swap_interval(1) # Toggles V-sync

prog1 = ctx.program(
    vertex_shader=open('prog1.vert', 'r').read(),
    fragment_shader=open('prog1.frag', 'r').read(),
)

cube_vertices = np.zeros(8, dtype=[('positions', 'f4', 3), ('colors', 'f4', 4),])  # 4 for no of vertices
cube_vertices['positions'] = (1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1)
cube_vertices['colors'] = (0, 1, 1, 1), (0, 0, 1, 1), (0, 0, 0, 1), (0, 1, 0, 1),(1, 1, 0, 1), (1, 1, 1, 1), (1, 0, 1, 1), (1, 0, 0, 1)

translations = []

for x in range(0, 101, 4):
    for y in range(0, 51, 4):
        for z in range(0, 51, 4):
        # for z in range(0, 4, 4):
            identity = np.eye(4, dtype='f4')
            translations.append(np.array(glm.translate(identity, np.array([x-50, y-25, z-25], 'f4'))))

translations = np.array(translations, 'f4')
instances = len(translations)
print('Total no of cubes =', instances)

indices = np.array([0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
                    1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5], dtype=np.uint32)

vbo1 = ctx.buffer(cube_vertices)
vbo2 = ctx.buffer(translations)
index_ibo = ctx.buffer(indices)

projection1 = np.array(glm.perspective(45.0, float(width/(height+0.00001)), 2.0, 200.0), 'f4')
view1 = np.eye(4, dtype='f4')
model1 = np.eye(4, dtype='f4')

# model1 = glm.translate(model1, np.array((-50, 20, 0), 'f4'))
view1 = glm.translate(view1, np.array((0, 0, -150), 'f4'))

prog1['projection'].write(projection1)
prog1['view'].write(view1)
prog1['model'].write(model1)

vao = ctx.vertex_array(prog1, ((vbo1, '3f 4f', 'position', 'color'), (vbo2, '16f/i', 'translation')), index_buffer=index_ibo)

theta = phi = 0

# ctx.enable(ctx.DEPTH_TEST) # for testing without culling

ctx.enable(ctx.DEPTH_TEST|ctx.CULL_FACE) # for testing with culling
ctx.cull_face = 'back'
ctx.front_face = 'ccw'

# Framerate measuring stuff
framerate_test = True

frames = 0
avg_frames, avg_count = 0, 1
init_time = start_time = time.time()

if enable_query:
    query = ctx.query(samples=True, time=True, primitives=True) # for quering info about no of samples, time elapsed and no of primitives

while not glfw.window_should_close(window):
    frames += 1

    ctx.screen.use()
    ctx.screen.clear(1.0, 1.0, 1.0, 1.0)
    
    theta = 0.02
    phi = 0.02

    # model1 = np.eye(4, dtype='f4')
    model1 = glm.rotate(model1, theta, np.array((0, 0, 1), 'f4'))
    model1 = glm.rotate(model1, phi, np.array((0, 1, 0), 'f4'))
    prog1['model'].write(model1)

    if enable_query:
        with query:
            vao.render(moderngl.TRIANGLES, instances=instances)
    else:
        vao.render(moderngl.TRIANGLES, instances=instances)

    glfw.swap_buffers(window)
    glfw.poll_events()

    if framerate_test:
        if time.time()-start_time >= 1:
            avg_frames = ((avg_count-1)*avg_frames + frames)*avg_count
            frames = 0
            start_time = time.time()
        if time.time()-init_time >= 60:
            print('Average Framerate =', avg_frames)
            if enable_query:
                print('samples =', query.samples)
                print('elapsed =', query.elapsed)
                print('primitives =', query.primitives)
            glfw.set_window_should_close(window, GLFW.GLFW_TRUE)

glfw.destroy_window(window)

