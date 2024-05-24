import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

MEAN_CSI_CSV = "mean_CSI.csv"

MU_SIGMA_TXT = "mu_sigma.txt"
QB = 3  # 3, 4, 5


def mi(df, qb=QB, path=""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    df = normalize(df)

    rows, cols = df.shape
    # increments = np.nan * np.ones((int(rows * (rows - 1) / 2), cols))
    #
    # # compute increments between CSI at time t and CSI at time t + delta_t (for each t and for each delta_t)
    # cur_row = 0
    # for i in tqdm(range(rows), total=rows):
    #     row = df.iloc[i, :]
    #     for j in range(i + 1, rows):
    #         diff = (row - df.iloc[j, :]).values
    #         increments[cur_row, :] = diff
    #         cur_row += 1

    increments = df.diff().dropna()  # DEBUG - compute increments between CSI at time t and CSI at time t + 1

    df_quant = quantize(df, -2 ** (qb - 1), 2 ** (qb - 1))  # quantize data over 2^qb levels
    bin_incr = quantize_norm(increments, qb, path)  # quantize increments over 2^qb levels

    # fit normal distribution to increments to compute mean and sigma of the distribution
    with open(os.path.join(path, MU_SIGMA_TXT), "w") as f:
        mu, sigma = norm.fit(increments)
        f.write("MU: " + str(mu) + "\tSIGMA: " + str(sigma) + "\n")

    save_mean_csi(df, os.path.join(path, MEAN_CSI_CSV))
    return df_quant, bin_incr


def quantize_norm(increments, qb, path=''):  # qb = 3, 4, 5 to have support over 8, 16, 32 levels
    mu, sigma = norm.fit(increments)
    dstar = 3 * sigma

    # sample = np.vectorize(lambda x: -dstar if x < -dstar else dstar if x > dstar else x)(norm.rvs(loc=mu, scale=sigma,
    #                   size=increments.size))  # generate sample from normal distribution with correct mu and sigma
    sample = np.vectorize(lambda x: -dstar if x < -dstar else dstar if x > dstar else x)(increments.values.flatten())

    snew = (sample - min(sample)) / (max(sample) - min(sample)) * (2 ** qb - 2) - (2 ** (qb - 1) - 1)
    zeros = []
    for i in range(len(snew)):
        if - 1e-5 < snew[i] < 0:
            zeros.append(i)
    qsamples = [int(round(i)) for i in snew]

    # make sure that the distribution integrates to 1
    occ = [qsamples.count(i) / len(qsamples) for i in range(-2 ** (qb - 1) + 1, 2 ** (qb - 1) + 1)]
    print(sum(occ))

    y, x = np.histogram(qsamples, bins=range(- 2 ** (qb - 1) + 1, 2 ** (qb - 1) + 1))
    # y = y / max(y)
    plt.bar(x[:-1], y, align='center')
    plt.gca().set_xticks(x[:-1])
    # plt.show()
    plt.grid()
    plt.savefig(os.path.join(path, "quant_increments_" + str(qb) + ".pdf"))

    binincr = []
    for i in range(len(qsamples)):
        # turn into 1+7 bits representation
        if qsamples[i] < 0 or i in zeros:
            binnum = ''.join(bin(qsamples[i])[3:])
            while len(binnum) < 7:
                binnum = '0' + binnum
            binnum = '1' + binnum
        else:
            binnum = ''.join(bin(qsamples[i])[2:])
            while len(binnum) < 8:
                binnum = '0' + binnum
        binincr.append(binnum)

    return binincr


def save_mean_csi(df, path):
    """Save mean CSI values to a CSV file.
    :param df: dataframe to compute the mean CSI on
    :param path: path to save the CSV file
    """
    if not path.endswith(".csv"):  # fix file extension
        path = path[:path.rfind(".")]
        path += ".csv"
    with open(path, "w") as mcsi:
        for col in df.columns:
            mcsi.write(str(df[col].mean()) + ",")
        mcsi.truncate(mcsi.tell() - 1)  # remove last comma
    mcsi.close()


def normalize(df):
    """Normalize data so that it ranges from 0 to 1.
    :param df: dataframe to normalize
    :return: normalized dataframe
    """
    df = df - df.min().min()  # shift data so that it ranges from 0 to max
    df = df / (df.max().max())  # normalize data so that it ranges from 0 to 1
    return df


def quantize(df, a=0, b=255):
    """Quantize data into an integer number of levels ranging from a to b.
    :param df: dataframe to quantize
    :param a: lower bound of the quantization interval
    :param b: upper bound of the quantization interval
    :return: quantized dataframe
    """
    return round(df * (b - a) + a)
