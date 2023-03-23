import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from collections import namedtuple

Sphere = namedtuple("Sphere", "vertices indices")
WINDOW_DIMS = np.array([800, 800])


def sphere(radius, num_latitudes, num_longitudes):
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
    return Sphere(vertices, indices)


sphere = sphere(radius=0.5, num_latitudes=10, num_longitudes=10)


def wiggle(vertices, center, magnitude):
    # time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    wiggled_vertices = []
    for vertex in vertices:
        direction = np.array(vertex) - np.array(center)
        distance = np.linalg.norm(direction)
        displacement = magnitude * np.random.uniform(-1, 1)
        wiggled_vertex = vertex + (direction / distance) * displacement
        wiggled_vertices.append(wiggled_vertex)
    return np.array(wiggled_vertices).tolist()


class Camera:
    def __init__(self):
        self.pos = [-10, -10, -10]
        self.vel = [0, 0, 0]


cam = Camera()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, WINDOW_DIMS[0] / WINDOW_DIMS[1], 0.1, 1000)

    # Set the modelview matrix and draw the voxel grid
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(cam.pos[0], cam.pos[1], cam.pos[2], 0, 0, 0, 0, 1, 0)

    light_ambient = [0.0, 0.0, 0.0, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    light_position = [1.0, 1.0, 1.0, 0.0]

    mat_ambient = [0.7, 0.7, 0.7, 1.0]
    mat_diffuse = [0.8, 0.8, 0.8, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    high_shininess = [100.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

    verts = wiggle(sphere.vertices, [0, 0, 0], 0.4)

    # render as wireframe
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_TRIANGLES)
    for triangle in sphere.indices:
        for vertex_idx in triangle:
            glVertex3fv(sphere.vertices[vertex_idx])
    glEnd()

    glDisable(GL_LIGHTING)
    glFlush()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 800)
glutInitWindowPosition(100, 100)
glutCreateWindow("Sphere")
glutDisplayFunc(display)
glClearColor(0.0, 0.0, 0.0, 0.0)
glutMainLoop()
