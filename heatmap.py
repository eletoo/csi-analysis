import gc
import os

import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm


def heatmap(dfqs):
    q = 0
    for k, v in tqdm(dfqs.items(), colour="green"):  # for each folder
        i = 0
        for k1, v1 in v.items():  # for each capture
            l = 0
            for k2, v2 in dfqs.items():  # for each folder
                j = 0
                for k3, v3 in v2.items():  # for each capture
                    df1 = v1
                    df2 = v3

                    if v1.shape[0] > v3.shape[0]:
                        df1 = v1.iloc[:v3.shape[0], :]
                    elif v1.shape[0] < v3.shape[0]:
                        df2 = v3.iloc[:v1.shape[0], :]
                    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(13, 10))
                    sns.heatmap(df1.T, ax=ax1, cmap='coolwarm', cbar=True, xticklabels=False,
                                cbar_kws={'label': 'Amplitude'})
                    ax1.set_ylabel('Sub-carrier Index', fontsize=8)
                    ax1.set_xlabel('CSI Index', fontsize=8)
                    ax1.set_title('Heatmap of Experiment ' + k + k1, fontsize=12)

                    sns.heatmap(df2.T, ax=ax2, cmap='coolwarm', cbar=True, xticklabels=False,
                                cbar_kws={'label': 'Amplitude'})
                    ax2.set_ylabel('Sub-carrier Index', fontsize=8)
                    ax2.set_xlabel('CSI Index', fontsize=8)
                    ax2.set_title('Heatmap of Experiment ' + k2 + k3, fontsize=12)

                    difference = df1.values - df2.values
                    sns.heatmap(difference.T, ax=ax3, cmap='bwr', cbar=True, xticklabels=False,
                                cbar_kws={'label': 'Amplitude Difference'})
                    ax3.set_yticklabels(ax2.get_yticklabels())
                    ax3.set_ylabel('Sub-carrier Index', fontsize=8)
                    ax3.set_xlabel('CSI Index', fontsize=8)
                    ax3.set_title('Difference Between the Two Experiments', fontsize=12)

                    if not os.path.exists('heatmaps/' + k):
                        os.makedirs('heatmaps/' + k)
                    fig.savefig(
                        'heatmaps/' + k + 'ppl' + str(q) + "cap" + str(i) + "ppl" + str(l) + "cap" + str(j) + '.png')
                    j += 1

                    plt.close('all')  # Close all open plots to free memory
                    del df1, df2, difference
                    gc.collect()
                l += 1
            i += 1
        q += 1
