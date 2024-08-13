import os

from tqdm import tqdm

from whd import whd_to_json, whd_csi


def mindist(dfqs, nsc, q_amp, mindistpath=None):
    """
    Computes the minimum Weighted Hamming Distance between the CSIs of each couple of captures.
    :param dfqs: dictionary containing the quantized data
    :param nsc: number of subcarriers
    :param q_amp: number of bits used for quantization
    :param mindistpath: path where to save the output
    :return: dictionary containing the minimum distance between each couple of experiments
    """
    if len(dfqs) == 0:
        return None

    normfact = nsc * ((2 ** q_amp) - 1)

    m = {}
    for k, v in tqdm(dfqs.items(), colour="red"):  # for each folder
        m[k] = {}
        for k1, v1 in tqdm(dfqs[k].items(), colour="green"):  # for each capture
            m[k][k + k1] = {}
            for kcsi1, csi1 in dfqs[k][k1].iterrows():  # for each CSI in the capture
                for k2, v2 in dfqs.items():  # for each folder
                    if k2 == k:  # if the folder is the same as the capture
                        m[k][k + k1][k2 + k1] = 0  # the distance is 0
                        continue
                    for k3, v3 in dfqs[k2].items():  # for each capture
                        if k2 + k3 in m.keys() \
                                and m[k][k2 + k3][k + k1] != {}:  # if the distance has already been computed
                            m[k][k + k1][k2 + k3] = m[k][k2 + k3][k + k1]  # copy the value
                            continue
                        for kcsi2, csi2 in dfqs[k2][k3].iterrows():  # for each CSI in the capture
                            d = whd_csi(csi1, csi2) / normfact
                            if k2 + k3 not in m[k][k + k1].keys() \
                                    or d < m[k][k + k1][k2 + k3]:
                                m[k][k + k1][k2 + k3] = d

    if mindistpath is not None:
        whd_to_json(m, os.path.join(mindistpath, 'mindist.json'))

    return m
