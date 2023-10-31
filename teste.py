import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Crie uma figura e um eixo
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], lw=2)

# Função de inicialização
def init():
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1, 1)
    return line,

# Função de animação
def animate(frame):
    x_data.append(frame)
    y_data.append(np.sin(frame))
    line.set_data(x_data, y_data)
    return line,

# Crie a animação
ani = FuncAnimation(fig, animate, frames=np.linspace(0, 2 * np.pi, 128), init_func=init, blit=True)

# Exiba a animação
plt.show()
