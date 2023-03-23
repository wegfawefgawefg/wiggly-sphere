import pyglet
from pyglet.gl import *

# Define the dimensions of our voxel grid
VOXEL_DIMENSIONS = (16, 16, 16)

# Define the size of each voxel in our grid
VOXEL_SIZE = 10

# Define the colors to use for each voxel type
VOXEL_COLORS = {
    0: (0, 0, 0),  # air
    1: (255, 0, 0),  # red
    2: (0, 255, 0),  # green
    3: (0, 0, 255),  # blue
}

# Define the voxel data for our grid
voxels = [
    [
        [1 if (x + y + z) % 2 == 0 else 2 for z in range(VOXEL_DIMENSIONS[2])]
        for y in range(VOXEL_DIMENSIONS[1])
    ]
    for x in range(VOXEL_DIMENSIONS[0])
]


# Define the function to draw a single voxel
def draw_voxel(x, y, z, voxel_type):
    # Get the color for this voxel type
    color = VOXEL_COLORS.get(voxel_type, (255, 255, 255))

    # Set the color for the voxel
    glColor3ub(*color)

    # Calculate the position of the voxel in 3D space
    x_pos = x * VOXEL_SIZE
    y_pos = y * VOXEL_SIZE
    z_pos = z * VOXEL_SIZE

    # Draw the six faces of the voxel
    glBegin(GL_QUADS)

    # Front face
    glVertex3f(x_pos, y_pos, z_pos)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos, z_pos)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos + VOXEL_SIZE, z_pos)
    glVertex3f(x_pos, y_pos + VOXEL_SIZE, z_pos)

    # Back face
    glVertex3f(x_pos, y_pos, z_pos + VOXEL_SIZE)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos, z_pos + VOXEL_SIZE)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos + VOXEL_SIZE, z_pos + VOXEL_SIZE)
    glVertex3f(x_pos, y_pos + VOXEL_SIZE, z_pos + VOXEL_SIZE)

    # Top face
    glVertex3f(x_pos, y_pos + VOXEL_SIZE, z_pos)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos + VOXEL_SIZE, z_pos)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos + VOXEL_SIZE, z_pos + VOXEL_SIZE)
    glVertex3f(x_pos, y_pos + VOXEL_SIZE, z_pos + VOXEL_SIZE)

    # Bottom face
    glVertex3f(x_pos, y_pos, z_pos)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos, z_pos)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos, z_pos + VOXEL_SIZE)
    glVertex3f(x_pos, y_pos, z_pos + VOXEL_SIZE)

    # Left face
    glVertex3f(x_pos, y_pos, z_pos)
    glVertex3f(x_pos, y_pos, z_pos + VOXEL_SIZE)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos, z_pos + VOXEL_SIZE)

    glVertex3f(x_pos + VOXEL_SIZE, y_pos, z_pos)

    # Right face
    glVertex3f(x_pos, y_pos, z_pos + VOXEL_SIZE)
    glVertex3f(x_pos, y_pos + VOXEL_SIZE, z_pos + VOXEL_SIZE)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos + VOXEL_SIZE, z_pos + VOXEL_SIZE)
    glVertex3f(x_pos + VOXEL_SIZE, y_pos, z_pos + VOXEL_SIZE)

    glEnd()


def draw_voxel_grid():
    # Loop through all the voxels in the grid and draw them
    for x in range(VOXEL_DIMENSIONS[0]):
        for y in range(VOXEL_DIMENSIONS[1]):
            for z in range(VOXEL_DIMENSIONS[2]):
                draw_voxel(x, y, z, voxels[x][y][z])


class Camera:
    def __init__(self):
        self.pos = [0, 0, 0]
        self.vel = [0, 0, 0]


cam = Camera()
window = pyglet.window.Window(resizable=True)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)


@window.event
def on_draw():
    # Clear the window and set the projection matrix
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, window.width / window.height, 0.1, 1000)

    # Set the modelview matrix and draw the voxel grid
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(cam.pos[0], cam.pos[1], cam.pos[2], 5, 5, 5, 0, 1, 0)
    # gluLookAt(5, 5, -20, 5, 5, 5, 0, 1, 0)
    draw_voxel_grid()


# wasd to move cam continuously
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.W:
        cam.pos[2] += 1
    if symbol == pyglet.window.key.S:
        cam.pos[2] -= 1
    if symbol == pyglet.window.key.A:
        cam.pos[0] -= 1
    if symbol == pyglet.window.key.D:
        cam.pos[0] += 1


pyglet.app.run()
