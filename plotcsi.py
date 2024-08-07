import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import xticks

import quantize


def plotcsi(df, n=1, title='CSI Amplitude', xlabel='Subcarrier index', ylabel='Amplitude'):
    plt.figure()
    for i in range(n):
        idx = np.random.randint(0, len(df))
        plt.plot(df.iloc[idx], label='A_c ' + str(idx))
    plt.title(title)
    plt.legend(fontsize=8)
    plt.xlabel(xlabel)
    xticks(np.arange(0, len(df.columns), 50), fontsize=6)
    plt.ylabel(ylabel)
    plt.grid()
    # plt.show()
    plt.savefig('csi.pdf')
    plt.close()


def plotcsi_quant(dfnorm, df_quant, n=1, q_amp=8, title='CSI Amplitude', xlabel=r'Subcarrier index ($n$)',
                  ylabel=r'$A_c$',
                  path=''):
    # undo quantization
    a = 0
    b = 2 ** q_amp - 1
    dequant = (df_quant - a) * (b - a)
    dequant = quantize.normalize(dequant)

    # plt.figure()
    fig, ax = plt.subplots(3, 1, sharex=True)
    for i in range(n):
        idx = np.random.randint(0, len(dfnorm))
        ax[0].plot(dfnorm.iloc[idx], label=r'$A({' + str(idx) + '},n)$')
        ax[1].plot(df_quant.iloc[idx], label=r'$A({' + str(idx) + '},n)^q$')
        ax[2].plot(dfnorm.iloc[idx] - dequant.iloc[idx], label=r'$A({' + str(idx) + '},n)-A({' + str(idx) + '},n)^q$')
    ax[0].legend(loc='upper right', fontsize=5)

    fig.suptitle(title)

    plt.xlabel(xlabel)
    xticks(np.arange(0, len(dfnorm.columns), 25), fontsize=6)

    ax[0].set_ylim(0, 1)
    ax[0].set_ylabel(ylabel)
    ax[1].set_ylim(0, 2 ** q_amp)
    ax[1].set_ylabel(r'$A_c^q$')
    ax[2].set_ylim(-0.1, 0.1)
    ax[2].set_ylabel(r'$A_c - A_c^q$')

    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    # plt.show()
    plt.savefig(os.path.join(path, 'csi_VS_csiquant.pdf'))
    plt.close()
