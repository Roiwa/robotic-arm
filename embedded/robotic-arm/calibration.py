import serial
import time

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

def checkJointValue(jointValue,linkNumber):
    """ We check that the value of the joint is between the proper range.
    Args:
        jointValue (str): joint angle introduced by the user
        linkNumber (str): number of the link

    Returns:
        int: the servo angle in degrees
    """
    
    # Convert jointValue from str to int
    val_int = int(jointValue)
    
    #transformation to servo angle in link 2
    if linkNumber == "2":
        val_int = -val_int 
        
    if 0 <= val_int <= 180:
        return val_int
    else:
        print("Value must be between 0 and 180 in absolute value.")
        return None
        
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

        
def nextJoint(jointNum):
    """It asks if the user wants to calibrate a link

    Args:
        jointNum (int): number of the joint
    """
    next="0"
    while next == "0":
        next = input(f"Do you want to calibrate link {jointNum}?(1/0)")

def main():
    
    # Configure comms
    print("Starting comms...")
    serial_comms = initComms(PORT,BAUD)
    print("Connection established. Calibrate, operate, or q for exit.\n")
    
    while True:
        program = input("calibration or operation?(c/o)")
        
        # Calibration
        if program.lower() == 'c':
            
            #calibration of link 1
            nextJoint(1)
            print("link 1 to 90 degrees")
            jointAngle = checkJointValue("90","1")
            if jointAngle is not None:
                sendAngle(serial_comms,jointAngle,"1")
            
            #calibration of link 2
            nextJoint(2)
            print("link 2 to -90 degrees regarding link 1")
            jointAngle = checkJointValue("-90","2")
            if jointAngle is not None:
                sendAngle(serial_comms,jointAngle,"2")
            
        # Operation
        elif program.lower() == 'o':
            while True:
                jointAngle = input("→ Joint value (0,180) for link1: ")
                jointAngle = checkJointValue(jointAngle,"1")
                if jointAngle is not None:
                    sendAngle(serial_comms,jointAngle,"1")
                    
                jointAngle = input("→ Joint value (-180,0) for link2: ")
                jointAngle = checkJointValue(jointAngle,"2")
                if jointAngle is not None:
                    sendAngle(serial_comms,jointAngle,"2")
                
        # Exit
        else:
            break
         
    # Close comms
    serial_comms.close()


# -----------------------------
# Entry point of the program
# -----------------------------
if __name__ == "__main__":
    main()