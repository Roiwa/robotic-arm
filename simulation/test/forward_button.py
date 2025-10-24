from link import Link


# ==============================================================
# Crear conjunto de links usando el constructor con padre
# ==============================================================
link1 = Link(30, 3)                         # primer eslabón
print(link1)
link2 = Link.from_parent(link1, 45, 3)    # segundo eslabón
print(link2)
link3 = Link.from_parent(link2, 10, 3)   # tercer eslabón
print(link3)

links = [link1, link2, link3]

for link in links:
    print(link)
input()


# -------------------------
# Animar link
# -------------------------
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


# ==============================================================
# Crear figura
# ==============================================================
fig, ax = plt.subplots(figsize=(7, 7))
fig.canvas.manager.set_window_title("Brazo robótico paso a paso")
plt.subplots_adjust(bottom=0.2)

ax.set_aspect('equal', 'box')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Brazo robótico controlado por botón")

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

(lineas,) = ax.plot([], [], lw=4, marker='o', color="#0077cc", markersize=6)
(end_dot,) = ax.plot([], [], 'o', color='red', markersize=8)
trayectoria, = ax.plot([], [], '--', color='orange', lw=1)

trayectoria_x, trayectoria_y = [], []

# ==============================================================
# Función de actualización
# ==============================================================
frame = 0
def update_frame(event):
    global frame
    frame += 1

    print(f'frame {frame}')
    # Animar los ángulos con el tiempo (movimiento suave)
    link1.set_angle_deg(30 + 30 * math.sin(frame * 0.2))

    # Calcular posiciones
    x_points = [0.0]
    y_points = [0.0]
    for link in links:
        xe, ye = link.endpoint()
        x_points.append(xe)
        y_points.append(ye)
        print(link)
    
    

    lineas.set_data(x_points, y_points)
    end_dot.set_data([x_points[-1]], [y_points[-1]])

    trayectoria_x.append(x_points[-1])
    trayectoria_y.append(y_points[-1])
    trayectoria.set_data(trayectoria_x, trayectoria_y)

    fig.canvas.draw_idle()

# ==============================================================
# Crear botón
# ==============================================================
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
boton = Button(ax_button, 'Siguiente paso', color='lightgray', hovercolor='0.8')
boton.on_clicked(update_frame)

plt.show()
