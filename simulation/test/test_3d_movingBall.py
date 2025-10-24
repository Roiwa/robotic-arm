import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import time

# Parámetros
g = 9.81
dt = 1 / 60.0   # 60 FPS
radius = 0.2
restitution = 0.8
speed = 4.0     # velocidad horizontal con las teclas

# Estado inicial
pos = np.array([0.0, 0.0, 3.0])
vel = np.array([0.0, 0.0, 0.0])

# Configurar figura 3D
plt.ion()
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")
ax.set_box_aspect([1.5, 1.0, 0.8])
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(0, 5)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_title("Bola 3D controlada con el teclado (60 FPS)")

# Crear esfera (malla)
phi, theta = np.mgrid[0:np.pi:20j, 0:2*np.pi:20j]
xs = radius * np.sin(phi) * np.cos(theta)
ys = radius * np.sin(phi) * np.sin(theta)
zs = radius * np.cos(phi)

# Dibujo inicial
surface = ax.plot_surface(xs + pos[0], ys + pos[1], zs + pos[2],
                          color='orange', shade=True)
trail, = ax.plot([], [], [], 'b-', linewidth=1)
bar, = ax.plot([], [], [], 'r-', linewidth=3)  # ← la barra roja

trail_points = [pos.copy()]

# Variables de control de entrada
key_state = {"up": False, "down": False, "left": False, "right": False, "1": False, "2": False}

# --- Funciones para el teclado ---
def on_key_press(event):
    if event.key in ["up", "w"]:
        key_state["up"] = True
    elif event.key in ["down", "s"]:
        key_state["down"] = True
    elif event.key in ["left", "a"]:
        key_state["left"] = True
    elif event.key in ["right", "d"]:
        key_state["right"] = True
    elif event.key in ["1"]:
        key_state["1"] = True
    elif event.key in ["2"]:
        key_state["2"] = True

def on_key_release(event):
    if event.key in ["up", "w"]:
        key_state["up"] = False
    elif event.key in ["down", "s"]:
        key_state["down"] = False
    elif event.key in ["left", "a"]:
        key_state["left"] = False
    elif event.key in ["right", "d"]:
        key_state["right"] = False
    elif event.key in ["1"]:
        key_state["1"] = False
    elif event.key in ["2"]:
        key_state["2"] = False

fig.canvas.mpl_connect("key_press_event", on_key_press)
fig.canvas.mpl_connect("key_release_event", on_key_release)

# --- Bucle principal ---
last_time = time.time()

while plt.fignum_exists(fig.number):

    # Movimiento horizontal según teclas
    move = np.array([0.0, 0.0, 0.0])
    if key_state["up"]:
        move[1] += speed
    if key_state["down"]:
        move[1] -= speed
    if key_state["left"]:
        move[0] -= speed
    if key_state["right"]:
        move[0] += speed
    if key_state["1"]:
        move[2] += speed
    if key_state["2"]:
        move[2] -= speed
    vel[0:3] = move[0:3]

    pos += vel * dt

    # Rebote con límites del área
    for i, lim in enumerate([5, 5]):
        if pos[i] >= lim - radius:
            pos[i] = lim - radius
            vel[i] = -vel[i] * restitution
        elif pos[i] <= -lim + radius:
            pos[i] = -lim + radius
            vel[i] = -vel[i] * restitution

    # --- Dibujo ---
    # eliminar la esfera anterior
    surface.remove()
    # dibujar la nueva esfera
    surface = ax.plot_surface(xs + pos[0], ys + pos[1], zs + pos[2],
                            color='orange', shade=True)
    
    # Actualizar barra (pegada al extremo de la esfera)
    # Por ejemplo, una barra de 1 metro hacia adelante en Y
    barra_longitud = 1.0
    start = pos + np.array([0, radius, 0])  # extremo que toca la esfera
    end = start + np.array([0, barra_longitud, 0])
    bar.set_data([start[0], end[0]], [start[1], end[1]])
    bar.set_3d_properties([start[2], end[2]])
    
    # actualizar rastro
    trail_points.append(pos.copy())
    trail_arr = np.array(trail_points[-300:])  # mantener últimos puntos
    trail.set_data(trail_arr[:, 0], trail_arr[:, 1])
    trail.set_3d_properties(trail_arr[:, 2])

    plt.pause(0.001)

    # limitar FPS aproximadamente
    now = time.time()
    elapsed = now - last_time
    if elapsed < dt:
        time.sleep(dt - elapsed)
    last_time = now
