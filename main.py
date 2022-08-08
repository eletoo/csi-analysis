import os

import merged_plotter
import parameters_calculator
from autocorrelation_plotter import plot_autocorrelation
from histograms_plotter import plot_histogram_for_sc
from increments_plotter import plot_increments_for_sc
from time_evolution_plotter import plot_time_evolution_for_sc
from fitting_by_sc import fit_by_sc

if __name__ == '__main__':
    import pandas as pd

    path = os.getcwd() + '\\csi.csv'

    colnames = ["SC" + str(i) for i in range(0, 256)]
    df = pd.read_csv(path, names=colnames, header=None)

    with open(os.getcwd() + "\\unnecessaryPlots") as f:
        unnecessary_plots = f.read().splitlines()

    for title in df:
        if title in unnecessary_plots:
            del df[title]
        else:
            df[title] = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])

    response = input("Plot magnitude/relative frequency histogram for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        for title in colnames:
            plot_histogram_for_sc(title, df)
    if response.lower() == "n":
        pass

    response = input("Plot evolution in time for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_time_evolution_for_sc(df)
    if response.lower() == "n":
        pass

    response = input("Plot increment/frequency histogram for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_increments_for_sc(df)
    if response.lower() == "n":
        pass

    response = input("Plot auto-correlation function for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_autocorrelation(df)
    if response.lower() == "n":
        pass

    response = input("Fit distributions? [Y/n]")
    if response.lower() == "y" or response == '':
        fit_by_sc(df, unnecessary_plots)
    if response.lower() == "n":
        pass

    response = input("Plot merged data? [Y/n]")
    if response.lower() == "y" or response == '':
        merged_plotter.plot_merged_data(df)
    if response.lower() == "n":
        pass

    parameters_calculator.calculate_params(df)
