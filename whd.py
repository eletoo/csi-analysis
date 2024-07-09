from tqdm import tqdm


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
