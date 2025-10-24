

## Embedded Folder
### robotic-arm folder (copy its files to embedded and remove it)
#### 1. Cal.ino Folder
This folder contains the arduino code for controlling the servos using the information received by UART from computer. The cal.ino file is a program made using Arduino IDE and its libraries for UART and servos. Very simple code, the mathematical processing its done inside the computer.

#### 2. calibration.py file (REWRITE)
This file has two functionalities: 
    1) the calibration functionality moves link 2 to 90 degrees and link 1 to 0 degrees. The objective is to put each servo in that position so we can place the real links in the servo. Fig. (INSERT IMAGE) shows the position for a calibrated robotic arm where link1 must be parallel to the horizontal line, and link 2 must be perpendicular to link 1 and pointing out to the floor. This will allow to move the robotic arm in the first quadrant of the xy plane, being its origin (0,0) in the first joint (base joint) of link 1. 

    2) the next functionality is to give different angles to the servo motors to test that they work properly in the xy plane. Note that servos only have a range of degrees between 0 and 180 degrees.Starting with link1, this link covers from one direction to the other one of the horizontal line (PICTURE). Regarding to the link 2, this link has its origin associated to link 1, so that when putting 0 degrees link 2 has to be in line with link 1 and pointing out in the same direction. On the other hand, if link 2 is in line with link 1 but pointing out in opposite direction, its angle must be 180. 
    
    However, we should not confuse theoretical angles (to move the robotic arm in the xy plane) with servo angles. Servo angles depend on the physical position of servos. Servo 1 is pointing out in the opposite direction to servo 2, this means that their rotation is also inverted. So, when we indicate both servos to move to 10 degrees, servo 1 will move to an angle of 10 degrees according to the horizontal line; however, servo 2 (as it is place in opposite direction) will rotate to -10 degrees respect to its reference. Also, our configuration (CALIBRATION PICTURE) determines movement range of link 2, so when link 1 is lined up with link 2 and pointing out the same direction, we must put in the servo 0 degrees; otherwise, when link 1 is lined up with link 2 and pointing out the opposite direction will be 180 degrees.

#### 3. path_follower_any.py
In this program, the robotic arm follows a sequence of points (path). It shows the simulation of the movement of the robotic arm in a window as also moves the physical robotic arm. 

To execute this program, you must set the configuration parameters:
-   PORT (the USB port where your MCU is connected)  
-   BAUD (baud rate of the communication)             
-   path (path of the robot: list of points)


#### 4. robotic_arm.py
This program allows us to control a physical robot while seeing in the computer screen a simulation of it in real-time.

To execute this program, you must set the configuration parameters:
-   PORT (the USB port where your MCU is connected)  
-   BAUD (baud rate of the communication)             
-   path (path of the robot: list of points)



## Simulation folder