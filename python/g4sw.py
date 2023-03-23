import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
import pyglet
from pyglet.gl import *


def generate_sphere(radius, num_latitudes, num_longitudes):
    vertices = []
    indices = []

    for lat_idx in range(num_latitudes + 1):
        theta = lat_idx * np.pi / num_latitudes
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)

        for long_idx in range(num_longitudes + 1):
            phi = long_idx * 2 * np.pi / num_longitudes
            sin_phi = np.sin(phi)
            cos_phi = np.cos(phi)

            x = radius * sin_theta * cos_phi
            y = radius * sin_theta * sin_phi
            z = radius * cos_theta

            vertices.append([x, y, z])

    for lat_idx in range(num_latitudes):
        for long_idx in range(num_longitudes):
            first = lat_idx * (num_longitudes + 1) + long_idx
            second = first + num_longitudes + 1

            indices.append([first, second, first + 1])
            indices.append([second, second + 1, first + 1])

    return np.array(vertices), np.array(indices, dtype=np.uint32)


def wiggle_vertices(vertices, center, magnitude):
    wiggled_vertices = []
    for vertex in vertices:
        direction = np.array(vertex) - np.array(center)
        distance = np.linalg.norm(direction)
        displacement = magnitude * np.random.uniform(-1, 1)
        wiggled_vertex = vertex + (direction / distance) * displacement
        wiggled_vertices.append(wiggled_vertex)
    return np.array(wiggled_vertices)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 1, 0)

    vertices, indices = generate_sphere(radius=1, num_latitudes=20, num_longitudes=20)
    wiggled_vertices = wiggle_vertices(vertices, center=[0, 0, 0], magnitude=0.1)

    glBegin(GL_TRIANGLES)
    for triangle in indices:
        for vertex_idx in triangle:
            glVertex3fv(wiggled_vertices[vertex_idx])
    glEnd()

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)


def init_gl():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Wiggled Sphere")

    init_gl()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(glutPostRedisplay)

    glutMainLoop()


if __name__ == "__main__":
    main()
