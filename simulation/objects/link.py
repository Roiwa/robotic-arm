import math
import numpy as np

class Link:
    def __init__(self, length, theta_deg, parent=None):
        """
        Constructor:
        - theta_deg: angle in degrees (relative to x axis or to parent link)
        - length   : link length
        - parent   : other link object (optional)
        """
        self.theta = math.radians(theta_deg)
        self.length = float(length)
        self.parent = parent
        
        # The link is defined by its its reference transform (related to its parent), 
        # its rotation matrix, and its coordinates
        
        
        if parent is None: # This link has no parent → its base is at the origin
            
            # Reference transform
            self.refTransform = np.array([
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ])
            self.x0, self.y0 = 0.0, 0.0
            self.theta_base = 0
        else:
            # its base is in the end point of its parent link
            # Reference transform
            self.refTransform = np.array([
                [1,         0, self.parent.length],
                [0,         1,                  0],
                [0,         0,                  1]
            ])
            
        # Rotation Matrix
        self.rotationMatrix = matriz = np.array([
            [np.cos(self.theta), -np.sin(self.theta),   0],
            [np.sin(self.theta),  np.cos(self.theta),   0],
            [0                 ,                   0,   1]
        ])
        
        # link coordinate about x axis
        self.coordinates = matriz = np.array([
            [self.length],
            [0],
            [1]
        ])
    
    def update(self):
        # Rotation Matrix
        self.rotationMatrix = matriz = np.array([
            [np.cos(self.theta), -np.sin(self.theta),   0],
            [np.sin(self.theta),  np.cos(self.theta),   0],
            [0                 ,                   0,   1]
        ])
        
        
    def calculateLinkTransform(self):
        
        if self.parent is None:
            return np.dot(self.refTransform,self.rotationMatrix)
        else:
            return np.dot(self.parent.calculateLinkTransform(),np.dot(self.refTransform,self.rotationMatrix))
        
    
    def calculateWorldCoordinates(self):
            return np.dot(self.calculateLinkTransform(),self.coordinates)