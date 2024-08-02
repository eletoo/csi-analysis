import csv
import os

import numpy as np
import pandas as pd

import setup
from quant import quantize, mean_csi_comp

MTXSTDDEV = "whd_std.csv"
MTXMEAN = "whd_mean.csv"


def whd(df, ref):
    """
    Computes the Weighted Hamming Distance between each CSI (row) of a dataframe and a reference CSI. CSIs are seen as
    strings of N_sc*nbits bits.
    :param df: dataframe, each row is a CSI
    :param ref: reference CSI
    :return: dictionary indexed by CSI index; each value is the WHD (XOR) between the reference and i-th CSI
    """
    dists = {}
    for index, row in df.iterrows():
        # sum of the absolute differences between the reference and the i-th CSI
        dists[index] = sum(pd.Series(abs(row - ref)))
    return dists


def whd_matrix(dfs, workdir, dfqs, nsc, q_amp=8, stddevpath=None, meanpath=None):
    if len(dfs) == 0:
        return [[0]], [[0]]

    m_stddev = [[0 for _ in range(len(dfs))] for _ in range(len(dfs))]
    m_mean = [[0 for _ in range(len(dfs))] for _ in range(len(dfs))]

    normfact = nsc * ((2 ** q_amp) - 1)

    i = 0
    for k, v in dfs.items():
        mean_csi = quantize(mean_csi_comp(dfs[k]), 0, 2 ** q_amp - 1)
        j = 0
        for k1, v1 in dfs.items():
            d = whd(dfqs[workdir][k1], mean_csi)
            l = []
            for e in d.values():
                l.append(e)
            m_stddev[i][j] = np.std(l) / normfact
            m_mean[i][j] = np.mean(l) / normfact
            j += 1
        i += 1

        if stddevpath is not None:
            save_whd(os.path.join(stddevpath, setup.removeext(k)), MTXSTDDEV, m_stddev)
        if meanpath is not None:
            save_whd(os.path.join(meanpath, setup.removeext(k)), MTXMEAN, m_mean)

    return m_stddev, m_mean


def ext_whd_matrix(dfqs, nsc, q_amp=8, stddevpath=None, meanpath=None):
    if len(dfqs) == 0:
        return [[0]], [[0]]

    m_stddev = [[0 for _ in range(len(dfqs[i]))] for i in range(len(dfqs))]
    m_mean = [[0 for _ in range(len(dfqs[i]))] for i in range(len(dfqs))]
    normfact = nsc * ((2 ** q_amp) - 1)

    for k in range(len(dfqs)):  # for each folder of data
        pass
    if stddevpath is not None:
        save_whd(stddevpath, MTXSTDDEV, m_stddev)
    if meanpath is not None:
        save_whd(meanpath, MTXMEAN, m_mean)

    return m_stddev, m_mean


def save_whd(path, outfile, idata):
    global f, wr
    with open(os.path.join(path, outfile), "w") as f:
        wr = csv.writer(f, delimiter=',', lineterminator='\n')
        wr.writerows(idata)
