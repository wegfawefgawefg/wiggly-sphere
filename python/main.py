import ctypes
import os
import platform
import sys
from collections import namedtuple

import glm
import numpy as np
from glfw import _GLFWwindow as GLFWwindow
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

Sphere = namedtuple("Sphere", "vertices indices")
WINDOW_DIMS = glm.vec2(1200, 800)


class Camera:
    def __init__(self):
        self.pos = glm.vec3(0.0, 0.0, 2.0)
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)


firstMouse = True
yaw = (
    -90.0
)  # yaw is initialized to -90.0 degrees since a yaw of 0.0 results in a direction vector pointing to the right so we initially rotate a bit to the left.
pitch = 0.0
lastX = 800.0 / 2.0
lastY = 600.0 / 2.0
fov = 90.0

# timing
deltaTime = 0.0  # time between current frame and last frame
lastFrame = 0.0

cam = Camera()


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

            # vertices.append([x, y, z])
            vertices.append(glm.vec3(x, y, z))

    for lat_idx in range(num_latitudes):
        for long_idx in range(num_longitudes):
            first = lat_idx * (num_longitudes + 1) + long_idx
            second = first + num_longitudes + 1

            # indices.append([first, second, first + 1])
            # indices.append([second, second + 1, first + 1])
            indices.append(glm.uvec3(first, second, first + 1))
            indices.append(glm.uvec3(second, second + 1, first + 1))
    return Sphere(vertices, indices)


def wiggle(vertices, center, magnitude):
    time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    wiggled_vertices = []
    for vertex in vertices:
        direction = np.array(vertex) - np.array(center)
        distance = np.linalg.norm(direction)
        # displacement = magnitude * np.random.uniform(-1, 1)
        displacement = magnitude * np.sin(vertex.z * 5 + time * 3)
        wiggled_vertex = vertex + (direction / distance) * displacement
        wiggled_vertices.append(wiggled_vertex)
    return np.array(wiggled_vertices).tolist()


sphere = sphere(radius=0.5, num_latitudes=10, num_longitudes=10)


def main() -> int:
    global deltaTime, lastFrame

    glfwInit()
    # glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    # glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    # glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
    print("GLFW version: ", glfwGetVersionString())
    print("OpenGL version: ", glGetString(GL_VERSION))

    window = glfwCreateWindow(
        int(WINDOW_DIMS.x), int(WINDOW_DIMS.y), "Wiggly Sphere", None, None
    )
    if window == None:

        print("Failed to create GLFW window")
        glfwTerminate()
        return -1

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback)
    glfwSetCursorPosCallback(window, mouse_callback)
    glfwSetScrollCallback(window, scroll_callback)

    # glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)  # capture mouse

    glEnable(GL_DEPTH_TEST)

    while not glfwWindowShouldClose(window):
        currentFrame = glfwGetTime()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame

        processInput(window)

        # render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fov, WINDOW_DIMS.x / WINDOW_DIMS.y, 0.1, 1000)
        gluLookAt(
            cam.pos.x,
            cam.pos.y,
            cam.pos.z,
            cam.front.x,
            cam.front.y,
            cam.front.z,
            cam.up.x,
            cam.up.y,
            cam.up.z,
        )

        light_ambient = [0.0, 0.0, 0.0, 0.0]
        light_diffuse = [5.0, 1.0, 1.0, 1.0]
        light_specular = [5.0, 1.0, 1.0, 1.0]
        light_position = [1.0, 1.0, 1.0, 0.0]
        # make the light spin around the origin
        light_position = glm.rotate(
            glm.mat4(1.0), glm.radians(glfwGetTime() * 500), glm.vec3(0, 1, 0)
        ) * glm.vec4(light_position[0], light_position[1], light_position[2], 1.0)
        light_position = light_position.xyz.to_tuple()

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

        # glShadeModel(GL_SMOOTH)
        # calculate normals
        normals = []
        for triangle in sphere.indices:
            v1 = sphere.vertices[triangle[0]]
            v2 = sphere.vertices[triangle[1]]
            v3 = sphere.vertices[triangle[2]]
            normal = glm.cross(v2 - v1, v3 - v1)
            normals.append(normal.to_list())
            normals.append(normal.to_list())
            normals.append(normal.to_list())

        glNormalPointer(GL_FLOAT, 0, normals)
        glEnableClientState(GL_NORMAL_ARRAY)

        # its not using the normals
        # fix by using glNormal3f

        # mutate verts
        verts = wiggle(sphere.vertices, [0, 0, 0], 0.1)

        # render
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_TRIANGLES)
        for triangle in sphere.indices:
            for vertex_idx in triangle:
                glVertex3fv(verts[vertex_idx])
                # calculate normal
                v1 = sphere.vertices[triangle[0]]
                v2 = sphere.vertices[triangle[1]]
                v3 = sphere.vertices[triangle[2]]
                normal = glm.cross(v2 - v1, v3 - v1)
                glNormal3f(*normal.to_list())
                # glNormal3f(*normals[vertex_idx])
        glEnd()
        glFlush()

        glfwSwapBuffers(window)
        glfwPollEvents()

    glfwTerminate()
    return 0


def processInput(window: GLFWwindow) -> None:
    global cam

    if glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
        glfwSetWindowShouldClose(window, True)

    cameraSpeed = 2.5 * deltaTime
    if glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS:
        cam.pos += cameraSpeed * cam.front
    if glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS:
        cam.pos -= cameraSpeed * cam.front
    if glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS:
        cam.pos -= glm.normalize(glm.cross(cam.front, cam.up)) * cameraSpeed
    if glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS:
        cam.pos += glm.normalize(glm.cross(cam.front, cam.up)) * cameraSpeed


def framebuffer_size_callback(window: GLFWwindow, width: int, height: int) -> None:
    # make sure the viewport matches the new window dimensions note that width and
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)


def mouse_callback(window: GLFWwindow, xpos: float, ypos: float) -> None:
    global cam, lastX, lastY, firstMouse, yaw, pitch

    if firstMouse:

        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos  # reversed since y-coordinates go from bottom to top
    lastX = xpos
    lastY = ypos

    sensitivity = 0.1  # change this value to your liking
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset

    # make sure that when pitch is out of bounds, screen doesn't get flipped
    if pitch > 89.0:
        pitch = 89.0
    if pitch < -89.0:
        pitch = -89.0

    front = glm.vec3()
    front.x = glm.cos(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    front.y = glm.sin(glm.radians(pitch))
    front.z = glm.sin(glm.radians(yaw)) * glm.cos(glm.radians(pitch))
    cam.front = glm.normalize(front)


def scroll_callback(window: GLFWwindow, xoffset: float, yoffset: float) -> None:
    global fov

    fov -= yoffset
    if fov < 1.0:
        fov = 1.0
    if fov > 120.0:
        fov = 120.0


main()
