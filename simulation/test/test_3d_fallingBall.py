# bola_3d.py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib import animation

# Parámetros de la simulación
g = 9.81         # gravedad (m/s^2)
dt = 0.03        # paso temporal (s)
T = 6.0          # tiempo total (s)
n_steps = int(T / dt)

# Condiciones iniciales (posición y velocidad)
pos = np.array([0.0, 0.0, 1.0])   # x, y, z (m)
vel = np.array([3.0, 1.2, 6.0])   # vx, vy, vz (m/s)
radius = 0.12                     # radio de la bola (m)
restitution = 0.75                # coeficiente de restitución (rebote)

# Precomputamos la trayectoria (rebotando contra el suelo en z = radius)
traj = np.zeros((n_steps, 3))
vel_local = vel.copy()
pos_local = pos.copy()

for i in range(n_steps):
    traj[i] = pos_local
    vel_local[2] -= g * dt            # efecto de la gravedad
    pos_local = pos_local + vel_local * dt
    # rebote simple con el suelo (z = radius)
    if pos_local[2] <= radius:
        pos_local[2] = radius
        if vel_local[2] < 0:
            vel_local[2] = -vel_local[2] * restitution

# Configuración de la figura 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([1.5, 1.0, 0.8])

ax.set_xlim(-1, max(1.0, np.max(traj[:,0]) + 1))
ax.set_ylim(np.min(traj[:,1]) - 1, np.max(traj[:,1]) + 1)
ax.set_zlim(0, np.max(traj[:,2]) + 1.5)

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title('Movimiento 3D de una bola')

# Suelo de referencia
xx = np.linspace(-1, np.max(traj[:,0]) + 1, 10)
yy = np.linspace(np.min(traj[:,1]) - 1, np.max(traj[:,1]) + 1, 10)
XX, YY = np.meshgrid(xx, yy)
ZZ = np.zeros_like(XX)
ax.plot_wireframe(XX, YY, ZZ, linewidth=0.5, rcount=6, ccount=6)

# Representación de la bola como un punto y la línea-trayectoria
ball_scatter = ax.scatter([pos[0]], [pos[1]], [pos[2]], s=220)
trail_line, = ax.plot([], [], [], linewidth=1)

def init():
    ball_scatter._offsets3d = ([pos[0]], [pos[1]], [pos[2]])
    trail_line.set_data([], [])
    trail_line.set_3d_properties([])
    return ball_scatter, trail_line

def update(frame):
    x = traj[frame, 0]
    y = traj[frame, 1]
    z = traj[frame, 2]
    ball_scatter._offsets3d = ([x], [y], [z])
    trail_line.set_data(traj[:frame+1,0], traj[:frame+1,1])
    trail_line.set_3d_properties(traj[:frame+1,2])
    return ball_scatter, trail_line

anim = animation.FuncAnimation(fig, update, frames=n_steps,
                               init_func=init, interval=dt*1000, blit=False)

# Muestra la ventana con la animación
plt.show()

# ----- Opcional: guardar la animación como GIF (requiere Pillow) -----
# from matplotlib.animation import PillowWriter
# gif_path = "bola3d.gif"
# writer = PillowWriter(fps=int(1/dt))
# anim.save(gif_path, writer=writer)
# ---------------------------------------------------------------------
