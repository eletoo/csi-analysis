import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import xticks

import mi


def plotcsi(df, n=1, title='CSI Amplitude', xlabel='Subcarrier index', ylabel='Amplitude'):
    plt.figure()
    for i in range(n):
        idx = np.random.randint(0, len(df))
        plt.plot(df.iloc[idx], label='A_c ' + str(idx))
    plt.title(title)
    plt.legend(fontsize=8)
    plt.xlabel(xlabel)
    xticks(np.arange(0, len(df.columns), 20), fontsize=6)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()


def plotcsi_quant(df, df_quant, n=1, q_amp=8, title='CSI Amplitude', xlabel='Subcarrier index', ylabel='Amplitude',
                  path=''):
    # undo quantization
    a = 0
    b = 2 ** q_amp - 1
    dequant = (df_quant - a) * (b - a)
    dequant = mi.normalize(dequant)

    # plt.figure()
    fig, ax = plt.subplots(3, 1, sharex=True)
    for i in range(n):
        idx = np.random.randint(0, len(df))
        ax[0].plot(df.iloc[idx], label='A_c ' + str(idx))
        ax[1].plot(df_quant.iloc[idx], label='A_c^q ' + str(idx))
        ax[2].plot(df.iloc[idx] - dequant.iloc[idx], label='A_c - A_c^q ' + str(idx))
    ax[0].legend(loc='upper right', fontsize=5)
    fig.suptitle(title)
    plt.xlabel(xlabel)
    xticks(np.arange(0, len(df.columns), 25), fontsize=6)
    ax[0].set_ylabel(ylabel)
    ax[1].set_ylabel('Quantized ' + ylabel)
    ax[2].set_ylabel('Difference')
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    # plt.show()
    plt.savefig(os.path.join(path, 'csi_VS_csiquant.pdf'))
    plt.close()
