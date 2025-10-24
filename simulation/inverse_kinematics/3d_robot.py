"""
Program: 3d_robot.py
Description:
    Controls a 2R robotic arm in cartesian way (x and y) using
    "up", "down", "left", and "right" keys in a 3D space. To do so, it uses 
    an analytical approach for inverse kinematics. The frame 
    updates continuously (≈60 FPS) without depending on the mouse movement.
Possibilities:
    Robot configuration can be changed. Be careful to not exceed the limits of the canvas
Requirements:
    pip install matplotlib
    robot2r library
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import time

import sys
sys.path.insert(0, "../objects") # add folder "objects" path to search list for importing its modules

from robot2r import Robot2r

# Create the robot
robot = Robot2r(4,3,0,0)

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
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
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


z_pos = 3

################################### TOCAR
# Dibujo inicial
surface = ax.plot_surface(xs + pos[0], ys + pos[1], zs + pos[2],
                          color='orange', shade=True)
bar0, = ax.plot([], [], [], 'b-', linewidth=3)  # ← la barra roja
bar1, = ax.plot([], [], [], 'b-', linewidth=3)  # ← la barra roja
bar2, = ax.plot([], [], [], 'r-', linewidth=3)  # ← la barra roja


# Texto en pantalla (posición)
pos_text = ax.text2D(0.02, 0.95, "", transform=ax.transAxes, fontsize=11, color='black',
                     bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))


trail, = ax.plot([], [], [], 'g-', linewidth=1)
trail_points = [pos.copy()]
################################### FIN TOCAR


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

    ## Rebote con límites del área
    #for i, lim in enumerate([5, 5]):
    #    if pos[i] >= lim - radius:
    #        pos[i] = lim - radius
    #        vel[i] = -vel[i] * restitution
    #    elif pos[i] <= -lim + radius:
    #        pos[i] = -lim + radius
    #        vel[i] = -vel[i] * restitution


    ################################### TOCAR
    
    # Move robot    
    robot.move2point((pos[0],pos[1]))
    
    # Robot coordinates
    x_points,y_points = robot.robotCoordinates()
    
    # --- Dibujo ---

    
    # Actualizar barra (pegada al extremo de la esfera)
    # Por ejemplo, una barra de 1 metro hacia adelante en Y
    start = [0,0,0]
    end = [0,0,3]
    bar0.set_data([start[0], end[0]], [start[1], end[1]])
    bar0.set_3d_properties([start[2], end[2]])
    
    # Actualizar barra (pegada al extremo de la esfera)
    # Por ejemplo, una barra de 1 metro hacia adelante en Y
    start = [x_points[0], y_points[0], z_pos]
    end = [x_points[1], y_points[1], z_pos]
    bar1.set_data([start[0], end[0]], [start[1], end[1]])
    bar1.set_3d_properties([start[2], end[2]])
    
    # Actualizar barra (pegada al extremo de la esfera)
    # Por ejemplo, una barra de 1 metro hacia adelante en Y
    start = [x_points[1], y_points[1], z_pos]
    end = [x_points[-1], y_points[-1], z_pos]
    bar2.set_data([start[0], end[0]], [start[1], end[1]])
    bar2.set_3d_properties([start[2], end[2]])
    
    # eliminar la esfera anterior
    surface.remove()
    # dibujar la nueva esfera
    surface = ax.plot_surface(xs + pos[0], ys + pos[1], zs + z_pos,
                            color='orange', shade=True)
    
    # --- Mostrar posición ---
    pos_text.set_text(f"Ball position: X={pos[0]:.2f}, Y={pos[1]:.2f}, Z={pos[2]:.2f}")

    
    # actualizar rastro
    trail_points.append(pos.copy())
    trail_arr = np.array(trail_points[-300:])  # mantener últimos puntos
    trail.set_data(trail_arr[:, 0], trail_arr[:, 1])
    trail.set_3d_properties(trail_arr[:, 2])
    ################################### NO TOCAR


    plt.pause(0.001)

    # limitar FPS aproximadamente
    now = time.time()
    elapsed = now - last_time
    if elapsed < dt:
        time.sleep(dt - elapsed)
    last_time = now
