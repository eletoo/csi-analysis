import os

import merged_plotter
import parameters_calculator
import std_deviation_and_kurtosis_plotter
from autocorrelation_plotter import plot_autocorrelation
from histograms_plotter import plot_histogram_for_sc
from increments_plotter import plot_increments_for_sc
from time_evolution_plotter import plot_time_evolution_for_sc
from fitting_by_sc import fit_data_by_sc
import scipy.stats as s

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
            if title not in unnecessary_plots:
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

    distributions = {
        "beta": s.beta,
        "cauchy": s.cauchy,
        "chi": s.chi,
        "chi2": s.chi2,
        "dgamma": s.dgamma,
        "f": s.f,
        "foldcauchy": s.foldcauchy,
        "foldnorm": s.foldnorm,
        "gamma": s.gamma,
        "gennorm": s.gennorm,
        "halfcauchy": s.halfcauchy,
        "halfnorm": s.halfnorm,
        "invgauss": s.invgauss,
        "invgamma": s.invgamma,
        "loggamma": s.loggamma,
        "lognorm": s.lognorm,
        "norm": s.norm,
        "powerlaw": s.powerlaw,
        "powerlognorm": s.powerlognorm,
        "powernorm": s.powernorm,
        "rayleigh": s.rayleigh,
        "wrapcauchy": s.wrapcauchy
    }

    response = input("Fit distributions on data and increments? [Y/n]")
    if response.lower() == "y" or response == '':
        fit_data_by_sc(df, distributions)
    if response.lower() == "n":
        pass

    response = input("Elaborate merged data? [Y/n]")
    if response.lower() == "y" or response == '':
        merged_plotter.plot_merged_data(df, distributions)
    if response.lower() == "n":
        pass

    response = input("Calculate variance, skewness and kurtosis for each sub-carrier and for their increments? [Y/n]")
    if response.lower() == "y" or response == '':
        parameters_calculator.calculate_params(df)
    if response.lower() == "n":
        pass

    response = input("Plot standard deviation and kurtosis for the increments? [Y/n]")
    if response.lower() == "y" or response == '':
        std_deviation_and_kurtosis_plotter.plot_std_dev_and_kurtosis(df)
    if response.lower() == "n":
        pass
