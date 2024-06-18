import math
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

MEAN_CSI_CSV = "mean_CSI.csv"

MU_SIGMA_TXT = "mu_sigma.txt"
QB = 4  # qb = 3, 4, 5 to have support over 7, 15, 31 levels


def mi(df, qb=QB, path=""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    df = normalize(df)

    # rows, cols = df.shape
    # increments = np.nan * np.ones((int(rows * (rows - 1) / 2), cols))

    # # compute increments between CSI at time t and CSI at time t + delta_t (for each t and for each delta_t)
    # cur_row = 0
    # for i in tqdm(range(rows), total=rows):
    #     row = df.iloc[i, :]
    #     for j in range(i + 1, rows):
    #         diff = (row - df.iloc[j, :]).values
    #         increments[cur_row, :] = diff
    #         cur_row += 1

    increments = df.diff().dropna()  # DEBUG - compute increments between CSI at time t and CSI at time t + 1
    mu, sigma = norm.fit(increments)

    q_inc = qb
    dstar = 3 * sigma
    q_amp = math.ceil(math.log2(1 / dstar * (2 ** q_inc + 1)))  # quantize amplitudes over 2^q_amp levels

    df_quant = quantize(df, 0, 2 ** q_amp - 1)  # quantize data over 2^qb levels
    incr_quant = quantize_norm(increments, sigma, qb, mu=0, path=path)  # quantize increments over 2^qb levels

    # fit normal distribution to increments to compute mean and sigma of the distribution
    with open(os.path.join(path, MU_SIGMA_TXT), "w") as f:
        f.write("MU: " + str(mu) + "\tSIGMA: " + str(sigma) + "\n")

    save_mean_csi(df, os.path.join(path, MEAN_CSI_CSV))
    return df_quant, incr_quant, q_inc, q_amp


def quantize_norm(increments, sigma, qb, mu=0, path=''):
    dstar = 3 * sigma

    sample = np.vectorize(lambda x: -dstar if x < -dstar else dstar if x > dstar else x)(
        np.random.normal(loc=mu, scale=sigma, size=increments.size))
    # sample2 = np.vectorize(lambda x: -dstar if x < -dstar else dstar if x > dstar else x)(increments.values.flatten())

    snew = (sample - min(sample)) / (max(sample) - min(sample)) * (2 ** qb - 2) - (2 ** (qb - 1) - 1)
    # snew2 = (sample2 - min(sample2)) / (max(sample2) - min(sample2)) * (2 ** qb - 2) - (2 ** (qb - 1) - 1)

    qsamples = [int(round(i)) for i in snew]
    # qsamples2 = [int(round(i)) for i in snew2]

    # make sure that the distribution integrates to 1
    occ = [qsamples.count(i) / len(qsamples) for i in range(-2 ** (qb - 1) + 1, 2 ** (qb - 1) + 1)]
    print(sum(occ))

    y, x = np.histogram(qsamples, bins=range(- 2 ** (qb - 1) + 1, 2 ** (qb - 1) + 1))
    y = y / max(y)  # normalize histogram
    # y2, x = np.histogram(qsamples2, bins=range(- 2 ** (qb - 1) + 1, 2 ** (qb - 1) + 1))
    # y2 = y2 / max(y2)  # normalize histogram
    plt.bar(x[:-1], y, align='center', label='Sample')
    # plt.bar(x[:-1], y2, align='center', label=str(qb) + ' bits', width=0.5)
    plt.gca().set_xticks(x[:-1])
    plt.yscale('log')
    plt.legend()
    plt.grid()
    # plt.show()
    plt.savefig(os.path.join(path, "quant_sample_" + str(qb) + ".pdf"))

    return qsamples


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
    for index, row in df.iterrows():  # each row is normalized wrt its max value
        df.iloc[index] = df.iloc[index] - df.iloc[index].min()
        df.iloc[index] = df.iloc[index] / df.iloc[index].max()
    # df = df - df.min().min()  # shift data so that it ranges from 0 to max
    # df = df / (df.max().max())  # normalize data so that it ranges from 0 to 1
    return df


def quantize(df, a=0, b=255):
    """Quantize data into an integer number of levels ranging from a to b.
    :param df: dataframe to quantize
    :param a: lower bound of the quantization interval
    :param b: upper bound of the quantization interval
    :return: quantized dataframe
    """
    return round(df * (b - a) + a)
