import os

import pandas as pd
import numpy as np

import autocorrelation_plotter
import histograms_plotter
import increments_plotter
import time_evolution_plotter


def process_artificial_increments(path, num_subcarriers):
    num_samples = 10000
    new_data = generate_artificial_increments(num_subcarriers=num_subcarriers, std_dev=15, num_samples=num_samples)

    if not os.path.exists(os.path.join(path, "increments_hist")):
        os.mkdir(os.path.join(path, "increments_hist"))
    for i in range(num_subcarriers):
        histograms_plotter.plot_histogram_for_sc(i, new_data, num_samples, path)
    time_evolution_plotter.plot_time_evolution_for_sc(new_data, path=path)
    increments_plotter.plot_increments_for_sc(new_data, path=path)
    autocorrelation_plotter.plot_autocorrelation(new_data, path=path)


def generate_artificial_increments(num_subcarriers, std_dev, num_samples=1000):
    # generate a DataFrame with as many columns as num_subcarriers and as many rows as the number of samples
    # each column will contain a series of random numbers (the increments)
    # the random number will be generated using a normal distribution with mean 0 and standard deviation std_dev
    # the increments will be added to the previous value to obtain the new value
    new_data = pd.DataFrame()
    for i in range(num_subcarriers):
        new_data[i] = np.random.normal(0, std_dev, num_samples)
        new_data[i] = new_data[i].cumsum()
    return new_data
