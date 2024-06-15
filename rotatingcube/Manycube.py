import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

def generate_random_colors():
    return [(random.random(), random.random(), random.random()) for _ in range(6)]

def set_vertices(max_distance):    
    x_value_change = random.randrange(-10, 10)
    y_value_change = random.randrange(-10, 10)
    z_value_change = random.randrange(-1 * max_distance, -20)

    new_vertices = []

    for vert in vertices:
        new_vert = []
        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change
        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)
        new_vertices.append(new_vert)

    return new_vertices, generate_random_colors()

def Cube(vertices, colors):
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(colors[i % len(colors)])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((1, 1, 1))  # White for the edges
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(random.randrange(-5, 5), random.randrange(-5, 5), -40)

    max_distance = 100
    cube_dict = {}

    for x in range(20):
        cube_dict[x] = set_vertices(max_distance)

    x_move = 0
    y_move = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = 0.3
                if event.key == pygame.K_RIGHT:
                    x_move = -0.3
                if event.key == pygame.K_UP:
                    y_move = -0.3
                if event.key == pygame.K_DOWN:
                    y_move = 0.3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glTranslatef(x_move, y_move, 0.50)

        for each_cube in cube_dict:
            vertices, colors = cube_dict[each_cube]
            Cube(vertices, colors)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
