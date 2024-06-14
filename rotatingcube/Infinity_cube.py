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

colors = (
    (0, 1, 1),    # Cyan
    (1, 1, 1),    # White
    (0, 1, 1),    # Cyan
    (0, 1, 1),    # Cyan
    (0.5, 0, 0.5) # Lighter Purple
)

def set_vertices(max_distance, start_x, start_y):
    x_value_change = random.randrange(-10, 10)
    y_value_change = random.randrange(-10, 10)
    z_value_change = random.randrange(-1 * max_distance, -20)

    new_vertices = []

    for vert in vertices:
        new_vert = []
        new_x = vert[0] + x_value_change + start_x
        new_y = vert[1] + y_value_change + start_y
        new_z = vert[2] + z_value_change
        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)
        new_vertices.append(new_vert)

    return new_vertices

def Cube(vertices):
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
            x += 1
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    max_distance = 100
    gluPerspective(45, (display[0] / display[1]), 0.1, max_distance)

    glTranslatef(0, 0, -40)

    x_move = 0
    y_move = 0
    cur_x = 0
    cur_y = 0
    game_speed = 2
    direction_speed = 2

    cube_dict = {}

    for x in range(50):
        cube_dict[x] = set_vertices(max_distance, cur_x, cur_y)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = direction_speed
                if event.key == pygame.K_RIGHT:
                    x_move = -1 * direction_speed
                if event.key == pygame.K_UP:
                    y_move = -1 * direction_speed
                if event.key == pygame.K_DOWN:
                    y_move = direction_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_move = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_move = 0

      
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glTranslatef(x_move, y_move, game_speed)

        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])

        
        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        camera_z = x[3][2]

        for each_cube in cube_dict:
            if cube_dict[each_cube][0][2] >= camera_z:
                new_max = int(-1 * (camera_z - (max_distance * 2)))
                cube_dict[each_cube] = set_vertices(new_max, cur_x, cur_y)

        pygame.display.flip()

if __name__ == "__main__":
    main()
