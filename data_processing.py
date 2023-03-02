import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from spicy import integrate
mpl.use('TkAgg')


def read_acceleration():
    df = pd.read_csv('Acceleration without g 2023-03-01 18-32-06.csv')
    return df

def calculate_velocity_displacement(t, a):
    v = [0]
    x = [0]
    for time_step in range(len(t)-1):
        time_step += 1
        v_t = integrate.simpson(a[:time_step], t[:time_step])
        v.append(v_t)
        x_t = integrate.simpson(v[:time_step], t[:time_step])
        x.append(x_t)
    return v, x


def draw_plot(t, a, v, x):
    t = np.array(t)
    a = np.array(a)
    plt.plot(t, a)
    plt.title("acceleration vs time")
    plt.xlabel("time")
    plt.ylabel("accleration")
    plt.show()
    plt.plot(t, v)
    plt.title("velocity vs time")
    plt.xlabel("time")
    plt.ylabel("velocity")
    plt.show()
    plt.plot(t, x)
    plt.title("displacement vs time")
    plt.xlabel("time")
    plt.ylabel("displacement")
    plt.show()

if __name__ == '__main__':
    df = read_acceleration()
    t = df['t(s)'].tolist()
    a = df['a(m/s²)'].tolist()
    print(t)
    print(a)
    v, x = calculate_velocity_displacement(t, a)
    draw_plot(t, a, v, x)
    print(v)
    print(x)
