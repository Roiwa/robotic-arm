"""
Program: excavator.py
Description:
    Controls a 2R robotic arm in cartesian way (x and y) using
    "up", "down", "left", and "right" keys. To do so, it uses 
    an analytical approach for inverse kinematics. The frame 
    updates continuously (≈60 FPS) without depending on the mouse movement.
Possibilities:
    Robot configuration can be changed. Be careful to not exceed the limits of the canvas
Requirements:
    pip install matplotlib
    robot2r library
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import sys
sys.path.insert(0, "../objects") # add folder "objects" path to search list for importing its modules

from robot2r import Robot2r

# Create the robot
robot = Robot2r(10,10,0,0)

# Create figure and axis
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_aspect('equal')
ax.set_title("Controlling Robot with Keyboard")
ax.grid(True, linestyle='--', alpha=0.5)

(lines,) = ax.plot([], [], lw=4, marker='o', color="#0077cc", markersize=6)
(end_dot,) = ax.plot([], [], 'o', color='red', markersize=8)

# Create a ball
radio = 0.25
ball = plt.Circle((0, 0), radio, color='green')
ball.radius
ax.add_patch(ball)

# Position and speed variables
pos_x, pos_y = 0, 0
vx, vy = 0, 0
speed = 0.3

# Manage pressed keys
def on_key_press(event):
    global vx, vy
    if event.key == 'left':
        vx = -speed
    elif event.key == 'right':
        vx = speed
    elif event.key == 'up':
        vy = speed
    elif event.key == 'down':
        vy = -speed

# Manage released keys
def on_key_release(event):
    global vx, vy
    if event.key in ['left', 'right']:
        vx = 0
    elif event.key in ['up', 'down']:
        vy = 0

# Update animation (≈60 FPS)
def actualizar(frame):
    global pos_x, pos_y, vx, vy
    pos_x += vx
    pos_y += vy
    
    # Move robot    
    robot.move2point((pos_x,pos_y))
    
    # Robot coordinates
    x_points,y_points = robot.robotCoordinates()

    # Print robot
    lines.set_data(x_points, y_points)
    end_dot.set_data([x_points[-1]], [y_points[-1]])

    # Movement limitation
    pos_x = max(-30 + radio, min(30 - radio, pos_x))
    pos_y = max(-30 + radio, min(30 - radio, pos_y))

    ball.center = (pos_x, pos_y)
    return ball, lines, end_dot

# Connect keyboard events
fig.canvas.mpl_connect('key_press_event', on_key_press)
fig.canvas.mpl_connect('key_release_event', on_key_release)

# Create animation (interval = 16 ms ≈ 60 FPS)
ani = animation.FuncAnimation(fig, actualizar, interval=16, blit=True)

plt.show()
