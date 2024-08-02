import os

import numpy as np
import pandas as pd

import correlation
import multidim_corr
import quant
from histograms import plot_histogram_for_sc
from increments import plot_increments_for_sc
from plotcsi import plotcsi_quant
from plotwhd import plt_superimposed_whd
from setup import print_menu, set_params, load_data, removeext
from time_evolution import plot_time_evolution_for_sc
from whd import full_whd_matrix

np.random.seed(seed=527302)


def bsc_processing(dforig, dfq, outpath):
    choice = -1
    while choice != 0:
        choice = int(print_menu())
        if choice == 0:  # exit
            pass
        if choice == 1:
            batch_size = len(dforig)
            for x in reversed(range(1, len(dforig))):  # create batches of size x (as long as possible)
                if len(dforig) % x == 0:
                    batch_size = x
                    break
            for title in dforig:
                plot_histogram_for_sc(title, dforig, batch_size, path=outpath)
                # plot_histogram_for_sc(title, df_quant, batch_size, path=os.path.join(dst_folder, "quantized"))
        elif choice == 2:
            # plot_time_evolution_for_sc(df, path=outpath)
            plot_time_evolution_for_sc(dforig, dfq, path=os.path.join(outpath, "quantized"))
        elif choice == 3:
            plot_increments_for_sc(dforig, path=outpath)
        elif choice == 4:
            correlation.save_autocorrelation(dforig, path=outpath)
        elif choice == 5:
            # correlation.save_intercorr(df, path=outpath,
            #                            mode=0)  # plot correlation of increments across adjacent subcarriers
            # correlation.save_intercorr(df, path=outpath,
            #                            mode=1)  # plot correlation of amplitude across subcarriers
            multidim_corr.save_multidimensional_corr(dforig, path=outpath)


if __name__ == '__main__':
    ########## INFORMATION SETUP ##########
    workdir = 'hdf5/'
    csv_file = workdir + 'csi_active_clean.h5'  # file containing the data to be processed
    compdir = 'fourppl/20ax/10min/'
    comparison_file = compdir + 'capture0_4ppl.csv'
    dst_folder = 'hdf5/clean'  # folder path where to save the output of the code, can be an empty string
    BW = 20  # channel bandwidth: 20, 40, 80 MHz
    STD = 'ax'  # modulation: ax, ac
    unneeded_dir = 'dontPlot/unnecessaryPlots' + str(
        BW) + STD  # folder containing the list of sub-carriers to be ignored
    #######################################

    num_sc, colnames, unneeded = set_params(BW, STD, unneeded_dir)

    dirs = [compdir, workdir]
    # dirs = [workdir, compdir, 'oneperson/20ax/10min/']
    dfs = {}
    for d in dirs:
        dfs[d] = {}
        p = os.path.join(os.getcwd(), d)
        for f in os.listdir(d):
            if os.path.isfile(p + f) and (f.endswith('.h5') or f.endswith('.csv')):
                dfs[d][f] = pd.DataFrame(load_data(os.path.join(p, f), colnames, unneeded))

    dfqs = {}
    for k, dframes in dfs.items():  # for each experiment (folder)
        dfqs[k] = {}
        for k1, df in dframes.items():  # for each capture (file in the folder)
            dst_folder = os.path.join(os.getcwd(), k, removeext(k1))

            # NORMALIZATION AND QUANTIZATION
            # plotcsi(df, 10)  # plot 10 random csi
            df_quant, art_incr_quant, incr_quant, q_inc, q_amp, mean_csi, sigma = quant.quant(df, path=dst_folder)
            dfqs[k][k1] = df_quant
            plotcsi_quant(df, df_quant, q_amp=q_amp, n=10, path=dst_folder)

            # bsc_processing(df, df_quant, dst_folder)

    # COMPUTING MUTUAL INFORMATION
    # problist = {}
    # for i in range(-2 ** (q_inc - 1) + 1, 2 ** (q_inc - 1)):
    #     problist[i] = art_incr_quant.count(i) / len(art_incr_quant)
    # int_info = mi.int_mi(df_quant, mean_csi, q_inc, q_amp, problist)

    # COMPUTING WEIGHTED HAMMING DISTANCE
    # whd = whd_int(df_quant, mean_csi2)
    dst_folder = os.path.join(os.getcwd(), "out")
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    whd_std, whd_mean = full_whd_matrix(dfs=dfs,  # passing dfs relative to a single experiment
                                        dfqs=dfqs,  # dictionary containing the quantized data
                                        nsc=num_sc,  # number of subcarriers
                                        q_amp=q_amp,  # quantization level
                                        stddevpath=dst_folder, meanpath=dst_folder)  # path where to save the output

    # PLOTTING
    dfq_plot = []  # TODO: add dataframes to plot
    plt_superimposed_whd(dfqs, dst_folder)
    # plt_whd_boxplot(df_quant, mean_csi, df_quant2, mean_csi2, df_quant3, mean_csi3, dst_folder)
    # plt_whd_violin(df_quant, mean_csi, df_quant2, mean_csi2, df_quant3, mean_csi3, dst_folder)
