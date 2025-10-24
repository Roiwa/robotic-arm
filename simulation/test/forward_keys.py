from link import Link
from bullet import Bullet
import sys

# ==============================================================
# Objective of the script:
# Controlling the robotic arm using 6 keys, one per each angle 
# direction.
# ==============================================================

# ==============================================================
# Parámetros de simulación
# ==============================================================
dt = 0.1  # cada frame equivale a 0.1 segundos
dtheta = 1 # cada cambio de theta es de 1 grado

# ==============================================================
# Estado del programa
# ==============================================================
estado_teclas = {'1': False, '2': False, '3': False, '4': False, '5': False, '6': False}

# ==============================================================
# Callbacks de teclado
# ==============================================================
def on_key_press(event):
    if event.key in estado_teclas:
        estado_teclas[event.key] = True

def on_key_release(event):
    if event.key in estado_teclas:
        estado_teclas[event.key] = False
        


# ==============================================================
# Crear conjunto de links usando el constructor con padre
# ==============================================================
link1 = Link(30, 3)                         # primer eslabón
link2 = Link.from_parent(link1, 45, 3)    # segundo eslabón
link3 = Link.from_parent(link2, 10, 3)   # tercer eslabón


links = [link1, link2, link3]

for link in links:
    print(link)
    
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
trayectoria, = ax.plot([], [], '--', color='orange', lw=1)

#deque limita la lista a los últimos 50 números
trayectoria_x, trayectoria_y = deque(maxlen=50), deque(maxlen=50)

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
    
    # Operaciones según las teclas presionadas
    if estado_teclas['1']:
        links[0].set_angle_deg(links[0].get_angle_rel_deg()-dtheta)
    if estado_teclas['2']:
        links[1].set_angle_deg(links[1].get_angle_rel_deg()-dtheta)
    if estado_teclas['3']:
        links[2].set_angle_deg(links[2].get_angle_rel_deg()-dtheta)
    if estado_teclas['4']:
        links[0].set_angle_deg(links[0].get_angle_rel_deg()+dtheta)
    if estado_teclas['5']:
        links[1].set_angle_deg(links[1].get_angle_rel_deg()+dtheta)
    if estado_teclas['6']:
        links[2].set_angle_deg(links[2].get_angle_rel_deg()+dtheta)


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
    trayectoria_x.append(x_points[-1])
    trayectoria_y.append(y_points[-1])
    trayectoria.set_data(trayectoria_x, trayectoria_y)

    return lineas, end_dot, trayectoria

# ==============================================================
# Conectar eventos de teclado
# ==============================================================
fig.canvas.mpl_connect('key_press_event', on_key_press)
fig.canvas.mpl_connect('key_release_event', on_key_release)

ani = FuncAnimation(fig, update, frames = 400, interval=50, blit=True)
plt.show()
