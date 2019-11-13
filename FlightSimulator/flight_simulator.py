import pygame
from pygame.locals import *
from OpenGL import GL as gl, GLUT as glut
from OpenGL.GLU import *

import random
from FlightSimulator.noise import perlinNoise






vertices = (
    (1, -2, -1),  # node1
    (1, 1, -1),  # node2
    (-1, 1, -1),  # node3
    (-1, -1, -1),  # node4
    (1, -1, 1),  # node5
    (1, 1, 1),  # node6
    (-1, 1, 1),  # node7
    (-1, -1, 1)  # node8
)

# Connections
edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 6),
    (5, 1),
    (5, 4),
    (5, 6),
    (7, 3),
    (7, 4),
    (7, 6),
)

surfaces = (
    (0, 1, 2, 3),
    (0, 1, 5, 4),
    (0, 3, 7, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (4, 5, 6, 7),
)

colors = (
    (1, 1, 1),  # white
    (1, 1, 0),  # yellow
    (1, 0, 1),  # magenta
    (1, 0, 0),  # red
    (0, 1, 1),  # cyan
    (0, 1, 0),  # green
    (0, 0, 1),  # blue
    (0, 0, 0),  # black
)


def Lights():

    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glEnable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_LIGHT0)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, (0.9, 0.2, 0.2, 1.0))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, (0.0, 40.0, 10.0, 10.0))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, (1, 1, 1, 1))
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, (1, 0, 0, 1))


def Cube():
    gl.glBegin(gl.GL_QUADS)
    bool = True
    for surface in surfaces:

        x = 0
        for vertex in surface:
            if bool:
                x += 1
                if x == 6:
                    bool = False
            else:
                x += 1
            #glColor3fv(colors[x])
            gl.glVertex3fv(vertices[vertex])

    gl.glEnd()

    gl.glBegin(gl.GL_LINES)
    for edge in edges:
        for vertex in edge:
            gl.glColor((0, 0, 0))
            gl.glVertex3fv(vertices[vertex])

    gl.glEnd()

noise = perlinNoise(32 * 3, 32 * 3, 255, 32)
noise.randomize()
lines_grid = noise.smoothNoise2D(smoothing_passes=5)

def Terrain():

    gl.glTranslate(0,0,0)

    mod = 8
    z = -1.0
    for lines in lines_grid:
        gl.glBegin(gl.GL_LINE_STRIP)
        x = 0.0
        z += 1.0
        for y in lines:
            y *= mod
            gl.glVertex3f(x, y, z)
            x += 1.0
        gl.glEnd()



width = 800
height = 600

def InitGL(Width, Height):
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    gl.glClearDepth(1.0)
    gl.glDepthFunc(gl.GL_LESS)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glPerspective(45.0, float(Width) / float(Height), 0.1, 50.0)
    gl.glTranslatef(0.0, -6.0, -45.0)
    gl.glRotatef(0.0, 0.0, 0.0, 0.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)


def InitGLUT(Width, Height, WindowName):
    gl.glutInit(gl.sys.argv)
    gl.glutInitDisplayMode(gl.GLUT_RGBA | gl.GLUT_DOUBLE | gl.GLUT_DEPTH)
    gl.glutInitWindowSize(Width, Height)
    gl.glutCreateWindow(WindowName)
    gl.glutDisplayFunc(Draw)
    gl.glutIdleFunc(Draw)
    gl.glutReshapeFunc(Reshape)
    gl.glutKeyboardFunc(Key)
    gl.glutKeyboardUpFunc(KeyUp)
    gl.glutSpecialFunc(Special)
    gl.glutSpecialUpFunc(SpecialUp)

def main():
    #pygame.init()
    display = (width * 2, height * 2)
    #pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # DOUBLEBUF = BUFFER



    gluPerspective(45, (display[0] / display[1]), 0.1,
                   1000.0)  # FOV, ASPECT RATIO, CLIPPING PLANE NEAR, CLIPPING PLANE FAR
    gl.glTranslate(0.0, 0.0, -10)
    gl.glRotatef(0, 0, 0, 0)

    rotate_right = False
    rotate_left = False
    turn_right = False
    turn_left = False
    ascend = False
    descend = False
    forward = False
    backward = False


    # glEnable(GL_LINE_SMOOTH)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # KEY PRESSED
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    rotate_left = True

                if event.key == pygame.K_e:
                    rotate_right = True

                if event.key == pygame.K_a:
                    turn_left = True

                if event.key == pygame.K_d:
                    turn_right = True

                if event.key == pygame.K_SPACE:
                    ascend = True

                if event.key == pygame.K_LSHIFT:
                    descend = True

                if event.key == pygame.K_w:
                    forward = True

                if event.key == pygame.K_s:
                    backward = True

            # KEY RELEASED
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_q:
                    rotate_left = False

                if event.key == pygame.K_e:
                    rotate_right = False

                if event.key == pygame.K_a:
                    turn_left = False

                if event.key == pygame.K_d:
                    turn_right = False

                if event.key == pygame.K_SPACE:
                    ascend = False

                if event.key == pygame.K_LSHIFT:
                    descend = False

                if event.key == pygame.K_w:
                    forward = False

                if event.key == pygame.K_s:
                    backward = False

        if rotate_left:
            gl.glRotate(1, 0, 0, 1)

        if rotate_right:
            gl.glRotate(1, 0, 0, -1)

        if turn_left:
            gl.glRotate(1, 0, 1, 0)

        if turn_right:
            gl.glRotate(1, 0, -1, 0)

        if ascend:
            gl.glTranslate(0, -0.1, 0)

        if descend:
            gl.glTranslate(0, 0.1, 0)

        if forward:
            gl.glTranslate(0, 0, -0.1)

        if backward:
            gl.glTranslate(0, 0, 0.1)

        # glRotatef(1, 1, 1, 1)  # Give value between 0-1



        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        Lights()
        Terrain()
        #glPolygonMode(GL_FRONT, GL_LINE)
        #glPolygonMode(GL_BACK, GL_LINE)

        Cube()
        #glPolygonMode(GL_FRONT, GL_FILL)
        #glPolygonMode(GL_BACK, GL_FILL)
        #pygame.display.flip()  # Update display
        #pygame.time.wait(10)
        gl.InitGLUT(1200, 1024, 'TERRAIN')
        gl.InitGL(1200, 1024)

        if "-info" in gl.sys.argv:
            print("GL_RENDERER   = ", gl.glGetString(gl.GL_RENDERER))
            print("GL_VERSION    = ", gl.glGetString(gl.GL_VERSION))
            print("GL_VENDOR     = ", gl.glGetString(gl.GL_VENDOR))

        gl.glutMainLoop()


if __name__ == "__main__":
    main()

