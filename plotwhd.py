import os

from matplotlib import pyplot as plt

from whd import whd_int


def plt_superimposed_whd(df_quant, mean_csi, df_quant2, mean_csi2, df_quant3, mean_csi3, dst_folder):
    plt.title("Distribution of WHD values")
    plt.hist(whd_int(df_quant, mean_csi).values(), bins=100, label="Empty Room", alpha=0.5)
    plt.hist(whd_int(df_quant3, mean_csi3).values(), bins=100, label="One Person", alpha=0.5)
    plt.hist(whd_int(df_quant2, mean_csi2).values(), bins=100, label="Four People", alpha=0.5)
    plt.grid()
    plt.xlabel(r'$WHD(A_c, A_c^*)$')
    plt.ylabel('Frequency')
    plt.legend()
    # plt.show()
    plt.savefig(os.path.join(dst_folder, "whd_dist_overlapped.pdf"))
    plt.close()


def plt_whd_boxplot(df_quant, mean_csi, df_quant2, mean_csi2, df_quant3, mean_csi3, dst_folder):
    plt.boxplot([list(whd_int(df_quant, mean_csi).values()),
                 list(whd_int(df_quant3, mean_csi3).values()),
                 list(whd_int(df_quant2, mean_csi2).values())],
                labels=["Empty Room", "One Person", "Four People"],
                flierprops=dict(marker='x', markersize=2))
    plt.ylabel(r'$WHD(A_c, A_c^*)$')
    plt.xlabel('Scenario')
    # plt.show()
    plt.savefig(os.path.join(dst_folder, "whd_boxplot.pdf"))
    plt.close()


def plt_whd_violin(df_quant, mean_csi, df_quant2, mean_csi2, df_quant3, mean_csi3, dst_folder):
    plt.violinplot([list(whd_int(df_quant, mean_csi).values()),
                    list(whd_int(df_quant3, mean_csi3).values()),
                    list(whd_int(df_quant2, mean_csi2).values())],
                   showmedians=True)
    plt.xticks([1, 2, 3], ["Empty Room", "One Person", "Four People"])
    plt.ylabel(r'$WHD(A_c, A_c^*)$')
    plt.xlabel('Scenario')
    plt.savefig(os.path.join(dst_folder, "whd_violinplot.pdf"))
