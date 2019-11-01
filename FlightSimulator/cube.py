import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

vertices = (
    (1, -1, -1),  # node1
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


def Cube():
    glBegin(GL_QUADS)
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
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])

    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor((0,0,0))
            glVertex3fv(vertices[vertex])

    glEnd()


def main():
    pygame.init()
    display = (800*2, 600*2)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # DOUBLEBUF = BUFFER

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # FOV, ASPECT RATIO, CLIPPING PLANE
    glTranslate(0.0, 0.0, -10)
    glRotatef(0, 0, 0, 0)

    rotate_right = False
    rotate_left = False
    turn_right = False
    turn_left = False
    ascend = False
    descend = False

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

        if rotate_left:
            glRotate(1, 0, 0, 1)

        if rotate_right:
            glRotate(1, 0, 0, -1)

        if turn_left:
            glRotate(1, 0, 1, 0)

        if turn_right:
            glRotate(1, 0, -1, 0)

        glTranslate(0, 0, -0.0e1)

        #glRotatef(1, 1, 1, 1)  # Give value between 0-1



        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()  # Update display
        pygame.time.wait(10)


main()
