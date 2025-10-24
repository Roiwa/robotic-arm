import math
import numpy as np
from link import Link
import random

class Robot2r:
    def __init__(self, L1,L2,q1,q2,low_consumption=None):
        """
        Constructor:
        - L1: Length of link 1
        - L2: Length of link 2
        - q1: joint 1 angle (link 1)
        - q2: joint 2 angle (link 2)
        """
        
        self.L1 = L1
        self.L2 = L2
        self.q1 = q1
        self.q2 = q2
        self.low_consumption = low_consumption
        
        self.links = []
        self.links.append(Link(L1, q1))
        self.links.append(Link(L2, q2, self.links[-1]))
        
        # Maximum and minimum squared norm of the robot
        self.max_norm2 = (self.L1 + self.L2)**2
        self.min_norm2 = (self.L1 - self.L2)**2
        
    def calculateQ(self,point):
        # Squared norm of the point
        self.norm_point2 = point[0]**2 + point[1]**2 # x² + y²
        theta = math.atan2(point[1],point[0])
        
        # q2 cosine
        c2 = (self.norm_point2 - self.L1**2 - self.L2**2)/(2*self.L1*self.L2)
        
        if c2 > 1:
            # Here, we have two cases. 1) whenever anything is outside the workspace,
            # we can just stop the robot. 2) Or we can just point out the "thing"
            
            if self.low_consumption is not None:
                print("The point is out of reach (above its maximum norm)")
                return None
            else:
                self.q2 = 0 #
                self.q1 = theta
        
        elif c2 < -1:
            if self.low_consumption is not None:
                print("The point is out of reach (above its minimum norm)")
                return None
            else:
                self.q2 = np.pi #
                self.q1 = theta
        
        elif c2 == 1: # maximum reach
            self.q2 = 0 #
            self.q1 = theta
        
        elif c2 ==-1 and math.sqrt(self.norm_point2)!=0 :
            self.q2 = np.pi
            self.q1 = theta
            
        elif c2 ==-1 and math.sqrt(self.norm_point2)==0 :
            self.q2 = np.pi
            self.q1 = random.uniform(0, 2*math.pi)
            
        else:
            q2 = [math.acos(c2),-math.acos(c2)]
            q1 = []
            
            # Condition when there are two solutions is that the sum of theta differences must be minimized
            diff_prev = 1000 #>= 2*pi
            for i,item in enumerate(q2):
                q1.append(theta - math.atan2(self.L2*math.sin(item),self.L1+self.L2*math.cos(item)))
                diff_theta = np.abs(self.q1 - q1[i]) + np.abs(self.q2 - q2[i])
                
                if diff_theta <= diff_prev:
                    i_f = i
                    diff_prev = diff_theta
            
            self.q1, self.q2 = q1[i_f], q2[i_f]
        self.links[0].theta = self.q1
        self.links[1].theta = self.q2
            
        
        return 1
            
    
    def move2point(self,point):
        
        # Calculate angles
        result = self.calculateQ(point)
            
        # Update links' positions
        if result is not None:
            for link in self.links:
                link.update()
        
        
    def endeffectorPos(self): #indicates the coordinates of the end effector
        return self.links[-1].calculateWorldCoordinates()
    
    def robotCoordinates(self): #gives the current position of all joints 
        # Calculate chained positions
        x_points = [0.0]
        y_points = [0.0]
        for link in self.links:
            coordinates = link.calculateWorldCoordinates()
            x_points.append(coordinates[0,0])
            y_points.append(coordinates[1,0])
            
        return x_points,y_points
            
                
