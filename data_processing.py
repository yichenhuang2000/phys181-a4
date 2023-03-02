import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from spicy import integrate
mpl.use('TkAgg')
g = 9.8

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


def draw_a_v_x_over_t(t, a, v, x):
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


def get_KE_over_m(v):
    return np.divide(np.power(v,2),2)


def get_PE_over_m(H, x):
    x = np.array(x)
    H_array = np.empty(len(x))
    H_array.fill(H)
    h = H_array-x
    return g*h


def get_potential_sum(KE, PE):
    return KE+PE

def draw_KE_PE_over_t(KE, PE,E_sum, t):
    KE = np.array(KE)
    PE = np.array(PE)
    E_sum = np.array(E_sum)
    plt.plot(t, KE, label='KE / m')
    plt.plot(t, PE, label='PE / m')
    plt.plot(t, E_sum, label='(KE + PE) / m')
    plt.title("energy vs time")
    plt.xlabel("time")
    plt.ylabel("energy per kilo")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    df = read_acceleration()
    t = df['t(s)'].tolist()
    a = df['a(m/s²)'].tolist()
    #print(t)
    #print(a)
    v, x = calculate_velocity_displacement(t, a)
    draw_a_v_x_over_t(t, a, v, x)
    KE_over_m = get_KE_over_m(v)
    PE_over_m = get_PE_over_m(1.32, x)
    SUM = get_potential_sum(KE_over_m, PE_over_m)
    #print(KE_over_m, PE_over_m, SUM)
    draw_KE_PE_over_t(KE_over_m, PE_over_m, SUM, t)

    #print(v)
    #print(x)
