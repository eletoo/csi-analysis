import math
import os
import numpy as np
from scipy.stats import norm
from tqdm import tqdm


def mi(df, path=""):
    df = df - df.min().min()  # shift data so that it ranges from 0 to max
    df = df / (df.max().max())  # normalize data so that it ranges from 0 to 1

    if path != "" and not os.path.exists(path):
        os.mkdir(path)

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

    # fit normal distribution to the data to compute mean and sigma of the distribution of the increments
    with open(os.path.join(path, "mu_sigma.txt"), "w") as f:
        mu, sigma = norm.fit(increments)
        f.write("MU: " + str(mu) + "\tSIGMA: " + str(sigma) + "\n")
    f.close()

    # for each delta_t compute increments between CSI at time t and CSI at time t + delta_t (for each t)
    # fit normal distribution to the data to compute mean and sigma of the distribution of the increments
    # with open(os.path.join(path, "mu_sigma_delta_t.txt"), "w") as f:
    #     for delta in tqdm(range(1, rows), total=rows - 1):
    #         diffs = []
    #         for row in range(1, rows):
    #             if row + delta >= math.floor(rows/2):
    #                 break
    #             diffs.extend(df.iloc[row, :] - df.iloc[row + delta, :])
    #         mu, sigma = norm.fit(diffs)
    #         f.write("DELTA_T: " + str(delta) + "\tMU: " + str(mu) + "\tSIGMA: " + str(sigma) + "\n")
    # f.close()

    return (df * 255).astype(int)  # quantize over 256 levels (0 to 255)
