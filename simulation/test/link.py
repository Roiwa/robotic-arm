import math

class Link:
    def __init__(self, theta_deg, length, parent=None):
        """
        Constructor principal:
        - theta_deg: ángulo en grados (relativo al eje x o al link padre)
        - length   : longitud del eslabón
        - parent   : otro objeto Link (opcional)
        """
        self.theta_rel = math.radians(theta_deg)
        self.length = float(length)
        self.parent = parent

        if parent is None:
            # Este link no tiene padre → su base está en el origen
            self.x0, self.y0 = 0.0, 0.0
            self.theta_base = 0
        else:
            # La base está en el extremo del link padre y con el ángulo entre el link padre y la horizontal
            self.theta_base = self.parent.theta_abs
            self.x0, self.y0 = parent.endpoint()
            
        self.theta_abs= self.theta_rel+self.theta_base

    @classmethod
    def from_parent(cls, parent, theta_deg, length):
        """
        Constructor alternativo:
        Crea un link usando otro link como base.
        """
        return cls(theta_deg, length, parent)

    def set_angle_deg(self, theta_deg):
        self.theta_rel = math.radians(theta_deg)
        
    def set_angle_ref(self,phi_radians):
        if self.parent is None:
            theta_parent = 0
        else:
            theta_parent = self.parent.theta_abs
        
        self.theta_rel = phi_radians-theta_parent

    def get_angle_deg(self):
        return math.degrees(self.theta_abs)
    
    def get_angle_rel_deg(self):
        return math.degrees(self.theta_rel)
    
    def update_angles(self):
        if self.parent is not None:
            self.theta_base = self.parent.theta_abs
        self.theta_abs= self.theta_rel+self.theta_base
    
    def endpoint(self):
        """Devuelve (x_end, y_end) calculado desde la posición y el ángulo actuales."""
        
        #actualiza los ángulos base y absoluto con el nuevo ángulo del link padre (de haberlo)
        self.update_angles()
        
        if self.parent is None:
            abs_angle = self.theta_rel
            x0, y0 = self.x0, self.y0
        else:
            abs_angle = self.parent.theta_abs + self.theta_rel
            x0, y0 = self.parent.endpoint()
            self.x0, self.y0 = x0, y0
        x_end = x0 + self.length * math.cos(abs_angle)
        y_end = y0 + self.length * math.sin(abs_angle)
        
        return (x_end, y_end)
        
    def __repr__(self):
        xe, ye = self.endpoint()
        return (
            f"Link(θt={self.get_angle_deg():.2f}°, θr={math.degrees(self.theta_rel):.2f}°, θb={math.degrees(self.theta_base):.2f}°, "
            f"L={self.length:.2f}, "
            f"Base=({self.x0:.2f},{self.y0:.2f}) → End=({xe:.2f},{ye:.2f}))"
        )