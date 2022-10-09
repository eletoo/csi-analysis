import os

import pandas as pd
import numpy as np

import autocorrelation_plotter
import histograms_plotter
import increments_plotter
import time_evolution_plotter


def process_artificial_increments(real_increments, path, sub_carriers, std_dev, num_samples=1000):
    new_data = generate_artificial_increments(sub_carriers=sub_carriers, std_dev=std_dev, num_samples=num_samples)

    if not os.path.exists(os.path.join(path, "increments_hist")):
        os.mkdir(os.path.join(path, "increments_hist"))
    for title in sub_carriers:
        histograms_plotter.plot_histogram_for_sc(title, new_data, num_samples, path)
    time_evolution_plotter.plot_time_evolution_for_sc(new_data, path=path)
    increments_plotter.plot_superimposed_increments(real_increments, new_data, path=path)
    autocorrelation_plotter.plot_autocorrelation(new_data, path=path)


def generate_artificial_increments(sub_carriers, std_dev, num_samples=1000):
    new_data = pd.DataFrame()
    i = 0
    for title in sub_carriers:
        new_data[title] = np.random.normal(0, std_dev[2][i], num_samples)
        new_data[title] = new_data[title].cumsum()
        i += 1
    return new_data
