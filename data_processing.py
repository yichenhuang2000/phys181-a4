import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from spicy import integrate
import dataframe_image as dfi
mpl.use('TkAgg')
g = 9.8
H1 = 0.55
H2 = 0.68
H3 = 0.80
m = 0.24

def read_acceleration(data_file):
    df = pd.read_csv(data_file)
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


def draw_a_v_x_over_t(t, a, v, x, i):
    t = np.array(t)
    a = np.array(a)
    plt.plot(t, a)
    plt.title("acceleration vs time")
    plt.xlabel("time (s)")
    plt.ylabel("accleration (m/s^2)")
    plt.savefig(f'plots/a_t-{i}.png')
    plt.cla()
    plt.plot(t, v)
    plt.title("velocity vs time")
    plt.xlabel("time (s)")
    plt.ylabel("velocity (m/s)")
    plt.savefig(f'plots/v_t-{i}.png')
    plt.cla()
    plt.plot(t, x)
    plt.title("displacement vs time")
    plt.xlabel("time (s)")
    plt.ylabel("displacement (m)")
    plt.savefig(f'plots/x_t-{i}.png')
    plt.cla()


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

def draw_KE_PE_over_t(KE_over_m, PE_over_m, E_sum, t, i):
    KE = np.multiply(KE_over_m, m)
    PE = np.multiply(PE_over_m, m)
    E_sum = np.multiply(E_sum, m)
    plt.plot(t, KE, label='KE')
    plt.plot(t, PE, label='PE')
    plt.plot(t, E_sum, label='KE + PE')
    plt.title("energy vs time")
    plt.xlabel("time (s)")
    plt.ylabel("energy (J)")
    plt.legend()
    plt.savefig(f'plots/E_t-{i}.png')
    plt.cla()



def processing(data_file, H, i):
    df = read_acceleration(data_file)
    t = df['Time (s)'].tolist()
    a = df['Absolute acceleration (m/s^2)'].tolist()
    # print(t)
    # print(a)
    v, x = calculate_velocity_displacement(t, a)
    draw_a_v_x_over_t(t, a, v, x, i)
    KE_over_m = get_KE_over_m(v)
    PE_over_m = get_PE_over_m(H, x)
    SUM = get_potential_sum(KE_over_m, PE_over_m)
    # print(KE_over_m, PE_over_m, SUM)
    draw_KE_PE_over_t(KE_over_m, PE_over_m, SUM, t, i)
    return PE_over_m, KE_over_m

if __name__ == '__main__':
    PE_list = []
    KE_list = []
    for i in range(3):
        i += 1
        PE_over_m, KE_over_m = processing(f'data/Raw Data-{i}.csv', H1, i)
        PE_list.append(PE_over_m[0] * m)
        KE_list.append(KE_over_m[-1] * m)
    for i in range(3):
        i += 4
        PE_over_m, KE_over_m = processing(f'data/Raw Data-{i}.csv', H2, i)

        PE_list.append(PE_over_m[0] * m)
        KE_list.append(KE_over_m[-1] * m)
    for i in range(3):
        i += 7
        PE_over_m, KE_over_m = processing(f'data/Raw Data-{i}.csv', H3, i)
        PE_list.append(PE_over_m[0] * m)
        KE_list.append(KE_over_m[-1] * m)
    diff = [x-y for x, y in zip(PE_list, KE_list)]
    Height = [H1, H1, H1, H2, H2, H2, H3, H3, H3]
    dict = {'Trials': [1,2,3,4,5,6,7,8,9],
            'Height (m)': Height,
            'Initial PE (J)': PE_list,
            'Final KE (J)': KE_list,
            'Difference (J)': diff}

    df = pd.DataFrame(dict).set_index('Trials')
    dfi.export(df, 'outcome1.png')
    PE_mean = []
    KE_mean = []
    diff_mean = []
    diff_sd = []
    for j in range(3):
        D = diff[3*j:3*j+3]
        K = KE_list[3*j:3*j+3]
        KE_mean.append(np.mean(K))
        diff_mean.append(np.mean(D))
        diff_sd.append(np.std(D))
    Height2 = [H1, H2, H3]
    PE_list2 = [PE_list[0],PE_list[3],PE_list[6]]
    dict = {
            'Height (m)': Height2,
            'Initial PE (J)': PE_list2,
            'Final KE mean value (J)': KE_mean,
            'Difference mean value (J)': diff_mean,
            'Difference standard deviation': diff_sd}
    df = pd.DataFrame(dict).set_index('Height (m)')
    dfi.export(df, 'outcome2.png')
    #print(v)
    #print(x)
