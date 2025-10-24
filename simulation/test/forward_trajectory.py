from link import Link
from bullet import Bullet
import sys
# ==============================================================
# Objective of the script:
# Observing how the robotic arm moves and a particle
# Input: python3 forward_trajectory.py <number op>
# Number ops:  0 - move link 1, 
#              1 - move link 2, 
#              2 - move link 3, 
#              3 - move all links
# ==============================================================

# ==============================================================
# Condiciones iniciales
# ==============================================================
if len(sys.argv) > 1:
    cd_robot = int(sys.argv[1]) #0 mover link 1, 1 mover link 2, 2 mover link 3, 3 mover todos los links
    print(cd_robot)
else:
    cd_robot = 0 
    
# ==============================================================
# Parámetros de simulación
# ==============================================================
dt = 0.1  # cada frame equivale a 0.1 segundos

# ==============================================================
# Crear conjunto de links usando el constructor con padre
# ==============================================================
link1 = Link(30, 3)                         # primer eslabón
link2 = Link.from_parent(link1, 45, 3)    # segundo eslabón
link3 = Link.from_parent(link2, 10, 3)   # tercer eslabón


links = [link1, link2, link3]

for link in links:
    print(link)
    
# ==============================================================
# Crear un proyectil
# ==============================================================
bullet = Bullet(x0=5, y0=5, color='black', max_step=0.1)


# -------------------------
# Animar link
# -------------------------
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque


# ==============================================================
# Crear figura
# ==============================================================
fig, ax = plt.subplots(figsize=(7, 7))
fig.canvas.manager.set_window_title("Animación Brazo Robótico 2D")

ax.set_aspect('equal', 'box')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Brazo robótico animado")

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

(lineas,) = ax.plot([], [], lw=4, marker='o', color="#0077cc", markersize=6)
(end_dot,) = ax.plot([], [], 'o', color='red', markersize=8)
max_trayectoria, = ax.plot([], [], '--', color='green', lw=1)
min_trayectoria, = ax.plot([], [], '--', color='green', lw=1)


point, = ax.plot([], [], 'o', color=bullet.color, markersize=8)
trayectoria, = ax.plot([], [], '--', color='orange', lw=1)

# ==============================================================
# Crear la trayectoria máxima del robot
# ==============================================================
length_links = 0
for link in links:
    length_links += link.length
    link_length =link.length


step_angles = list(range(0, 181, 10))
print(step_angles)
max_trayectoria_x = [length_links* math.cos(math.radians(i)) for i in step_angles]
max_trayectoria_y = [length_links* math.sin(math.radians(i)) for i in step_angles]
max_trayectoria.set_data(max_trayectoria_x, max_trayectoria_y)

min_trayectoria_x = [link_length* math.cos(math.radians(i)) for i in step_angles]
min_trayectoria_y = [link_length* math.sin(math.radians(i)) for i in step_angles]
min_trayectoria.set_data(min_trayectoria_x, min_trayectoria_y)

# ==============================================================
# Animación
# ==============================================================

def update(frame):
        
    # Calcular tiempo real del frame
    t = frame * dt  # cada frame representa 0.1 segundos
    
    #mover el proyectil
    bullet.move()
    
    x, y = bullet.get_position()
    tx, ty = bullet.get_trajectory()
    
    # Animar los ángulos según las condiciones iniciales
    if cd_robot == 0:
        link1.set_angle_deg(30 + 30 * math.sin(t * 0.2))
    elif cd_robot == 1:
        link2.set_angle_deg(45 + 40 * math.sin(t * 0.3))
    elif cd_robot == 2:
        link3.set_angle_deg(-60 + 50 * math.sin(t * 0.4))
    elif cd_robot == 3:
        link1.set_angle_deg(30 + 30 * math.sin(t * 0.2))
        link2.set_angle_deg(45 + 40 * math.sin(t * 0.3))
        link3.set_angle_deg(-60 + 50 * math.sin(t * 0.4))

    # Calcular posiciones encadenadas
    x_points = [0.0]
    y_points = [0.0]

    length_links = 0
    for link in links:
        #print(link)
        xe, ye = link.endpoint()
        x_points.append(xe)
        y_points.append(ye)
        length_links += link.length

    # Actualizar brazo
    lineas.set_data(x_points, y_points)
    end_dot.set_data([x_points[-1]], [y_points[-1]])

    # Guardar y mostrar trayectoria del extremo final
    point.set_data([x], [y])
    trayectoria.set_data(tx, ty)

    return lineas, end_dot, trayectoria, point

ani = FuncAnimation(fig, update, frames = 400, interval=50, blit=True)
plt.show()
