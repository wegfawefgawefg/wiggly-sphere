from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)

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
    glutSolidSphere(0.5, 30, 30)
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
