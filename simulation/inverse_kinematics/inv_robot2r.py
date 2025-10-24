
"""
Program: inverse_onearm.py
Description:
    Shows how a 2R robotic arm follows a bullet moved by the mouse.
    The text in the graph indicates mouse coordinates and robot angles (q1 and q2).
    The frame updates continuously (≈60 FPS) without depending on the mouse movement.
Requirements:
    pip install matplotlib
"""

import matplotlib.pyplot as plt
import math
import sys

sys.path.insert(0, "../objects") # add folder "objects" path to search list for importing its modules

from robot2r import Robot2r
from bullet import Bullet

# ==============================================================
# Create a bullet
# ==============================================================
bullet = Bullet(x0=5, y0=5, color='black', max_step=0.1)

# ==============================================================
# Create a robot
# ==============================================================
robot = Robot2r(3,2,0,0)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal', 'box')
ax.set_title('Robot follows the mouse')

(lines,) = ax.plot([], [], lw=4, marker='o', color="#0077cc", markersize=6)
(end_dot,) = ax.plot([], [], 'o', color='red', markersize=8)

point, = ax.plot([], [], 'o', color=bullet.color, markersize=8)


# Create a text to show data
text_info = ax.text(-9.5, 9, "", fontsize=10, color='blue', va='top')

# Global variables
mouse_pos = (1.0, 1.0)

# Save mouse position
def on_move(event):
    global mouse_pos
    if event.inaxes is not None:
        mouse_pos = (event.xdata, event.ydata)

# Connect mouse event
fig.canvas.mpl_connect('motion_notify_event', on_move)

# Continuous update function
def update_frame():

    # Actualizar bola
    x, y = mouse_pos
    bullet.move2pos(x,y)
    
    # Move the robot    
    robot.move2point((x,y))
    
    # Robot coordinates
    x_points,y_points = robot.robotCoordinates()

    # Print the robot
    lines.set_data(x_points, y_points)
    end_dot.set_data([x_points[-1]], [y_points[-1]])

    # Update text
    text_info.set_text(f"Mouse: ({x:.2f}, {y:.2f}), Robot q1: {math.degrees(robot.q1):.2f}, Robot q2: {math.degrees(robot.q2):.2f}")
    
    # Print the bullet
    point.set_data([x], [y])

    # Redrawn
    fig.canvas.draw_idle()

# Timer for updating ≈60 times per second (interval=16)
timer = fig.canvas.new_timer(interval=16)
timer.add_callback(update_frame)
timer.start()

plt.show()
