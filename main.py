import os
import pickle
from time import sleep

import numpy as np
import pandas as pd
from tqdm import tqdm

import correlation
import multidim_corr
import quantize
import whd
from hdf2df import hdf2csv
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

    print("\n\nMake sure you have run the 'clean' script before running this one to remove spurious data.", end="\n\n")
    sleep(3)

    ########## INFORMATION SETUP ##########
    dirs = [
        "80ax/0ppl/",
    ]  # folders containing the data
    BWS = [20, 40, 80]  # channel bandwidth: 20, 40, 80 MHz
    STD = 'ax'  # modulation: ax, ac
    #######################################

    if os.path.exists('preloaded/q_amp.pickle') and os.path.exists('preloaded/dfs.pickle') and os.path.exists(
            'preloaded/dirs.pickle'):
        # load variables from file
        with open('preloaded/q_amp.pickle', 'rb') as f:
            q_amp = pickle.load(f)
        with open('preloaded/dfs.pickle', 'rb') as f1:
            dfs = pickle.load(f1)
        with open('preloaded/dirs.pickle', 'rb') as f2:
            dirs = pickle.load(f2)
        with open('preloaded/dfqs.pickle', 'rb') as f3:
            dfqs = pickle.load(f3)
    else:
        if not os.path.exists('preloaded'):
            os.makedirs('preloaded')

        q_amp = 8
        dfs = {}
        for bw in BWS:
            unneeded_dir = 'dontPlot/unnecessaryPlots' + str(bw) + STD  # list of suppressed sub-carriers
            num_sc, colnames, unneeded = set_params(bw, STD, unneeded_dir)

            print("\nLoading data at " + str(bw) + "MHz...\n")
            dirs1 = [di for di in dirs if str(bw) in di]
            for d in tqdm(dirs1, colour="red"):
                dfs[d] = {}
                p = os.path.join(os.getcwd(), d)
                for f in os.listdir(d):
                    if os.path.isfile(p + f) and f.endswith('.h5'):  # only hdf5 files from antisense project
                        hdf2csv(os.path.join(p, f), d)  # convert hdf5 to csv
                    elif os.path.isfile(p + f) and f.endswith('.csv'):
                        dfs[d][f] = pd.DataFrame(load_data(os.path.join(p, f), colnames, unneeded))  # load data

        for k, dframes in tqdm(dfs.items(), colour="red"):  # for each experiment (folder)
            for k1, df in dframes.items():  # for each capture (file in the folder)
                q_ampl, _, _, _ = quantize.compute_qamp(df, path=os.path.join(os.getcwd(), k, removeext(k1)))
                if q_ampl > q_amp:
                    q_amp = q_ampl

        print("Amplitude quantization level: " + str(q_amp) + " bits")

        print("\nQuantizing data...\n")
        dfqs = {}
        for k, dframes in tqdm(dfs.items(), colour="red"):  # for each experiment (folder)
            dfqs[k] = {}
            for k1, df in dframes.items():  # for each capture (file in the folder)
                dst_folder = os.path.join(os.getcwd(), k, removeext(k1))

                # NORMALIZATION AND QUANTIZATION
                df1, df_quant, mean_csi = quantize.quant(df, q_amp, path=dst_folder)
                dfs[k][k1] = df1  # normalized data
                dfqs[k][k1] = df_quant  # quantized data
                # plotcsi(df1, 10)  # plot 10 random csi
                plotcsi_quant(df1, df_quant, q_amp=q_amp, n=10, path=dst_folder)
                # bsc_processing(df1, df_quant, dst_folder)

        with open('preloaded/q_amp.pickle', 'wb') as f:
            pickle.dump(q_amp, f)
        with open('preloaded/dfs.pickle', 'wb') as f1:
            pickle.dump(dfs, f1)
        with open('preloaded/dirs.pickle', 'wb') as f2:
            pickle.dump(dirs, f2)
        with open('preloaded/dfqs.pickle', 'wb') as f3:
            pickle.dump(dfqs, f3)

    # COMPUTING MUTUAL INFORMATION - NOT USING IT FOR NOW (N.B. NOT REFACTORED)
    # problist = {}
    # for i in range(-2 ** (q_inc - 1) + 1, 2 ** (q_inc - 1)):
    #     problist[i] = art_incr_quant.count(i) / len(art_incr_quant)
    # int_info = mi.int_mi(df_quant, mean_csi, q_inc, q_amp, problist)

    BW = int(input("Bandwidth to analyze (20, 40, 80): "))
    unneeded_dir = 'dontPlot/unnecessaryPlots' + str(BW) + STD
    num_sc, colnames, unneeded = set_params(BW, STD, unneeded_dir)
    dirs = [di for di in dirs if str(BW) in di]
    print("\nLoading data at " + str(BW) + "MHz...\n")

    keys = []
    for k, v in dfs.items():
        if k not in dirs:
            keys.append(k)
    for k in keys:
        dfs.pop(k)
        dfqs.pop(k)

    # COMPUTING WEIGHTED HAMMING DISTANCE
    print("\nComputing WHD for " + str(BW) + " MHz...\n")
    dst_folder = os.path.join(os.getcwd(), str(BW) + STD + "/out")
    # dst_folder = os.path.join(os.getcwd(), "20hdf5" + "/out")
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    whd_std, whd_mean = full_whd_matrix(dfs=dfs,  # dictionary containing the normalized CSIs
                                        dfqs=dfqs,  # dictionary containing the quantized CSIs
                                        nsc=num_sc,  # number of subcarriers
                                        q_amp=q_amp,  # quantization level
                                        stddevpath=dst_folder,  # path where to save the output
                                        meanpath=dst_folder)

    # heatmap(dfqs)

    # COMPUTING MINIMUM DISTANCE
    # mindist = mindist(dfqs, nsc=num_sc, q_amp=q_amp, mindistpath=dst_folder)

    # PLOTTING
    dfq_plot = [
        dfqs['80ax/0ppl/']['capture1.csv'],
        dfqs['80ax/0ppl/']['capture2.csv'],

    ]
    dfs_plot = [
        dfs['80ax/0ppl/']['capture1.csv'],
        dfs['80ax/0ppl/']['capture2.csv'],
    ]
    plt_superimposed_whd(dfq_plot, dfs_plot, q_amp, dst_folder, num_sc, labels=None)
