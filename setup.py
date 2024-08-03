import os

import pandas as pd


def print_menu():
    """
    :return: choice from the user
    """
    print("-------------------------")
    print("0. Exit")
    print("1. Plot magnitude/relative frequency histogram")
    print("2. Plot evolution in time")
    print("3. Plot increment/frequency histogram")
    print("4. Plot auto-correlation function")
    # print("5. Plot inter-SC correlation")
    print("5. Plot multidimensional correlation")
    print("-------------------------")
    return input("Choose an action: ")


def load_data(path, colnames, unneeded):
    """
    Load the data from the csv file and remove the sub-carriers that are not needed
    :param path: path to the csv file
    :param colnames: names of the columns
    :param unneeded: list of sub-carriers to remove
    :return: the data frame
    """
    df = pd.read_csv(path, names=colnames, header=None)
    df = df.dropna(axis=1)
    if len(df.columns) != len(colnames):  # if the number of columns is not the expected one,
        # the data comes from the hdf5 files, so we treat it differently
        for title in df:
            df[title] = pd.DataFrame(
                abs(complex(value.replace(" ", "").replace("i", "j").replace("(", "").replace(")", ""))) for value
                in df[title])
        df.columns = [colnames[i] for i in range(len(colnames)) if colnames[i] not in unneeded]
    else:
        for title in df:
            if title in unneeded:
                del df[title]
            else:
                # format complex numbers into readable values
                df[title] = pd.DataFrame(
                    abs(complex(value.replace(" ", "").replace("i", "j").replace("(", "").replace(")", ""))) for value
                    in df[title])

    # REMOVE EFFECT OF AGC
    for index, row in df.iterrows():
        # each row is a time sample over the sub-carriers (frequencies)
        # compute the mean amplitude over the frequencies and normalize the values by it (i.e. by the energy of the CSI)
        mean = row.mean()
        df.iloc[index] = row / mean
    return df


def set_params(BW, STD, unneeded_dir):
    """
    Set the parameters of the data
    :param BW: channel bandwidth
    :param STD: modulation
    :param unneeded_dir: directory containing the list of sub-carriers to be ignored
    :return: number of sub-carriers, column names, list of unneeded sub-carriers
    """
    nsc = 3.2 * BW
    if STD == 'ax':
        nsc = nsc * 4
    colnames = ["SC" + str(i) for i in range(0, int(nsc))]
    with open(os.path.join(os.getcwd(), unneeded_dir)) as f:
        unneeded = f.read().splitlines()
    return nsc, colnames, unneeded


def removeext(filename):
    return os.path.splitext(filename)[0]
