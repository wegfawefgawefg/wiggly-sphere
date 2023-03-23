from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glutSolidSphere(0.5, 30, 30)
    glFlush()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 800)
glutInitWindowPosition(100, 100)
glutCreateWindow("Sphere")
glutDisplayFunc(display)
glEnable(GL_DEPTH_TEST)
glClearColor(0.0, 0.0, 0.0, 0.0)
glutMainLoop()
