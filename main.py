import os

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

    response = input("Plot magnitude/relative frequency histogram for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        for title in colnames:
            plot_histogram_for_sc(title, df, unnecessary_plots)
    if response.lower() == "n":
        pass

    response = input("Plot evolution in time for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_time_evolution_for_sc(df, unnecessary_plots)
    if response.lower() == "n":
        pass

    response = input("Plot increment/frequency histogram for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_increments_for_sc(df, unnecessary_plots)
    if response.lower() == "n":
        pass

    response = input("Plot auto-correlation function for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_autocorrelation(df, unnecessary_plots)
    if response.lower() == "n":
        pass

    response = input("Fit distributions? [Y/n]")
    if response.lower() == "y" or response == '':
        fit_by_sc(df, unnecessary_plots)
    if response.lower() == "n":
        pass
