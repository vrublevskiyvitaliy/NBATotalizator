import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization!

import numpy as np
import json


def all_data():
    with open('my_results_2014.json') as data_file:
        data = json.load(data_file)
    return data


def get_x():
    data = all_data()
    data = filter(lambda x: abs(x['k3'] - 0.2) < 0.01, data)
    x = [point['k1'] for point in data]
    return x


def get_y():
    data = all_data()
    data = filter(lambda x: abs(x['k3'] - 0.2) < 0.01, data)
    y = [point['k2'] for point in data]
    return y


def get_z():
    data = all_data()
    data = filter(lambda x: abs(x['k3'] - 0.2) < 0.01, data)
    gain = [point['gain'] for point in data]
    return gain


def get_best_gain():
    data = all_data()
    best = sorted(data, key=lambda x: -x['gain'])[0]
    print(best)


def main():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_axis_bgcolor('green')


    x = get_x()
    y = get_y()

    color = get_z()
    mmin = min(color)
    color = [p - mmin for p in color]
    mmax = max(color)
    color = [p/(1. * mmax) for p in color]

    color = [(p,p,p,1) for p in color]

    # if collor for white - than the z is higher

    ax.scatter(x, y, color = color)
    plt.show()

#main()
get_best_gain()