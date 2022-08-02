import os

from histograms_plotter import plot_histogram_for_sc
from increments_plotter import plot_increments_for_sc
from time_evolution_plotter import plot_time_evolution_for_sc

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
