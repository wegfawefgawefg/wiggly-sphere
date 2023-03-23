import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define your voxel data here (1 represents a filled voxel, 0 represents an empty voxel)
# voxel_data = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]]]


def generate_sphere(center_x, center_y, center_z, radius):
    sphere = []
    for x in range(center_x - radius, center_x + radius + 1):
        row = []
        for y in range(center_y - radius, center_y + radius + 1):
            column = []
            for z in range(center_z - radius, center_z + radius + 1):
                if (x - center_x) ** 2 + (y - center_y) ** 2 + (
                    z - center_z
                ) ** 2 <= radius**2:
                    column.append(1)
                else:
                    column.append(0)
            row.append(column)
        sphere.append(row)
    return sphere


voxel_data = generate_sphere(5, 5, 5, 5)


def draw_voxels():
    for x, plane in enumerate(voxel_data):
        for y, row in enumerate(plane):
            for z, voxel in enumerate(row):
                if voxel:
                    draw_cube(x, y, z)


def draw_cube(x, y, z):
    vertices = [
        (x, y, z),
        (x + 1, y, z),
        (x + 1, y + 1, z),
        (x, y + 1, z),
        (x, y, z + 1),
        (x + 1, y, z + 1),
        (x + 1, y + 1, z + 1),
        (x, y + 1, z + 1),
    ]

    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(90, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-1.0, -1.0, -5)
    pygame.mouse.get_rel()  # call this once to reset the relative mouse position

    camera_speed = 0.1
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            glTranslatef(0, 0, camera_speed)
        if keys[pygame.K_s]:
            glTranslatef(0, 0, -camera_speed)
        if keys[pygame.K_a]:
            glTranslatef(camera_speed, 0, 0)
        if keys[pygame.K_d]:
            glTranslatef(-camera_speed, 0, 0)
        if keys[pygame.K_q]:
            glTranslatef(0, -camera_speed, 0)
        if keys[pygame.K_e]:
            glTranslatef(0, camera_speed, 0)

        x, y = pygame.mouse.get_rel()
        mouserotscale = 0.1
        x, y = x * mouserotscale, y * mouserotscale
        glRotatef(x, 0, 1, 0)
        glRotatef(y, 1, 0, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_voxels()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
