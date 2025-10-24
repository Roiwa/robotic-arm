from link import Link
import sys

# ==============================================================
# Condiciones iniciales
# ==============================================================
if len(sys.argv) > 1:
    cd_robot = int(sys.argv[1]) #0 mover link 1, 1 mover link 2, 2 mover link 3, 3 mover todos los links
    print(cd_robot)
else:
    cd_robot = 0 

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
trayectoria, = ax.plot([], [], '--', color='orange', lw=1)

#deque limita la lista a los últimos 50 números
trayectoria_x, trayectoria_y = deque(maxlen=50), deque(maxlen=50)


# ==============================================================
# Crear la trayectoria máxima del robot
# ==============================================================
length_links = 0
for link in links:
    length_links += link.length


step_angles = list(range(0, 181, 10))
print(step_angles)
max_trayectoria_x = [length_links* math.cos(math.radians(i)) for i in step_angles]
max_trayectoria_y = [length_links* math.sin(math.radians(i)) for i in step_angles]
max_trayectoria.set_data(max_trayectoria_x, max_trayectoria_y)

# ==============================================================
# Animación
# ==============================================================
def update(frame):
    
    # Animar los ángulos según las condiciones iniciales
    if cd_robot == 0:
        link1.set_angle_deg(3*frame)
    elif cd_robot == 1:
        link2.set_angle_deg(3*frame)
    elif cd_robot == 2:
        link3.set_angle_deg(3*frame)
    elif cd_robot == 3:
        link1.set_angle_deg(30 + 30 * math.sin(frame * 0.2))
        link2.set_angle_deg(45 + 40 * math.sin(frame * 0.3))
        link3.set_angle_deg(-60 + 50 * math.sin(frame * 0.4))

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

ani = FuncAnimation(fig, update, interval=30, blit=True)
plt.show()
