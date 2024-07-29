import os

import numpy as np
from matplotlib import pyplot as pl

import quant


def plot_time_evolution_for_sc(df, df_quant, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "time_evolution")):
        os.mkdir(os.path.join(path, "time_evolution"))
    df = quant.normalize(df)
    for title in df:
        fig, ax1 = pl.subplots()
        ax2 = ax1.twinx()
        ax1.plot(df[title], label="Normalized", color='r')
        ax2.plot(df_quant[title], label="Quantized", color='b', linewidth=0.5)
        ax1.set_xlabel("CSI index")
        pl.ylabel("Amplitude")
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax1.set_ylim([0, df.max().max() * 1.1])
        ax2.set_ylim([0, df_quant.max().max() * 1.1])
        ax1.grid()
        pl.title(title)
        pl.rcParams.update({'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large',
                            'ytick.labelsize': 'large'})
        pl.savefig(os.path.join(os.getcwd(), path, 'time_evolution', 'figure' + str(title) + '.pdf'))
        pl.close()
        print("plotting graph " + str(title))
