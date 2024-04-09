import os

from matplotlib import pyplot as pl
from statsmodels.tsa.stattools import acovf


def diag_to_vec(df, s_i, s_j, direction=(1, 1)):
    """
    :param df: dataframe containing the amplitude of the CSI packets
    :param s_i: starting index of the row (CSI index)
    :param s_j: starting index of the column (sub-carrier index)
    :param direction: direction of the diagonal (1, 1) for the main diagonal, (1, -1) for the secondary diagonal, etc.
    :return: next element of the diagonal
    """
    h, w = df.shape
    i, j = s_i, s_j
    while h > i >= 0 and w > j >= 0:
        yield df.iloc[i, j]
        i += direction[0]
        j += direction[1]


def save_multidimensional_corr(df, path: str = ""):
    """
    :param df: dataframe containing the amplitude of the CSI packets
    :param path: path where to save the output of the code, can be an empty string
    :return: None
    """
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "multidim_corr")):
        os.mkdir(os.path.join(path, "multidim_corr"))
    path = path + "/multidim_corr"

    for i in range(df.shape[0]):  # for each CSI
        for j in range(df.shape[1]):  # for each sub-carrier
            diag1 = list(diag_to_vec(df, i, j, direction=(1, 1)))  # main diagonal
            diag2 = list(diag_to_vec(df, i, j, direction=(1, -1)))  # secondary diagonal
            c1 = acovf(diag1, nlag=len(diag1) - 1)
            c1 = c1 / c1[0]  # autocorrelation of the main diagonal
            c2 = acovf(diag2, nlag=len(diag2) - 1)
            c2 = c2 / c2[0]  # autocorrelation of the secondary diagonal
            pl.plot(c1, label="Main Diagonal")
            pl.plot(c2, label="Secondary Diagonal")
            pl.xlabel('Tau')
            pl.ylabel('Correlation')
            pl.title("Correlation Along Diagonals starting from (CSI: " + str(i) + ", SC: " + str(j) + ")")
            pl.rcParams.update(
                {'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large',
                 'ytick.labelsize': 'large'})
            pl.grid(visible=True)
            pl.legend()
            if not os.path.exists(os.path.join(path, df.columns[j])):
                os.mkdir(os.path.join(path, df.columns[j]))
            pl.savefig(os.path.join(os.getcwd(), path, df.columns[j], 'CSI' + str(i) + "_" + df.columns[j] + '.pdf'))
            pl.close()
