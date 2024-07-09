import os

import numpy as np
import pandas as pd

import correlation
import multidim_corr
import quant
from histograms import plot_histogram_for_sc
from increments import plot_increments_for_sc
from plotcsi import plotcsi_quant
from time_evolution import plot_time_evolution_for_sc
from whd import whd_int

np.random.seed(seed=527302)


def print_menu():
    """
    :return: choice from the user
    """
    print("-------------------------")
    print("0. Exit")
    print("1. Plot magnitude/relative frequency histogram")
    print("2. Plot evolution in time")
    print("3. Plot increment/frequency histogram")
    print("4. Plot auto-correlation function")
    # print("5. Plot inter-SC correlation")
    print("5. Plot multidimensional correlation")
    print("6. Compute mutual information")
    print("-------------------------")
    return input("Choose an action: ")


if __name__ == '__main__':

    ########## INFORMATION SETUP ##########
    csv_file = 'emptyroom/20ax/capture0.csv'  # file containing the data to be processed
    dst_folder = 'emptyroom/capture0'  # folder path where to save the output of the code, can be an empty string
    BW = 20  # channel bandwidth: 20, 40, 80 MHz
    STD = 'ax'  # modulation: ax, ac
    unneeded_dir = 'dontPlot/unnecessaryPlots' + str(
        BW) + STD  # folder containing the list of sub-carriers to be ignored
    #######################################

    path = os.path.join(os.getcwd(), csv_file)

    num_sc = 3.2 * BW
    if STD == 'ax':
        num_sc = num_sc * 4

    colnames = ["SC" + str(i) for i in range(0, int(num_sc))]
    df = pd.read_csv(path, names=colnames, header=None)

    with open(os.path.join(os.getcwd(), unneeded_dir)) as f:
        unneeded = f.read().splitlines()

    for title in df:
        if title in unneeded:
            del df[title]
        else:
            # format complex numbers into readable values
            df[title] = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])

    # removing impact of AGC on data
    for index, row in df.iterrows():
        # each row is a time sample over the sub-carriers (frequencies)
        # compute the mean amplitude over the frequencies and normalize the values by it (i.e. by the energy of the CSI)
        mean = row.mean()
        df.iloc[index] = row / mean

    # plotcsi(df, 10)  # plot 10 random csi
    df_quant, art_incr_quant, incr_quant, q_inc, q_amp, mean_csi, sigma = quant.quant(df,
                                                                                      path=dst_folder)  # normalize data and quantize
    plotcsi_quant(df, df_quant, q_amp=q_amp, n=10, path=dst_folder)  # plot 10 random csi and their quantized version

    # problist = {}
    # for i in range(-2 ** (q_inc - 1) + 1, 2 ** (q_inc - 1)):
    #     problist[i] = art_incr_quant.count(i) / len(art_incr_quant)
    # int_info = mi.int_mi(df_quant, mean_csi, q_inc, q_amp, problist)

    whd = whd_int(df_quant, mean_csi)

    choice = -1
    while choice != 0:
        choice = int(print_menu())
        if choice == 0:  # exit
            pass
        if choice == 1:
            batch_size = len(df)
            for x in reversed(range(1, len(df))):  # create batches of size x (as long as possible)
                if len(df) % x == 0:
                    batch_size = x
                    break
            for title in df:
                plot_histogram_for_sc(title, df, batch_size, path=dst_folder)
                # plot_histogram_for_sc(title, df_quant, batch_size, path=os.path.join(dst_folder, "quantized"))
        elif choice == 2:
            # plot_time_evolution_for_sc(df, path=dst_folder)
            plot_time_evolution_for_sc(df, df_quant, path=os.path.join(dst_folder, "quantized"))
        elif choice == 3:
            plot_increments_for_sc(df, path=dst_folder)
        elif choice == 4:
            correlation.save_autocorrelation(df, path=dst_folder)
        elif choice == 5:
            # correlation.save_intercorr(df, path=dst_folder,
            #                            mode=0)  # plot correlation of increments across adjacent subcarriers
            # correlation.save_intercorr(df, path=dst_folder,
            #                            mode=1)  # plot correlation of amplitude across subcarriers
            multidim_corr.save_multidimensional_corr(df, path=dst_folder)
        elif choice == 6:
            pass
            # mutual_info.save_mutual_info(df, path=dst_folder)
