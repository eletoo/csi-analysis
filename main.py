import os

from histograms import plot_histogram_for_sc
from increments import plot_increments_for_sc
from time_evolution import plot_time_evolution_for_sc
import autocorrelation
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
    print("-------------------------")
    return input("Choose an action: ")


if __name__ == '__main__':

    ########## INFORMATION SETUP ##########
    csv_file = 'capture0.csv'  # file containing the data to be processed
    dst_folder = 'capture0'  # folder path where to save the output of the code, can be an empty string
    BW = 40  # channel bandwidth: 20, 40, 80 MHz
    STD = 'ax'  # modulation: ax, ac
    #######################################

    path = os.path.join(os.getcwd(), csv_file)

    num_sc = 3.2 * BW
    if STD == 'ax':
        num_sc = num_sc * 4

    colnames = ["SC" + str(i) for i in range(0, int(num_sc))]
    df = pd.read_csv(path, names=colnames, header=None)

    with open(os.path.join(os.getcwd(), "dontPlot/unnecessaryPlots" + str(BW) + STD)) as f:
        unnecessary_plots = f.read().splitlines()

    for title in df:
        if title in unnecessary_plots:
            del df[title]
        else:
            # format complex numbers into readable values
            df[title] = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in df[title])

    # removing impact of AGC on data
    for index, row in df.iterrows():
        # each row is a time sample over the sub-carriers (frequencies)
        # compute the mean amplitude over the frequencies and normalize the values by it (i.e. by the energy of the CSI)
        mean = row.mean()
        df.iloc[index] = row / mean

    choice = -1
    while choice != 0:
        choice = int(print_menu())
        if choice == 0:  # exit
            pass
        if choice == 1:
            batch_size = len(df)
            for x in reversed(range(1, len(df))):  # create batches of size x (as long as possible)
                if len(df) % x == 0:
                    batch_size = x
                    break
            for title in df:
                plot_histogram_for_sc(title, df, batch_size, path=dst_folder)
        elif choice == 2:
            plot_time_evolution_for_sc(df, path=dst_folder)
        elif choice == 3:
            plot_increments_for_sc(df, path=dst_folder)
        elif choice == 4:
            autocorrelation.plot_autocorrelation(df, path=dst_folder)
