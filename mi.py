import os

from matplotlib import pyplot as pl
from scipy.stats import norm


def mi(df, path=""):
    df = df - df.min().min()  # shift data so that it ranges from 0 to max
    df = df / (df.max().max())  # normalize data so that it ranges from 0 to 1

    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    # if not os.path.exists(os.path.join(path, "normalized_incr")):
    #     os.mkdir(os.path.join(path, "normalized_incr"))
    # for each column of df, save the histogram of the values as a .pdf file
    # for title in df:
    #     df[title].diff().hist(bins=100)
    #     pl.xlabel('Normalized Increment')
    #     pl.ylabel('Frequency')
    #     pl.title(title)
    #     pl.rcParams.update({'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large',
    #                         'ytick.labelsize': 'large'})
    #     pl.savefig(os.path.join(os.getcwd(), path, 'normalized_incr', 'figure' + str(title) + '.pdf'))
    #     # print("Plotting histogram " + str(title))
    #     pl.close()

    # create an array with all increments
    increments = []
    for title in df:
        increments.extend(df[title].diff().drop(labels=0, axis=0))

    # fit normal distribution to the data to compute mean and sigma of the distribution of the increments
    # on each column of df
    with open(os.path.join(path, "mu_sigma.txt"), "w") as f:
        # for title in df:
        # mu, sigma = norm.fit(df[title].diff().drop(labels=0, axis=0))  # fit a normal distribution to the increments
        mu, sigma = norm.fit(increments)
        f.write("MU: " + str(mu) + "\tSIGMA: " + str(sigma) + "\n")

    return (df * 255).astype(int)  # quantize over 256 levels (0 to 255)
