
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial
import math
import numpy as np

import sys
sys.path.insert(0, "../objects") # add folder "objects" path to search list for importing its modules

from robot2r import Robot2r

def interp_linear(point1, point2, x):
    """Lineal interpolation betwen (x1,y1) and (x2,y2)"""
    y = point1[1] + (point2[1] - point1[1]) * (x - point1[0]) / (point2[0] - point1[0])
    return [x,y]

def path_interp(path, n_nums):
    n_nums +=1
    new_path =[]
    print(path)
    for i,p in enumerate(path):
        if i == len(path)-1: #Circular buffer
            p_next =path[0]
        else:
            p_next = path[i+1]
        #new_path.append(path_prev)
        xs = np.linspace(p[0], p_next[0], n_nums)
        for xi in xs[:-1]:
            new_path.append(interp_linear(p,p_next, xi))
        
    return new_path

def checkValue(jointValue,linkNumber):

    #if jointValue.isdigit():
    val_int = int(jointValue)
    
    #transformation for servo angle in link 2
    if linkNumber == 2:
        #val_int = 180 + val_int 
        val_int = -val_int

    message = f"{int(linkNumber)},{val_int}\n"
    arduino.write(message.encode('utf-8'))  # Send value with line break
    print(f"Sent: {val_int}")

# Create the robot
print("Creating the Robot...")
robot = Robot2r(10,10,90,-30)
print("Robot created!")

# Create figure and axis
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_aspect('equal')
ax.set_title("Controlling Robot with Keyboard")
ax.grid(True, linestyle='--', alpha=0.5)

(lines,) = ax.plot([], [], lw=4, marker='o', color="#0077cc", markersize=6)
(end_dot,) = ax.plot([], [], 'o', color='red', markersize=8)


### Create the path
path = [
    [5,10],
    [7,5],
    [11,5],
    [13,10],
    [9,15]
]

new_path = path_interp(path,5)
new_path = path
counter = 0
# Update animation (≈60 FPS)
def actualizar(frame):
    global counter
    time.sleep(5)
    
    point = new_path[counter]
    
    # Move robot    
    robot.move2point((point[0],point[1]))
    
    q1 = math.degrees(robot.links[0].theta)
    q2 = math.degrees(robot.links[1].theta)
    print(f"pos: {point[0],point[1]}, q1 = {q1:.2f}, q2 = {q2:.2f}")
    
    # Robot coordinates
    x_points,y_points = robot.robotCoordinates()
    print(f"\t link {1}: [{x_points[0]:.2f}, {y_points[0]:.2f}]")
    print(f"\t link {2}: [{x_points[1]:.2f}, {y_points[1]:.2f}]")

    # Print robot
    lines.set_data(x_points, y_points)
    end_dot.set_data([x_points[-1]], [y_points[-1]])

    # Movement limitation
    pos_x = max(-30, 30)
    pos_y = max(-30, 30)
    
    if counter< len(new_path)-1:
        counter +=1
    else:
        counter = 0
    
    
    return lines, end_dot


# Create animation (interval = 16 ms ≈ 60 FPS)
ani = animation.FuncAnimation(fig, actualizar, interval=16, blit=True)

plt.show()

