import math
import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import xticks


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
    # UNCOMMENT COMMENTED LINES TO PROCESS PHASE AS WELL
    # colnames=["SC" + str(i) for i in range(-256,256)]
    # unneeded=['SC-256', 'SC-255', 'SC-254', 'SC-253', 'SC-252', 'SC-251', 'SC-250', 'SC-249', 'SC-248', 'SC-247', 'SC-246', 'SC-245', 'SC-244', 'SC245', 'SC246', 'SC247', 'SC248', 'SC249', 'SC250', 'SC251', 'SC252', 'SC253', 'SC254', 'SC255', 'SC256']
    df = pd.read_csv(path, names=colnames, header=None)
    df = df.dropna(axis=1)
    # dfphase = df.copy()
    if len(df.columns) != len(colnames):  # if the number of columns is not the expected one,
        # the data comes from the hdf5 files, so we treat it differently
        for title in df:
            df[title] = pd.DataFrame(
                abs(complex(value.replace(" ", "").replace("i", "j").replace("(", "").replace(")", ""))) for value
                in df[title])
            # df[title] = pd.DataFrame(abs(val) for val in df[title])
            # dfphase[title] = pd.DataFrame(
            #     np.angle(complex(value.replace(" ", "").replace("i", "j").replace("(", "").replace(")", "")) for value
            #              in dfphase[title]))
        df.columns = [colnames[i] for i in range(len(colnames)) if colnames[i] not in unneeded]
    else:
        for title in df:
            if title in unneeded:
                del df[title]
                # del dfphase[title]
            else:
                # format complex numbers into readable values
                df[title] = pd.DataFrame(
                    abs(complex(value.replace(" ", "").replace("i", "j").replace("(", "").replace(")", ""))) for value
                    in df[title])

                # dfphase[title] = pd.DataFrame(
                #     np.angle(
                #         complex(value.replace(" ", "").replace("i", "j").replace("(", "").replace(")", ""))) for value
                #     in dfphase[title])

    # REMOVE EFFECT OF AGC
    indexes = []
    for index, row in df.iterrows():
        # each row is a time sample over the sub-carriers (frequencies)
        # compute the mean amplitude over the frequencies and normalize the values by it (i.e. by the energy of the CSI)
        mean = row.mean()
        if row.mean() < 1e-20:
            indexes.append(index)
        else:
            df.iloc[index] = row / mean
    df = df.drop(indexes)
    # dfphase = dfphase.drop(indexes)

    # fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    # for i in range(10):
    #     idx = np.random.randint(0, len(df))
    #     ax1.plot(df.iloc[idx], label=r'$A_c$ ' + str(idx))
    #     ax2.plot(np.unwrap(dfphase.iloc[idx], discont=math.pi), label=r'$\angle_c$ ' + str(idx))
    # ax1.set_ylabel('Amplitude [a.u.]')
    # ax2.set_ylabel('Phase [rad]')
    # plt.xlabel('Subcarrier index')
    # # fig.suptitle('CSI Amplitude and Phase (40 MHz, one person)')
    # labels = np.arange(-244, 245, 61)
    # xticks(np.arange(0,len(df.columns)+1,61), labels, fontsize=10)
    # ax1.tick_params(axis='y', which='major', labelsize=10)
    # ax2.tick_params(axis='y', which='major', labelsize=10)
    # ax1.grid()
    # ax2.grid()
    # # plt.show()
    # plt.savefig('csi.pdf', bbox_inches='tight')
    # plt.close()

    return df.reset_index(drop=True)  # , dfphase.reset_index(drop=True)


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
