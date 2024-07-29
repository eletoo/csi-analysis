import os

import numpy as np

from quant import quantize, mean_csi_comp
from setup import load_data


def whd_int(df, ref):
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
        dists[index] = sum(abs(row - ref).sum())
        # .sum() computes sum over columns (although there's only one element per column),
        # then sum(...) sums all elements of the resulting series (i.e. the sum of the absolute differences)
    return dists


def whd_matrix(workdir, unneeded=[], colnames=[], dst_folder='', q_amp=8):
    m_stddev = [[0 for _ in range(len(os.listdir(workdir)))] for _ in range(len(os.listdir(workdir)))]
    m_mean = [[0 for _ in range(len(os.listdir(workdir)))] for _ in range(len(os.listdir(workdir)))]

    dfs = []
    for file in os.listdir(workdir):
        if not file.startswith("mean") and file.endswith('.csv'):
            dfs.append(load_data(workdir + file, colnames, unneeded))
    normfact = len(colnames) * ((2 ** q_amp) - 1)

    for i in range(len(dfs)):
        # df_quant = quantize(dfs[i], 0, 2 ** q_amp - 1)
        mean_csi = quantize(mean_csi_comp(dfs[i]), 0,
                            2 ** q_amp - 1)
        for j in range(len(dfs)):
            df_quant2 = quantize(dfs[j], 0, 2 ** q_amp - 1)
            # mean_csi2 = quantize(save_mean_csi(dfs[j], os.path.join(dst_folder, "mean" + i + ".csv")), 0,
            #                      2 ** q_amp - 1)
            d = whd_int(df_quant2, mean_csi)
            l = []
            for e in d.values():
                l.append(e)
            m_stddev[i][j] = np.std(l) / normfact
            m_mean[i][j] = np.mean(l) / normfact
    return m_stddev, m_mean


def cross_whd_matrix(reference, experiment, unneeded=[], colnames=[], q_amp=8):
    dfi = []
    for file in os.listdir(reference):
        if not file.startswith("mean") and file.endswith('.csv'):
            dfi.append(load_data(reference + file, colnames, unneeded))
    dfj = []
    for file in os.listdir(experiment):
        if not file.startswith("mean") and file.endswith('.csv'):
            dfj.append(load_data(experiment + file, colnames, unneeded))

    m_stddev = [[0 for _ in range(len(dfi))] for _ in range(len(dfj))]
    m_mean = [[0 for _ in range(len(dfi))] for _ in range(len(dfj))]
    normfact = len(colnames) * ((2 ** q_amp) - 1)
    for i in range(len(dfi)):
        mean_csi = quantize(mean_csi_comp(dfi[i]), 0, 2 ** q_amp - 1)
        for j in range(len(dfj)):
            df_quant2 = quantize(dfj[j], 0, 2 ** q_amp - 1)
            d = whd_int(df_quant2, mean_csi)
            l = []
            for e in d.values():
                l.append(e)
            m_stddev[i][j] = np.std(l) / normfact
            m_mean[i][j] = np.mean(l) / normfact

    return m_stddev, m_mean
