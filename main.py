import os


def is_stationary(batch_mean, column_mean):
    return abs(batch_mean - column_mean) < 0.1 * column_mean


def process_batch(column_mean, batch, size):
    sum = 0
    for value in batch:
        value = complex(value.replace(" ", "").replace("i", "j"))
        sum += abs(value)

    batch_mean = sum / size
    print(batch_mean)
    if not is_stationary(batch_mean, column_mean):
        print("Non stationary process")
        return False
    else:
        return True


def create_batches(data, length):
    return [data[i:i + length] for i in range(0, len(data), length)]


def plot_histogram_for_sc(title, df, unnecessary_plots, size=365):  # customizable: size is set as 365 because it
    # divides the column length in 5 batches of the same size

    if title not in unnecessary_plots:
        col = df[title]

        c = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in col)

        print(title)
        column_mean = float(c.mean())
        print("Column mean:", column_mean)

        # plottable = True
        # for batch in create_batches(df, size):
        #   if process_batch(column_mean, batch[title], size):
        #      continue
        #   plottable = False

        # if plottable:
        #   plot(c, column_mean, title)

        # remove previous comments and instead comment the following three lines if the plot is only needed for
        # stationary processes
        for batch in create_batches(df, size):
            process_batch(column_mean, batch[title], size)
        plot(c, column_mean, title)


def plot(c, column_mean, title):
    c = c - column_mean
    c.hist(bins=100, density=True)
    pl.xlabel('Magnitude')
    pl.ylabel('Relative frequency')
    pl.title(title)
    pl.xlim(-150, 150)
    # pl.show()
    if not os.path.exists("histograms"):
        os.mkdir("histograms")
    pl.savefig(os.getcwd() + '\\histograms\\figure' + title + '.png')
    pl.close()


def plot_time_evolution(df, unnecessary_plots):
    if not os.path.exists("time_evolution"):
        os.mkdir("time_evolution")

    for title in df:
        if title not in unnecessary_plots:
            col = df[title]
            y = [abs(complex(value.replace(" ", "").replace("i", "j"))) for value in col]
            pl.plot(y)
            pl.xlabel("Packet")
            pl.ylabel("Magnitude")
            pl.savefig(os.getcwd() + '\\time_evolution\\figure' + title + '.png')
            pl.close()
            print("plotting graph " + title)


if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as pl

    path = os.getcwd() + '\\csi.csv'

    colnames = ["SC" + str(i) for i in range(0, 256)]
    df = pd.read_csv(path, names=colnames, header=None)

    # colnames = ['SC0', 'SC10', 'SC20', 'SC30', 'SC40', 'SC50', 'SC60', 'SC70', 'SC80', 'SC90', 'SC100', 'SC200',
    # 'SC255']

    with open(os.getcwd() + "\\unnecessaryPlots") as f:
        unnecessary_plots = f.read().splitlines()

    for title in colnames:
        plot_histogram_for_sc(title, df, unnecessary_plots)

    response = input("Plot evolution in time for each sub-carrier? [Y/n]")
    if response.lower() == "y" or response == '':
        plot_time_evolution(df, unnecessary_plots)
    if response.lower() == "n":
        quit()