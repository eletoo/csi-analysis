import os

import numpy as np
import pandas as pd
from scipy.stats import norm
from tqdm import tqdm

MEAN_CSI_CSV = "mean_CSI.csv"

MU_SIGMA_TXT = "mu_sigma.txt"


def mi(df, path=""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    df = normalize(df)

    rows, cols = df.shape
    increments = np.nan * np.ones((int(rows * (rows - 1) / 2), cols))

    # compute increments between CSI at time t and CSI at time t + delta_t (for each t and for each delta_t)
    cur_row = 0
    for i in tqdm(range(rows), total=rows):
        row = df.iloc[i, :]
        for j in range(i + 1, rows):
            diff = (row - df.iloc[j, :]).values
            increments[cur_row, :] = diff
            cur_row += 1

    # increments = df.diff().dropna()  # DEBUG - compute increments between CSI at time t and CSI at time t + 1

    df_quant = quantize(df, 0, 255)

    df_incr = pd.DataFrame()
    df_incr = increments
    incr = (df_incr * 255).round()

    # fit normal distribution to increments to compute mean and sigma of the distribution
    with open(os.path.join(path, MU_SIGMA_TXT), "w") as f:
        mu, sigma = norm.fit(increments)
        f.write("MU: " + str(mu) + "\tSIGMA: " + str(sigma) + "\n")

        mu, sigma = norm.fit(incr)
        f.write("MU_quant: " + str(mu) + "\tSIGMA_quant: " + str(sigma) + "\n")

    # for each delta_t compute increments between CSI at time t and CSI at time t + delta_t (for each t)
    # fit normal distribution to the data to compute mean and sigma of the distribution of the increments
    # with open(os.path.join(path, "mu_sigma_delta_t.txt"), "w") as f:
    # for delta in tqdm(range(1, rows), total=math.floor(rows / 2)):
    #     diffs = []
    #     for row in range(1, rows):
    #         if row + delta >= math.floor(rows / 2):
    #             break
    #         diffs.extend(df.iloc[row, :] - df.iloc[row + delta, :])
    #     mu, sigma = norm.fit(diffs)
    #     f.write("DELTA_T: " + str(delta) + "\tMU: " + str(mu) + "\tSIGMA: " + str(sigma) + "\n")
    # f.close()

    save_mean_csi(df, os.path.join(path, MEAN_CSI_CSV))
    # df_quant = quantize(df, 0, 255).diff().dropna()
    return quantize(df, a=0, b=255)  # quantize over 256 levels (0 to 255)


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
