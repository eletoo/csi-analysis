import math
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

MEAN_CSI_CSV = "mean_CSI.csv"

MU_SIGMA_TXT = "mu_sigma.txt"
QB = 4  # qb = 3, 4, 5 to have support over 7, 15, 31 levels


def compute_qamp(df, path="", qb=QB):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    df = normalize(df)

    art_incrq, incrq, mu, sigma = quantize_incr(df, path, qb)

    # with open(os.path.join(path, MU_SIGMA_TXT), "w") as f:
    #     f.write("MU: " + str(mu) + "\tSIGMA: " + str(sigma) + "\n")

    q_inc = qb
    dstar = 3 * sigma
    return math.ceil(math.log2(1 / dstar * (2 ** q_inc + 1))), q_inc, art_incrq, incrq


def quant(df, q_amp, path=""):
    df = normalize(df)

    # plt.plot(df['capture0.csv'].iloc[1000], label='Normalized')
    # plt.grid()
    # plt.xlabel('Subcarrier')
    # plt.ylabel('Amplitude')
    # plt.savefig('original.pdf')
    # plt.close()
    df_quant = quantize(df, 0, 2 ** q_amp - 1)  # quantize data over 2^qb levels
    save_mean_csi(df, os.path.join(path, MEAN_CSI_CSV))
    mean_csi = quantize(mean_csi_comp(df), 0, 2 ** q_amp - 1)

    return df, df_quant, mean_csi


def quantize_incr(df, path, qb):
    increments = df.diff().dropna()
    mu, sigma = norm.fit(increments, loc=0)  # sigma = stddev
    art_incr_quant, incr_quant = quantize_norm(increments, sigma, qb, mu=0,
                                               path=path)  # quantize increments over 2^qb levels
    return art_incr_quant, incr_quant, mu, sigma


def quantize_norm(increments, sigma, qb, mu=0, path=''):
    dstar = 3 * sigma
    ss = norm.rvs(loc=mu, scale=sigma, size=increments.size)  # generate artificial sample
    sample = np.vectorize(lambda x: -dstar if x < -dstar else dstar if x > dstar else x)(ss)
    sample2 = np.vectorize(lambda x: -dstar if x < -dstar else dstar if x > dstar else x)(increments.values.flatten())

    snew = (sample - min(sample)) / (max(sample) - min(sample)) * (2 ** qb - 2) - (2 ** (qb - 1) - 1)
    snew2 = (sample2 - min(sample2)) / (max(sample2) - min(sample2)) * (2 ** qb - 2) - (2 ** (qb - 1) - 1)

    qsamples = [int(round(i)) for i in snew]
    qsamples2 = [int(round(i)) for i in snew2]

    # make sure that the distribution integrates to 1
    occ = [qsamples.count(i) / len(qsamples) for i in range(-2 ** (qb - 1) + 1, 2 ** (qb - 1) + 1)]
    print("\n" + str(sum(occ)) + "\n")

    hist_dist_compared(path, qb, qsamples, qsamples2)

    return qsamples, qsamples2


def hist_dist_compared(path, qb, qsamples, qsamples2):
    y, x = np.histogram(qsamples, bins=range(- 2 ** (qb - 1) + 1, 2 ** (qb - 1) + 1))
    y = y / sum(y)  # normalize histogram
    y2, x = np.histogram(qsamples2, bins=range(- 2 ** (qb - 1) + 1, 2 ** (qb - 1) + 1))
    y2 = y2 / sum(y2)  # normalize histogram
    plt.bar(x[:-1], y, align='center', label='Sample')
    plt.bar(x[:-1], y2, align='center', label=str(qb) + ' bits', width=0.5)
    plt.gca().set_xticks(x[:-1])
    plt.title("Histogram of quantized increments")
    plt.xlabel("Quantized increment value")
    plt.ylabel("Probability")
    plt.yscale('log')
    plt.legend()
    plt.grid()
    # plt.show()
    plt.xticks(fontsize=6)
    plt.savefig(os.path.join(path, "hist_quant_incr_VS_sample_" + str(qb) + ".pdf"))
    plt.close()


def mean_csi_comp(df):
    """Compute mean CSI values.
    :param df: dataframe to compute the mean CSI on
    """
    return df.mean(axis=0)


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
