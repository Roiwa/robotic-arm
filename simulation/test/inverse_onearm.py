
"""
Programa: inverse_onearm.py
Descripction:
    Shows how a one-link robotic arm follows a bullet moved by the mouse.
    The text in the graph indicates the bullet coordinates and its angle.
    The frame updates continuously (≈60 FPS) without depending on the mouse movement.
Requirements:
    pip install matplotlib
"""

import matplotlib.pyplot as plt
import math

from link import Link
from bullet import Bullet

# ==============================================================
# Create a bullet
# ==============================================================
bullet = Bullet(x0=5, y0=5, color='black', max_step=0.1)

# ==============================================================
# Create a link
# ==============================================================
link1 = Link(30, 3)                         # primer eslabón

links = [link1]

# Crear figura y ejes
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal', 'box')
ax.set_title('La bola sigue al ratón (actualización continua)')

(lineas,) = ax.plot([], [], lw=4, marker='o', color="#0077cc", markersize=6)
(end_dot,) = ax.plot([], [], 'o', color='red', markersize=8)

point, = ax.plot([], [], 'o', color=bullet.color, markersize=8)


# Crear texto para mostrar los datos
texto_info = ax.text(-9.5, 9, "", fontsize=10, color='blue', va='top')

# Variables globales
mouse_pos = (1.0, 1.0)

# Guardar posición del ratón
def on_move(event):
    global mouse_pos
    if event.inaxes is not None:
        mouse_pos = (event.xdata, event.ydata)

# Conectar evento del ratón
fig.canvas.mpl_connect('motion_notify_event', on_move)

# Función de actualización continua
def update_frame():

    # Actualizar bola
    x, y = mouse_pos
    bullet.move2pos(x,y)
    #bola.center = (x, y)
    
    # Move the arm
    links[0].set_angle_ref(bullet.get_angle_abs())
    
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

    # Print the arm
    lineas.set_data(x_points, y_points)
    end_dot.set_data([x_points[-1]], [y_points[-1]])

    # Actualizar texto
    texto_info.set_text(f"Mouse: ({x:.2f}, {y:.2f}), phi: {math.degrees(bullet.get_angle_abs()):.2f}, theta_rel: {links[0].get_angle_rel_deg():.2f}, theta_abs: {links[0].get_angle_deg():.2f}")
    
    # Print the bullet
    point.set_data([x], [y])

    # Redibujar figura
    fig.canvas.draw_idle()

# Temporizador para actualizar ≈60 veces por segundo interval=16
timer = fig.canvas.new_timer(interval=16)
timer.add_callback(update_frame)
timer.start()

plt.show()
