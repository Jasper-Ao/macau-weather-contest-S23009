import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import pandas as pd

pm25_df = pd.read_csv('data/PM2.5 data.csv')
pm10_df = pd.read_csv('data/PM10 data.csv')
o3_df = pd.read_csv('data/O3 data.csv')


class data_storage:
    def __init__(self, x,y, xlim,ylim, ylabel_name) -> None:
        self.x = x
        self.y = y

        self.m, self.b = np.polyfit(x,y, 1)

        self.xlim = xlim
        self.ylim = ylim

        self.ylabel_name = ylabel_name

pm25_s = data_storage(pm25_df.index, pm25_df.value, 5,30, 'PM2.5 (μg/m3)')
pm10_s = data_storage(pm10_df.index, pm10_df.value, 25,55, 'PM10 (μg/m3)')
o3_s = data_storage(o3_df.index, o3_df.value, 70,130, 'O3 (ppb)')

# choose the data here
storage = pm25_s

# 0 = linear regression, 1 = nonlinear regression
mode = 0


def quadratic_func(x, a, b, c):
    return a + b * x + c * x**2

popt, pcov = curve_fit(quadratic_func, storage.x, storage.y)


plt.ylim(storage.xlim, storage.ylim)
plt.xlabel('time interval (30s)')
plt.ylabel(storage.ylabel_name)

if mode == 0:
    plt.plot(storage.x, storage.y, 'b', storage.x, storage.m*storage.x + storage.b, 'r')
elif mode == 1:
    plt.plot(storage.x, storage.y, 'b', storage.x, quadratic_func(storage.x, *popt), 'r')

plt.show()