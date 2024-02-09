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


def initiate_distributions(complete: bool):
    if complete:
        return {
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
    return {
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


def print_menu():
    print("-------------------------")
    print("0. Exit")
    print("1. Plot magnitude/relative frequency histogram")
    print("2. Plot evolution in time")
    print("3. Plot increment/frequency histogram")
    print("4. Plot auto-correlation function")
    print("5. Fit distributions on data and increments")
    print("6. Plot and fit merged data and their increments")
    print("7. Calculate variance, skewness and kurtosis (for sub-carriers and increments)")
    print("8. Plot standard deviation and kurtosis for increments")
    print("9. Find distribution that best fits the increments of each sub-carrier")
    print("10. Process artificial_increments trace")
    print("11. All of the above")
    print("-------------------------")
    return input("Choose an action: ")


if __name__ == '__main__':
    import pandas as pd

    ########## INFORMATION SETUP ##########
    csv_file = 'csi.csv'  # file containing the data to be processed
    dst_folder = 'csi'  # folder path where to save the output of the code, can be an empty string
    BW = 20  # channel bandwidth: 20, 40, 80 MHz
    STD = 'ax'  # modulation: ax, ac
    #######################################

    distributions = initiate_distributions(True)  # True for complete list of distributions, False for shorter list
    path = os.path.join(os.getcwd(), csv_file)

    num_sc = 3.2 * BW
    if STD == 'ax':
        num_sc = num_sc * 4

    colnames = ["SC" + str(i) for i in range(0, int(num_sc))]
    df = pd.read_csv(path, names=colnames, header=None)

    with open(os.path.join(os.getcwd(), "unnecessaryPlots" + str(BW))) as f:
        unnecessary_plots = f.read().splitlines()

    for title in df:
        if title in unnecessary_plots:
            del df[title]
        else:
            # format complex numbers into readable values
            df[title] = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])

    choice = -1
    while choice != 0:
        choice = int(print_menu())
        if choice == 0:
            pass
        if choice == 1:
            batch_size = len(df)
            for x in reversed(range(1, len(df))):
                if len(df) % x == 0:
                    batch_size = x
                    break
            for title in df:
                plot_histogram_for_sc(title, df, batch_size, path=dst_folder)
        elif choice == 2:
            plot_time_evolution_for_sc(df, path=dst_folder)
        elif choice == 3:
            plot_increments_for_sc(df, path=dst_folder)
        elif choice == 4:
            plot_autocorrelation(df, path=dst_folder)
        elif choice == 5:
            fit_data_by_sc(df, distributions, path=dst_folder)
        elif choice == 6:
            merged_plotter.plot_merged_data(df, distributions, path=dst_folder)
        elif choice == 7:
            parameters_calculator.calculate_params(df, path=dst_folder)
        elif choice == 8:
            std_deviation_and_kurtosis_plotter.plot_std_dev_and_kurtosis(df, path=dst_folder)
        elif choice == 9:
            fitting_by_sc.find_best_dist(df.diff().drop(labels=0, axis=0), distributions,
                                         os.path.join(os.getcwd(), dst_folder))
        elif choice == 10:
            artificial_path = os.path.join(os.getcwd(), dst_folder, 'artificial_increments')
            if not os.path.exists(artificial_path):
                os.mkdir(os.path.join(os.getcwd(), dst_folder, artificial_path))

            if not os.path.exists(os.path.join(dst_folder, 'normal_distribution_info.csv')):
                fitting_by_sc.find_best_dist(df.diff().drop(labels=0, axis=0), distributions,
                                             os.path.join(os.getcwd(), dst_folder))
            file_name = "normal_distribution_info.csv"
            data = pd.read_csv(os.path.join(dst_folder, file_name), header=None)
            std_dev = pd.DataFrame(data.iloc[:, 2].map(lambda x: x.rstrip(')')).astype(float))
            artificial_trace_processor.process_artificial_increments(df.diff(), path=artificial_path,
                                                                     sub_carriers=df.columns,
                                                                     std_dev=std_dev,
                                                                     num_samples=df.shape[0])
        elif choice == 11:
            batch_size = len(df)
            for x in reversed(range(1, len(df))):
                if len(df) % x == 0:
                    batch_size = x
                    break
            for title in df:
                plot_histogram_for_sc(title, df, batch_size, path=dst_folder)
            plot_time_evolution_for_sc(df, path=dst_folder)
            plot_increments_for_sc(df, path=dst_folder)
            plot_autocorrelation(df, path=dst_folder)
            fit_data_by_sc(df, distributions, path=dst_folder)
            merged_plotter.plot_merged_data(df, distributions, path=dst_folder)
            parameters_calculator.calculate_params(df, path=dst_folder)
            std_deviation_and_kurtosis_plotter.plot_std_dev_and_kurtosis(df, path=dst_folder)
            fitting_by_sc.find_best_dist(df.diff().drop(labels=0, axis=0), distributions,
                                         os.path.join(os.getcwd(), dst_folder))
            artificial_path = os.path.join(os.getcwd(), dst_folder, 'artificial_increments')
            if not os.path.exists(artificial_path):
                os.mkdir(os.path.join(os.getcwd(), dst_folder, artificial_path))

            if not os.path.exists(os.path.join(dst_folder, 'normal_distribution_info.csv')):
                fitting_by_sc.find_best_dist(df.diff().drop(labels=0, axis=0), distributions,
                                             os.path.join(os.getcwd(), dst_folder))
            file_name = "normal_distribution_info.csv"
            data = pd.read_csv(os.path.join(dst_folder, file_name), header=None)
            std_dev = pd.DataFrame(data.iloc[:, 2].map(lambda x: x.rstrip(')')).astype(float))
            artificial_trace_processor.process_artificial_increments(df.diff(), path=artificial_path,
                                                                     sub_carriers=df.columns,
                                                                     std_dev=std_dev,
                                                                     num_samples=df.shape[0])

    # if there is not the desired csv file to read, then plot merged data to create it
    if not os.path.exists(os.path.join(dst_folder, 'merged_plot',
                                       'Best five distributions fitting Increments of Merged Data.csv')):
        merged_plotter.plot_merged_data(df, distributions, path=dst_folder)

    # read the csv file (read the five distributions that best fit the merged increments)
    file = open(os.path.join(os.getcwd(), dst_folder, 'merged_plot',
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

    print("Computing and plotting their parameters for each sub-carrier...")
    best_fits_param_calculator.calculate_best_params(df, best_distributions, path=dst_folder)
