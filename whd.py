import os

import numpy as np
from tqdm import tqdm

from quant import quantize, save_mean_csi
from setup import load_data


def whd_bin(df, csi_mean, nbits):
    """
    Computes the Weighted Hamming Distance between each CSI (row) of a dataframe and a reference CSI. CSIs are seen
    as strings of N_sc*nbits bits.
    :param df: dataframe, each row is a CSI, each column a Sub-carrier
    :param csi_mean: reference CSI (mean CSI)
    :param nbits: number of bits over which CSIs are quantized
    :return: dictionary indexed by CSI index; each value is a dictionary indexed by Sub-carrier having as value the WHD
    (XOR) between the amplitudes of the reference and i-th CSI on the j-th sub-carrier
    """
    dfbin = df.applymap(lambda x: [*bin(int(x))[2:].zfill(nbits)])
    # N.B. I can fill with zeros because all quantized values are positive
    csi_mean_bin = csi_mean.apply(lambda x: [*bin(int(x))[2:].zfill(nbits)])
    dists = {i: {} for i in range(len(dfbin))}
    for index, row in tqdm(dfbin.iterrows()):  # for each CSI
        for index2, item in row.iteritems():  # for each SC
            dists[index][index2] = 0
            for i in range(nbits - 1, -1, -1):
                if item[i] == csi_mean_bin[index2][i]:
                    dists[index][index2] += 0
                else:
                    dists[index][index2] += 2 ** (nbits - 1 - i)
    return dists


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
    # the -1 in the following lines is due to the fact that the last element of the list is the config json file
    m_stddev = [[0 for _ in range(len(os.listdir(workdir)) - 1)] for _ in range(len(os.listdir(workdir)) - 1)]
    m_mean = [[0 for _ in range(len(os.listdir(workdir)) - 1)] for _ in range(len(os.listdir(workdir)) - 1)]

    dfs = []
    for file in os.listdir(workdir):
        if file.endswith('.csv'):
            dfs.append(load_data(workdir + file, colnames, unneeded))

    for i in range(len(dfs)):
        # df_quant = quantize(dfs[i], 0, 2 ** q_amp - 1)
        mean_csi = quantize(save_mean_csi(dfs[i], os.path.join(dst_folder, "mean" + str(i) + ".csv")), 0,
                            2 ** q_amp - 1)
        for j in range(len(dfs)):
            df_quant2 = quantize(dfs[j], 0, 2 ** q_amp - 1)
            # mean_csi2 = quantize(save_mean_csi(dfs[j], os.path.join(dst_folder, "mean" + i + ".csv")), 0,
            #                      2 ** q_amp - 1)
            d = whd_int(df_quant2, mean_csi)
            l = []
            for e in d.values():
                l.append(e)
            m_stddev[i][j] = np.std(l)
            m_mean[i][j] = np.mean(l)
    return m_stddev, m_mean


def cross_whd_matrix(workdir, compdir, unneeded=[], colnames=[], q_amp=8):
    dfi = []
    for file in os.listdir(workdir):
        if file.endswith('.csv'):
            dfi.append(load_data(workdir + file, colnames, unneeded))
    dfj = []
    for file in os.listdir(compdir):
        if file.endswith('.csv'):
            dfj.append(load_data(compdir + file, colnames, unneeded))

    m_stddev = [[0 for _ in range(len(dfi))] for _ in range(len(dfj))]
    m_mean = [[0 for _ in range(len(dfi))] for _ in range(len(dfj))]

    for i in range(len(dfi)):
        mean_csi = quantize(save_mean_csi(dfi[i], os.path.join(workdir, "mean" + str(i) + ".csv")), 0, 2 ** q_amp - 1)
        for j in range(len(dfj)):
            df_quant2 = quantize(dfj[j], 0, 2 ** q_amp - 1)
            d = whd_int(df_quant2, mean_csi)
            l = []
            for e in d.values():
                l.append(e)
            m_stddev[i][j] = np.std(l)
            m_mean[i][j] = np.mean(l)

    return m_stddev, m_mean
