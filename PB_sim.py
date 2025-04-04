import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# Parámetros del Puzzlebot
R = 0.05  # Radio de las ruedas (m)
L = 0.18  # Distancia entre ruedas (m)

def cinematica_directa(w_r, w_l, x, y, theta, dt):
    v = R * (w_r + w_l) / 2
    w = R * (w_r - w_l) / L
    x += v * np.cos(theta) * dt
    y += v * np.sin(theta) * dt
    theta += w * dt
    return x, y, theta

def cinematica_inversa(v, w):
    w_r = (2 * v + w * L) / (2 * R)
    w_l = (2 * v - w * L) / (2 * R)
    return w_r, w_l

def calcular_velocidades(xf, yf, t_final):
    v = np.sqrt(xf**2 + yf**2) / t_final
    w = np.arctan2(yf, xf) / t_final
    return v, w

def simular(v, w):
    dt = 0.1
    t_final = 10  # Aumentado el tiempo de simulación
    x, y, theta = 0.0, 0.0, 0.0  # Posición inicial
    x_data, y_data, theta_data = [], [], []
    w_r_data, w_l_data = [], []
    theta_w_r, theta_w_l = 0, 0
    theta_w_r_data, theta_w_l_data = [], []

    for t in np.arange(0, t_final, dt):
        w_r, w_l = cinematica_inversa(v, w)
        x, y, theta = cinematica_directa(w_r, w_l, x, y, theta, dt)
        x_data.append(x)
        y_data.append(y)
        theta_data.append(theta)
        w_r_data.append(w_r)
        w_l_data.append(w_l)
        theta_w_r += w_r * dt
        theta_w_l += w_l * dt
        theta_w_r_data.append(theta_w_r)
        theta_w_l_data.append(theta_w_l)
    
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))
    axs[0].plot(x_data, y_data, label="Trayectoria del Puzzlebot")
    axs[0].set_xlabel("Posición en X (m)")
    axs[0].set_ylabel("Posición en Y (m)")
    axs[0].set_title("Movimiento del Puzzlebot")
    axs[0].legend()
    axs[0].grid()
    
    axs[1].plot(np.arange(0, t_final, dt), theta_w_r_data, label="Ángulo total rueda derecha")
    axs[1].plot(np.arange(0, t_final, dt), theta_w_l_data, label="Ángulo total rueda izquierda")
    axs[1].set_xlabel("Tiempo (s)")
    axs[1].set_ylabel("Ángulo total (rad)")
    axs[1].set_title("Evolución del ángulo total de giro de las ruedas")
    axs[1].legend()
    axs[1].grid()
    
    axs[2].plot(np.arange(0, t_final, dt), w_r_data, label="Velocidad rueda derecha")
    axs[2].plot(np.arange(0, t_final, dt), w_l_data, label="Velocidad rueda izquierda")
    axs[2].set_xlabel("Tiempo (s)")
    axs[2].set_ylabel("Velocidad angular (rad/s)")
    axs[2].set_title("Cinemática inversa: Velocidades de las ruedas")
    axs[2].legend()
    axs[2].grid()
    
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([0, 2])  # Expandido el rango
    ax.set_ylim([0, 2])
    ax.set_zlim([0, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("Animación del Puzzlebot")

    carrito, = ax.plot([], [], [], 'ro', markersize=8)
    trayectoria, = ax.plot([], [], [], 'b-', linewidth=2)

    def update(num):
        carrito.set_data([x_data[num]], [y_data[num]])
        carrito.set_3d_properties([0.05])  # Altura fija
        trayectoria.set_data(x_data[:num+1], y_data[:num+1])
        trayectoria.set_3d_properties([0.05] * (num+1))
        return carrito, trayectoria
    
    ani = animation.FuncAnimation(fig, update, frames=len(x_data), interval=100, blit=False)
    plt.show()

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Simulación del Puzzlebot")

tk.Label(root, text="Velocidad lineal v (m/s):").grid(row=0, column=0)
v_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
v_slider.grid(row=0, column=1)
v_slider.set(0.2)

tk.Label(root, text="Velocidad angular w (rad/s):").grid(row=1, column=0)
w_slider = tk.Scale(root, from_=-1, to=1, resolution=0.01, orient=tk.HORIZONTAL)
w_slider.grid(row=1, column=1)
w_slider.set(0.5)

tk.Label(root, text="Posición final X (m):").grid(row=2, column=0)
xf_entry = tk.Entry(root)
xf_entry.grid(row=2, column=1)

tk.Label(root, text="Posición final Y (m):").grid(row=3, column=0)
yf_entry = tk.Entry(root)
yf_entry.grid(row=3, column=1)

def simular_desde_coordenadas():
    try:
        xf = float(xf_entry.get())
        yf = float(yf_entry.get())
        v, w = calcular_velocidades(xf, yf, 10)
        simular(v, w)
    except ValueError:
        print("Ingrese valores válidos para las coordenadas finales.")

btn_simular_vw = tk.Button(root, text="Simular con v y w", command=lambda: simular(v_slider.get(), w_slider.get()))
btn_simular_vw.grid(row=4, column=0, columnspan=2)

btn_simular_coord = tk.Button(root, text="Simular con coordenadas", command=simular_desde_coordenadas)
btn_simular_coord.grid(row=5, column=0, columnspan=2)

root.mainloop()
