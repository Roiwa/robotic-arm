
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial
import math
import numpy as np

import sys
sys.path.insert(0, "../../simulation/objects") # add folder "objects" path to search list for importing its modules

from robot2r import Robot2r

# ==============================================================
# Configuration parameters
# ==============================================================
PORT = '/dev/ttyACM0'   # Change '/dev/ttyACM0' by the correct port of your system
BAUD = 9600             # Change by the baud rate of your configuration
path = [
    [5,10],
    [7,5],
    [11,5],
    [13,10],
    [9,15]
]

def initComms(port, baud_rate):
    """This fcn starts the serial communication

    Args:
        port (str): name of the port
        baud_rate (int): baud rate of the comms
    """
    serial_comm = serial.Serial(port, baud_rate)
    time.sleep(2)  # Waits until MCU restarts the connection
    
    # Reset buffers
    serial_comm.reset_input_buffer
    serial_comm.reset_output_buffer

    return serial_comm

def sendAngle(comms,jointAngle,linkNumber):
    """It sends to the MCU the servo and its angle 
    Args:
        comms (serial): object which manages the serial communications
        jointAngle (int): servo angle
        linkNumber (str): number of the link
    """
    
    message = f"{int(linkNumber)},{jointAngle}\n"
    comms.write(message.encode('utf-8'))  # Send value with line break
    print(f"Sent: {jointAngle}")
    

def checkJointValue(jointValue,linkNumber):
    """ If it is servo 2, we need to transform the angle. Also, we check 
        that the value of the joint is between the proper range.
    Args:
        jointValue (str): joint angle introduced by the user
        linkNumber (str): number of the link

    Returns:
        int: the servo angle in degrees
    """    
    #transformation to servo angle in link 2
    if linkNumber == "2":
        jointValue = -jointValue 
        
    if 0 <= jointValue <= 180:
        return jointValue
    else:
        print("Value must be between 0 and 180 in absolute value.")
        return None
    

def interp_linear(point1, point2, x):
    """Gives a new point using the linear interporlation of point1 and point2 and its x value

    Args:
        point1 (list): first point (x1,y1)
        point2 (list): second point (x2,y2)
        x (int): x value for the new point

    Returns:
        list: new point (x,y)
    """
    y = point1[1] + (point2[1] - point1[1]) * (x - point1[0]) / (point2[0] - point1[0])
    return [x,y]

def path_interp(path, n_nums):
    """ Increases the number of points of the current path using linear interpolation

    Args:
        path (list): a list of points of the current path
        n_nums (int): number of new points between each two consecutive points of the current path

    Returns:
        list: a list of points of the new path
    """
    n_nums +=1
    new_path =[]
    print(path)
    for i,p in enumerate(path):
        if i == len(path)-1: #Circular buffer
            p_next =path[0]
        else:
            p_next = path[i+1]
        xs = np.linspace(p[0], p_next[0], n_nums)
        for xi in xs[:-1]:
            new_path.append(interp_linear(p,p_next, xi))
        
    return new_path





counter = 0
# Update animation (≈60 FPS)
def update(frame,new_path,robot,comms,lines,end_dot):
    """Dynamics and graphical update

    Args:
        frame (frame): frame pic
        new_path (list): A list of points
        robot (robot): The robotic arm
        comms (serial): serial communication
        lines (list): links points
        end_dot (list): point of end effector

    Returns:
        list: the line list is the new links points, end_dot is the new point of end effector
    """
    global counter
    
    time.sleep(0.5)
    
    point = new_path[counter]
    
    # Move robot    
    robot.move2point((point[0],point[1]))
    
    q1 = math.degrees(robot.q1)
    q2 = math.degrees(robot.q2)
    
    # Send angle of servo 2
    sendAngle(comms,checkJointValue(q2,"2"),"2")
    
    # Send angle of servo 1
    sendAngle(comms,checkJointValue(q1,"1"),"1")
    
    # Robot coordinates
    x_points,y_points = robot.robotCoordinates()

    print(f"pos: {point[0],point[1]}, q1 = {q1:.2f}, q2 = {q2:.2f}")
    print(f"end effector:  [{x_points[-1]:.2f}, {y_points[-1]:.2f}]")

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



def main():
    # Create the robot
    print("Creating the Robot...")
    robot = Robot2r(10,10,90,-30)
    print("Robot created!")
    
    # Configure comms
    print("Starting comms...")
    serial_comms = initComms(PORT,BAUD)
    print("Connection established. Calibrate, operate, or q for exit.\n")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    ax.set_aspect('equal')
    ax.set_title("Controlling Robot with Keyboard")
    ax.grid(True, linestyle='--', alpha=0.5)

    (lines,) = ax.plot([], [], lw=4, marker='o', color="#0077cc", markersize=6)
    (end_dot,) = ax.plot([], [], 'o', color='red', markersize=8)

    new_path = path_interp(path,10)
    
    # Create animation (interval = 16 ms ≈ 60 FPS)
    ani = animation.FuncAnimation(fig, update,fargs=(new_path,robot,serial_comms,lines,end_dot), interval=16, blit=True)

    plt.show()
         
    # Close comms
    serial_comms.close()


# -----------------------------
# Entry point of the program
# -----------------------------
if __name__ == "__main__":
    main()