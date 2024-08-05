import json
import os

import numpy as np
import pandas as pd
from tqdm import tqdm

from quant import quantize, mean_csi_comp

MTXSTDDEV = "whd_std.json"
MTXMEAN = "whd_mean.json"


def whd(df, ref):
    """
    Computes the Weighted Hamming Distance between each CSI (row) of a dataframe and a reference CSI. CSIs are seen as
    strings of N_sc*nbits bits, the weight is given by the conversion from binary to decimal.
    :param df: dataframe, each row is a CSI
    :param ref: reference CSI
    :return: dictionary indexed by CSI index; each value is the WHD between the reference and i-th CSI
    """
    dists = {}
    for index, row in df.iterrows():
        # sum of the absolute differences between the reference and the i-th CSI
        dists[index] = sum(pd.Series(abs(row - ref)))
    return dists


def whd_matrix(dfs, workdir, dfqs, nsc, q_amp=9, stddevpath=None, meanpath=None):
    """
    Computes the average Weighted Hamming Distance between the mean CSI of each capture and the CSIs of all the other
    captures belonging to the same experiment.
    :param dfs: dictionary of dataframes, each containing the CSI of a capture
    :param workdir: working directory
    :param dfqs: dictionary of quantized dataframes
    :param nsc: number of subcarriers
    :param q_amp: number of bits used for quantization
    :param stddevpath: path where to save the standard deviation matrix
    :param meanpath: path where to save the mean matrix
    :return: standard deviation and mean matrices
    """
    # if used, pass the dfs[experiment] dictionary, not dfs as a whole.
    # in main it was used as (in the "for k1, df in dframes.items()" loop):
    # whd_std, whd_mean = whd_matrix(dfs=dfs[k],  # passing dfs relative to a single experiment
    #                                workdir=k,  # name of the folder containing the data
    #                                dfqs=dfqs,  # dictionary containing the quantized data
    #                                nsc=num_sc,  # number of subcarriers
    #                                q_amp=q_amp,  # quantization level
    #                                stddevpath=dst_folder, meanpath=dst_folder)  # path where to save the output

    if len(dfs) == 0:
        return [[0]], [[0]]
    normfact = nsc * ((2 ** q_amp) - 1)

    m_stddev = {}
    m_mean = {}
    for k, v in tqdm(dfs.items(), colour="red"):  # for each capture k in the experiment
        mean_csi = quantize(mean_csi_comp(dfs[k]), 0, 2 ** q_amp - 1)  # quantize the mean CSI of k
        m_stddev[k] = {}
        m_mean[k] = {}
        for k1, v1 in tqdm(dfs.items(), colour="green"):  # for each capture k1 in the experiment
            d = whd(dfqs[workdir][k1], mean_csi)  # compute the WHD between the mean CSI of k and the CSIs of k1
            l = []
            for e in d.values():
                l.append(e)
            m_stddev[k][k1] = np.std(l) / normfact
            m_mean[k][k1] = np.mean(l) / normfact

        if stddevpath is not None:
            whd_to_json(m_stddev, os.path.join(stddevpath, MTXSTDDEV))
        if meanpath is not None:
            whd_to_json(m_mean, os.path.join(meanpath, MTXMEAN))
    return m_stddev, m_mean


def whd_to_json(data, path):
    """
    Saves a dictionary to a json file.
    :param data: dictionary
    :param path: path where to save the file
    :return: None
    """
    with open(path, 'w') as fp:
        json.dump(data, fp)


def full_whd_matrix(dfs, dfqs, nsc, q_amp=9, stddevpath=None, meanpath=None):
    """
    Computes the average Weighted Hamming Distance between the mean CSI of each capture and the CSIs of all the other
    captures.
    :param dfs: dictionary of dataframes, each containing the CSI of a capture
    :param dfqs: dictionary of quantized dataframes
    :param nsc: number of subcarriers
    :param q_amp: number of bits used for quantization
    :param stddevpath: path where to save the standard deviation matrix
    :param meanpath: path where to save the mean matrix
    :return: standard deviation and mean matrices
    """
    if len(dfs) == 0:
        return [[0]], [[0]]

    normfact = nsc * ((2 ** q_amp) - 1)

    m_stddev = {}
    m_mean = {}
    for k, v in tqdm(dfs.items(), colour="red"):  # for each folder
        m_stddev[k] = {}
        m_mean[k] = {}
        for k1, v1 in tqdm(dfs[k].items(), colour="green"):  # for each capture
            mean_csi = quantize(mean_csi_comp(dfs[k][k1]), 0, 2 ** q_amp - 1)  # quantize the mean CSI of capture k1
            m_stddev[k][k + k1] = {}
            m_mean[k][k + k1] = {}
            for k2, v2 in dfs.items():  # for each folder
                for k3, v3 in dfs[k2].items():  # for each capture
                    d = whd(dfqs[k2][k3], mean_csi)  # compute the WHD between the mean CSI of k1 and the CSIs of k3
                    l = []
                    for e in d.values():
                        l.append(e)
                    m_stddev[k][k + k1][k2 + k3] = np.std(l) / normfact  # folder, capture1, capture2
                    m_mean[k][k + k1][k2 + k3] = np.mean(l) / normfact

    if stddevpath is not None:
        whd_to_json(m_stddev, os.path.join(stddevpath, MTXSTDDEV))
    if meanpath is not None:
        whd_to_json(m_mean, os.path.join(meanpath, MTXMEAN))
    return m_stddev, m_mean
