import csv
import os

import numpy as np

import correlation
import multidim_corr
import quant
from histograms import plot_histogram_for_sc
from increments import plot_increments_for_sc
from plotcsi import plotcsi_quant
from setup import print_menu, set_params, load_data
from time_evolution import plot_time_evolution_for_sc
from whd import whd_matrix, cross_whd_matrix

np.random.seed(seed=527302)


def save_whd(path, outfile, idata):
    global f, wr
    with open(path + outfile, "w") as f:
        wr = csv.writer(f, delimiter="\t")
        wr.writerows(idata)


if __name__ == '__main__':

    ########## INFORMATION SETUP ##########
    workdir = 'emptyroom/20ax/10min/'
    csv_file = workdir + 'capture0_empty.csv'  # file containing the data to be processed
    compdir = 'fourppl/20ax/10min/'
    comparison_file = compdir + 'capture0_4ppl.csv'
    dst_folder = 'emptyroom/capture0'  # folder path where to save the output of the code, can be an empty string
    BW = 20  # channel bandwidth: 20, 40, 80 MHz
    STD = 'ax'  # modulation: ax, ac
    unneeded_dir = 'dontPlot/unnecessaryPlots' + str(
        BW) + STD  # folder containing the list of sub-carriers to be ignored
    #######################################

    num_sc, colnames, unneeded = set_params(BW, STD, unneeded_dir)

    path = os.path.join(os.getcwd(), csv_file)
    path_comp = os.path.join(os.getcwd(), comparison_file)

    df = load_data(path, colnames, unneeded)
    df_comp = load_data(path_comp, colnames, unneeded)

    # NORMALIZATION AND QUANTIZATION
    # plotcsi(df, 10)  # plot 10 random csi
    df_quant, art_incr_quant, incr_quant, q_inc, q_amp, mean_csi, sigma = quant.quant(df, path=dst_folder)
    plotcsi_quant(df, df_quant, q_amp=q_amp, n=10, path=dst_folder)  # plot 10 random csi and their quantized version

    df_quant_comp, art_incr_quant_comp, incr_quant_comp, q_inc_comp, q_amp_comp, mean_csi_comp, sigma_comp = quant.quant(
        df_comp,
        path=dst_folder)

    # COMPUTING MUTUAL INFORMATION
    # problist = {}
    # for i in range(-2 ** (q_inc - 1) + 1, 2 ** (q_inc - 1)):
    #     problist[i] = art_incr_quant.count(i) / len(art_incr_quant)
    # int_info = mi.int_mi(df_quant, mean_csi, q_inc, q_amp, problist)

    # COMPUTING WEIGHTED HAMMING DISTANCE
    # whd = whd_int(df_quant, mean_csi_comp)
    whd_std_work, whd_mean_work = whd_matrix(workdir=workdir, unneeded=unneeded, colnames=colnames,
                                             dst_folder=dst_folder,
                                             q_amp=q_amp)
    save_whd(dst_folder, "/whd_std.txt", whd_std_work)
    save_whd(dst_folder, "/whd_mean.txt", whd_mean_work)

    whd_std_comp, whd_mean_comp = whd_matrix(workdir=compdir, unneeded=unneeded, colnames=colnames,
                                             dst_folder=dst_folder,
                                             q_amp=q_amp)
    save_whd(dst_folder, "/whd_std_1.txt", whd_std_comp)
    save_whd(dst_folder, "/whd_mean_1.txt", whd_mean_comp)

    cross_whd_std, cross_whd_mean = cross_whd_matrix(workdir, compdir, unneeded=unneeded, colnames=colnames,
                                                     q_amp=q_amp)
    save_whd(dst_folder, "/whd_std_compared.txt", cross_whd_std)
    save_whd(dst_folder, "/whd_mean_compared.txt", cross_whd_mean)

    cross_whd_std1, cross_whd_mean1 = cross_whd_matrix(compdir, workdir, unneeded=unneeded, colnames=colnames,
                                                       q_amp=q_amp)
    save_whd(dst_folder, "/whd_std_compared1.txt", cross_whd_std1)
    save_whd(dst_folder, "/whd_mean_compared1.txt", cross_whd_mean1)

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
