
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial
import math
import threading

import sys
sys.path.insert(0, "../../simulation/objects") # add folder "objects" path to search list for importing its modules

from robot2r import Robot2r

# ==============================================================
# Configuration parameters
# ==============================================================
PORT = '/dev/ttyACM0'   # Change '/dev/ttyACM0' by the correct port of your system
BAUD = 9600             # Change by the baud rate of your configuration

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


## Starting the communications
# Configure comms
print("Starting comms...")
serial_comms = initComms(PORT,BAUD)
print("Connection established. Calibrate, operate, or q for exit.\n")

# --- shared variable ---
q1 = 90
q2 = -90
lock = threading.Lock()

def send_uart():
    """Fcn to send the servo angles to the MCU. It uses threads to avoid 
    interfering with keyboard and graphics
    """
    global q1, q2
    
    while True:
        with lock:
            #Sending joint 1 angle
            val_int = q1
            message = f"{1},{val_int}\n"
            serial_comms.write(message.encode('utf-8'))  # Send value with line break
            
            #Sending joint 2 angle
            val_int = q2
            val_int = -val_int 
            message = f"{2},{val_int}\n"
            serial_comms.write(message.encode('utf-8'))  # Send value with line break
            time.sleep(0.01) # avoid saturating the CPU

# Launch the UART Sending thread
threading.Thread(target=send_uart, daemon=True).start()

# Position and speed variables
pos_x, pos_y = 0, 20
vx, vy = 0, 0
speed = 0.5

# Manage pressed keys
def on_key_press(event):
    """this fcn detects that one of these four keys are pressed 
    and changes the axis velocity

    Args:
        event (event): pressed keys
    """
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
    """This fcn detects that one of these four keys are released

    Args:
        event (event): released keys
    """
    global vx, vy
    if event.key in ['left', 'right']:
        vx = 0
    elif event.key in ['up', 'down']:
        vy = 0


# Update animation (≈60 FPS)
def update(frame,robot,lines,end_dot,ball):
    """Dynamics and graphical update

    Args:
        frame (frame): frame pic
        new_path (list): A list of points
        robot (robot): The robotic arm
        comms (serial): serial communication
        lines (list): links points
        end_dot (list): point of end effector

    Returns:
        list: the line list is the new links points, 
        end_dot is the new point of end effector, 
        and ball is also the point of the end effector when matches
    """
    global pos_x, pos_y, vx, vy, q1, q2
    pos_x += vx
    pos_y += vy
    
    # Move robot    
    robot.move2point((pos_x,pos_y))
    q1 = int(math.degrees(robot.q1))
    q2 = int(math.degrees(robot.q2))

    # Robot coordinates
    x_points,y_points = robot.robotCoordinates()

    # Print robot
    lines.set_data(x_points, y_points)
    end_dot.set_data([x_points[-1]], [y_points[-1]])

    # Movement limitation
    pos_x = max(-10 + ball.radius, min(20 - ball.radius, pos_x))
    pos_y = max(-10 + ball.radius, min(20 - ball.radius, pos_y))

    ball.center = (pos_x, pos_y)
    return ball, lines, end_dot

def main():
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

    # Create a ball
    radio = 0.25
    ball = plt.Circle((0, 0), radio, color='green')
    ax.add_patch(ball)
    
    # Connect keyboard events
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    fig.canvas.mpl_connect('key_release_event', on_key_release)

    # Create animation (interval = 16 ms ≈ 60 FPS)
    ani = animation.FuncAnimation(fig, update,fargs=(robot,lines,end_dot,ball), interval=100, blit=True)

    plt.show()
         
    # Close comms
    serial_comms.close()


# -----------------------------
# Entry point of the program
# -----------------------------
if __name__ == "__main__":
    main()
