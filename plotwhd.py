import os

import numpy as np
from matplotlib import pyplot as plt

from quantize import quantize, mean_csi_comp
from whd import whd


def plt_superimposed_whd(df_quant, df, q_amp, dst_folder, nsc, labels=None):
    if labels is None:
        labels = []
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 2.5)
    ax.set_xlim(0, 0.23)
    # plt.title("Distribution of normalized internal WHD values")
    for i in range(len(df_quant)):
        whds = list(whd(df_quant[i], quantize(mean_csi_comp(df[i]), 0, 2 ** q_amp - 1)).values())
        whds = list([dist / (nsc * (2 ** q_amp) - 1) for dist in whds])
        hist, edges = np.histogram(whds, bins=100)
        plt.plot(edges[:-1], hist / sum(hist), label=labels[i] if i < len(labels) else "#ppl: " + str(i))

    plt.grid()
    plt.xlabel(r'$WHD(A_c, A_c^*)$', fontsize=12)
    plt.ylabel('Relative Frequency', fontsize=12)
    plt.legend()
    # plt.show()
    plt.savefig(os.path.join(dst_folder, "whd_dist_overlapped.pdf"), bbox_inches='tight')
    plt.close()


def plt_whd_boxplot(df_quant, mean_csi, df_quant2, mean_csi2, df_quant3, mean_csi3, dst_folder):
    plt.boxplot([list(whd(df_quant, mean_csi).values()),
                 list(whd(df_quant3, mean_csi3).values()),
                 list(whd(df_quant2, mean_csi2).values())],
                labels=["Empty Room", "One Person", "Four People"],
                flierprops=dict(marker='x', markersize=2))
    plt.ylabel(r'$WHD(A_c, A_c^*)$')
    plt.xlabel('Scenario')
    # plt.show()
    plt.savefig(os.path.join(dst_folder, "whd_boxplot.pdf"))
    plt.close()


def plt_whd_violin(df_quant, mean_csi, df_quant2, mean_csi2, df_quant3, mean_csi3, dst_folder):
    plt.violinplot([list(whd(df_quant, mean_csi).values()),
                    list(whd(df_quant3, mean_csi3).values()),
                    list(whd(df_quant2, mean_csi2).values())],
                   showmedians=True)
    plt.xticks([1, 2, 3], ["Empty Room", "One Person", "Four People"])
    plt.ylabel(r'$WHD(A_c, A_c^*)$')
    plt.xlabel('Scenario')
    plt.savefig(os.path.join(dst_folder, "whd_violinplot.pdf"))
