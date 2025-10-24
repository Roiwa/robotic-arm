import random
from collections import deque
import math


class Bullet:
    def __init__(self, x0=1.0, y0=1.0, color='red', max_step=1.0):
        """
        x0, y0: posición inicial del proyectil
        color: color del punto en la gráfica
        max_step: desplazamiento máximo en cada eje por paso
        """
        self.x = x0
        self.y = y0
        self.max_step = max_step
        self.color = color
        
        #deque limita la lista a los últimos 50 números (sliding window)
        self.trayectoria_x, self.trayectoria_y = deque(maxlen=50), deque(maxlen=50)
        self.trayectoria_x.append(x0)
        self.trayectoria_y.append(y0)
        
        
    def move(self):
        """Actualiza la posición del proyectil con un movimiento aleatorio suave."""
        dx = random.uniform(-self.max_step, self.max_step)
        dy = random.uniform(-self.max_step, self.max_step)
        if self.x+dx < 10 and self.x + dx > -10:
            self.x += dx
        if self.y+dy < 10 and self.y+dy > -10:
            self.y += dy

        # Guardar trayectoria
        self.trayectoria_x.append(self.x)
        self.trayectoria_y.append(self.y)
    
    def move2pos(self,x,y):
        self.x = x
        self.y = y
    
    def get_angle_abs(self):
        if self.x < 0:
            phi = math.pi + math.atan(self.y/self.x)
        else:
            phi = math.atan(self.y/self.x)
        return phi

    def get_position(self):
        """Devuelve la posición actual (x, y)."""
        return self.x, self.y

    def get_trajectory(self):
        """Devuelve toda la trayectoria (listas de x e y)."""
        return self.trayectoria_x, self.trayectoria_y