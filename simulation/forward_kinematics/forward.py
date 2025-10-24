"""
Programa: brazo_dos_eslabones.py
Descripción:
    Visualiza el área de movimiento (alcance) de un brazo robótico de dos eslabones.
    Permite modificar los ángulos de las articulaciones con deslizadores.
Requisitos:
    pip install matplotlib numpy
Ejecución:
    python brazo_dos_eslabones.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# -----------------------
# Parámetros del brazo
# -----------------------
L1 = 2.0   # longitud del primer eslabón
L2 = 1.5   # longitud del segundo eslabón

# -----------------------
# Cálculo del área de alcance
# -----------------------
n = 300
theta1 = np.linspace(0, 2 * np.pi, n)
theta2 = np.linspace(0, 2 * np.pi, n)
T1, T2 = np.meshgrid(theta1, theta2)

X = L1 * np.cos(T1) + L2 * np.cos(T1 + T2)
Y = L1 * np.sin(T1) + L2 * np.sin(T1 + T2)

# -----------------------
# Crear figura
# -----------------------
fig, ax = plt.subplots(figsize=(7, 7))
plt.subplots_adjust(left=0.1, bottom=0.25)
ax.set_aspect('equal')
ax.set_xlim(-(L1 + L2 + 0.5), L1 + L2 + 0.5)
ax.set_ylim(-(L1 + L2 + 0.5), L1 + L2 + 0.5)
ax.set_title('Área de movimiento de un brazo robótico de dos eslabones')

# Dibujar área de alcance
ax.fill(X.flatten(), Y.flatten(), color='lightblue', alpha=0.3, label="Área alcanzable")

# Eslabones (posición inicial)
theta1_val = np.pi / 4
theta2_val = np.pi / 4

x1 = L1 * np.cos(theta1_val)
y1 = L1 * np.sin(theta1_val)
x2 = x1 + L2 * np.cos(theta1_val + theta2_val)
y2 = y1 + L2 * np.sin(theta1_val + theta2_val)

# Dibujar brazo
brazo_line, = ax.plot([0, x1, x2], [0, y1, y2], 'o-', color='red', lw=3, label='Brazo')
ax.legend()

# -----------------------
# Deslizadores para los ángulos
# -----------------------
ax_theta1 = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_theta2 = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_theta1 = Slider(ax_theta1, 'Ángulo 1', 0, 2*np.pi, valinit=theta1_val)
slider_theta2 = Slider(ax_theta2, 'Ángulo 2', 0, 2*np.pi, valinit=theta2_val)

# -----------------------
# Función de actualización
# -----------------------
def actualizar(val):
    t1 = slider_theta1.val
    t2 = slider_theta2.val

    x1 = L1 * np.cos(t1)
    y1 = L1 * np.sin(t1)
    x2 = x1 + L2 * np.cos(t1 + t2)
    y2 = y1 + L2 * np.sin(t1 + t2)

    brazo_line.set_data([0, x1, x2], [0, y1, y2])
    fig.canvas.draw_idle()

slider_theta1.on_changed(actualizar)
slider_theta2.on_changed(actualizar)

plt.show()
