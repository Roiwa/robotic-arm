"""
Programa: pendulo_invertido.py
Descripción:
    Simula un péndulo colgante sobre un carro en 2D.
    El carro y el péndulo comienzan completamente quietos.
    El usuario solo puede aplicar velocidad horizontal (izquierda/derecha).
Controles:
    ← : mueve el carro a la izquierda
    → : mueve el carro a la derecha
    ESPACIO : pausa/reanuda la simulación
Requisitos:
    pip install pygame
"""

import pygame
import math
import sys

# Inicializar pygame
pygame.init()

# Parámetros de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Péndulo sobre carro (inicio en reposo)")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
AZUL = (0, 0, 200)

# Parámetros físicos
dt = 0.02               # paso de tiempo (s)
g = 9.81                # gravedad (m/s²)
L = 1.0                 # longitud del péndulo (m)
m = 0.1                 # masa del péndulo (kg)
M = 1.0                 # masa del carro (kg)
x = 0.0                 # posición inicial del carro
x_dot = 0.0             # velocidad inicial del carro
theta = 0.0             # ángulo inicial del péndulo (0 = hacia abajo)
theta_dot = 0.0         # velocidad angular inicial

# Escala para dibujo
escala = 200
origen = (ANCHO // 2, ALTO // 2 + 150)

# Control
vel_control = 0.0
paused = False

# Reloj
clock = pygame.time.Clock()

def dinamica(x, x_dot, theta, theta_dot, F):
    """Ecuaciones del movimiento del péndulo sobre carro."""
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    denom = M + m * sin_t**2

    # Dinámica linealizada (para el péndulo colgante)
    x_ddot = (F + m * sin_t * (L * theta_dot**2 - g * cos_t)) / denom
    theta_ddot = (-F * cos_t - m * L * theta_dot**2 * cos_t * sin_t + (M + m) * g * sin_t) / (L * denom)
    return x_ddot, theta_ddot

def dibujar(x, theta):
    ventana.fill(BLANCO)

    # Posición del carro
    carro_x = origen[0] + int(x * escala)
    carro_y = origen[1]
    ancho_carro = 80
    alto_carro = 30
    pygame.draw.rect(ventana, AZUL, (carro_x - ancho_carro//2, carro_y - alto_carro//2, ancho_carro, alto_carro))

    # Posición del péndulo (colgante)
    px = carro_x + int(L * escala * math.sin(theta))
    py = carro_y + int(L * escala * math.cos(theta))
    pygame.draw.line(ventana, NEGRO, (carro_x, carro_y), (px, py), 4)
    pygame.draw.circle(ventana, ROJO, (px, py), 10)

    pygame.display.flip()

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                vel_control = -10
            elif evento.key == pygame.K_RIGHT:
                vel_control = 10
            elif evento.key == pygame.K_DOWN:
                vel_control = 0
            elif evento.key == pygame.K_SPACE:
                paused = not paused
        elif evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                vel_control = 0

    if not paused:
        F = vel_control
        x_ddot, theta_ddot = dinamica(x, x_dot, theta, theta_dot, F)

        # Integración simple (Euler)
        x_dot += x_ddot * dt
        x += x_dot * dt
        theta_dot += theta_ddot * dt
        theta += theta_dot * dt

    dibujar(x, theta)
    clock.tick(60)
