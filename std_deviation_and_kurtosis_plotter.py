import os
import pandas
import math
import matplotlib.pyplot as plt


def plot_std_dev_and_kurtosis(df: pandas.DataFrame, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "params")):
        os.mkdir(os.path.join(path, "params"))

    df1 = df.diff().drop(labels=0, axis=0)
    std_devs = []
    kurtosis = []
    for title in df1:
        numerator = 0
        for data in df1[title]:
            numerator += pow((data - df1[title].mean()), 2)
        std_devs.append(math.sqrt(numerator / (df1[title].size - 1)))

        num = 0
        for data in df1[title]:
            num += pow((data - df1[title].mean()), 4)
        kurtosis.append((num / pow(df1[title].STD(), 4) / df1[title].size) - 3)

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(std_devs, 'g-')
    ax2.plot(kurtosis, 'b-')
    ax1.set_xlabel('Sub-carrier')
    ax1.set_ylabel('Standard deviation of the increments', color='g')
    ax2.set_ylabel('Kurtosis of the increments', color='b')
    # plt.show()
    plt.savefig(os.path.join(os.getcwd(), path, 'params', 'std_deviation_and_kurtosis.pdf'))
