import os

import artificial_trace_processor
import best_fits_param_calculator
import fitting_by_sc
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

    ########## INFORMATION SETUP ##########
    csi_name = 'training2_192_168_2_4.csv'  # file containing the data to be processed
    specific_path = "training2_192_168_2_4"  # folder path where to save the output of the code, can be an empty string
    bandwidth = 20  # channel bandwidth: 20, 40, 80 MHz
    #######################################

    path = os.path.join(os.getcwd(), csi_name)

    if bandwidth == 80:
        colnames = ["SC" + str(i) for i in range(0, 256)]
        df = pd.read_csv(path, names=colnames, header=None)
    elif bandwidth == 40:
        colnames = ["SC" + str(i) for i in range(0, 128)]
        df = pd.read_csv(path, names=colnames, header=None)
    elif bandwidth == 20:
        colnames = ["SC" + str(i) for i in range(0, 64)]
        # in our data columns and rows need to be transposed before being processed.
        # if transposing is unneeded use: df = pd.read_csv(path, names=colnames, header=None)
        df = pd.read_csv(path, header=None)
        df = df.transpose()
        df.columns = colnames

    if bandwidth == 80:
        with open(os.path.join(os.getcwd(), "unnecessaryPlots")) as f:
            unnecessary_plots = f.read().splitlines()
    elif bandwidth == 40:
        unnecessary_plots = []
    elif bandwidth == 20:
        unnecessary_plots = ['SC0', 'SC1', 'SC2', 'SC3', 'SC4', 'SC5', 'SC32', 'SC33', 'SC59', 'SC60', 'SC61',
                             'SC62', 'SC63']

    for title in df:
        if title in unnecessary_plots:
            del df[title]
        else:
            df[title] = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])

    response = input("Plot magnitude/relative frequency histogram for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        batch_size = len(df)
        for x in reversed(range(1, len(df))):
            if len(df) % x == 0:
                batch_size = x
                break
        for title in df:
            plot_histogram_for_sc(title, df, batch_size, path=specific_path)

    if response.lower() == "n":
        pass

    response = input("Plot evolution in time for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_time_evolution_for_sc(df, path=specific_path)
    if response.lower() == "n":
        pass

    response = input("Plot increment/frequency histogram for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_increments_for_sc(df, path=specific_path)
    if response.lower() == "n":
        pass

    response = input("Plot auto-correlation function for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_autocorrelation(df, path=specific_path)
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

    distributions = {
        "gamma": s.gamma,  # gamma
        "genextreme": s.genextreme,  # generalized extreme value (weibull+frechét+gumbel)
        "gengamma": s.gengamma,  # generalized gamma
        "genlogistic": s.genlogistic,  # generalized logistic
        "gennorm": s.gennorm,  # generalized normal
        "logistic": s.logistic,  # logistic
        "norm": s.norm,  # normal
        "weibull_max": s.weibull_max,  # inverted weibull distribution
        "weibull_min": s.weibull_min  # actual weibull distribution
    }

    distributions = {"norm": s.norm}

    response = input("Fit distributions on data and increments? [Y/n]")
    if response.lower() == "y" or response == '':
        fit_data_by_sc(df, distributions, path=specific_path)
    if response.lower() == "n":
        pass

    response = input("Plot and fit merged data and their increments? [Y/n]")
    if response.lower() == "y" or response == '':
        merged_plotter.plot_merged_data(df, distributions, path=specific_path)
    if response.lower() == "n":
        pass

    response = input("Calculate variance, skewness and kurtosis for each sub-carrier and for their increments? [Y/n]")
    if response.lower() == "y" or response == '':
        parameters_calculator.calculate_params(df, path=specific_path)
    if response.lower() == "n":
        pass

    response = input("Plot standard deviation and kurtosis for the increments? [Y/n]")
    if response.lower() == "y" or response == '':
        std_deviation_and_kurtosis_plotter.plot_std_dev_and_kurtosis(df, path=specific_path)
    if response.lower() == "n":
        pass

    # if there is not the desired csv file to read, then plot merged data to create it
    if not os.path.exists(os.path.join(specific_path, 'merged_plot',
                                       'Best five distributions fitting Increments of Merged Data.csv')):
        merged_plotter.plot_merged_data(df, distributions, path=specific_path)

    # read the csv file (read the five distributions that best fit the merged increments)
    file = open(os.path.join(os.getcwd(), specific_path, 'merged_plot',
                             'Best five distributions fitting Increments of Merged Data.csv'), "r")
    f = pd.read_csv(file, sep='\t', header=None)

    # take the first column (names of the distributions) - except for the title
    best_dists = f.iloc[:, 0].drop(0)

    best_distributions = {}
    # create a dictionary containing the association (distribution name, scipy distribution) for the five selected
    # distributions

    print("\nThe distributions that best fit the merged increments are: ")
    for dist in best_dists:
        print("-> " + str(dist))
        best_distributions[dist] = distributions[dist]

    response = input("Calculate and plot their parameters for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        best_fits_param_calculator.calculate_best_params(df, best_distributions, path=specific_path)
    if response.lower() == "n":
        pass

    response = input("Find distribution that best fits the increments of each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        fitting_by_sc.find_best_dist(df.diff().drop(labels=0, axis=0), distributions,
                                     os.path.join(os.getcwd(), specific_path))
    if response.lower() == "n":
        pass

    response = input("Process artificial_increments trace? [Y/n]")
    if response.lower() == "y" or response == '':
        artificial_path = os.path.join(os.getcwd(), specific_path, 'artificial_increments')
        if not os.path.exists(artificial_path):
            os.mkdir(os.path.join(os.getcwd(), specific_path, artificial_path))

        if not os.path.exists(os.path.join(specific_path, 'normal_distribution_info.csv')):
            fitting_by_sc.find_best_dist(df.diff().drop(labels=0, axis=0), distributions,
                                         os.path.join(os.getcwd(), specific_path))
        file_name = "normal_distribution_info.csv"
        data = pd.read_csv(os.path.join(specific_path, file_name), header=None)
        std_dev = pd.DataFrame(data.iloc[:, 2].map(lambda x: x.rstrip(')')).astype(float))
        artificial_trace_processor.process_artificial_increments(df.diff(), path=artificial_path,
                                                                 sub_carriers=df.columns,
                                                                 std_dev=std_dev,
                                                                 num_samples=df.shape[0])
    if response.lower() == "n":
        pass
