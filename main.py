import os


def is_stationary(batch_mean, column_mean):
    return abs(batch_mean - column_mean) < 0.1 * column_mean


def elaborate_batch(column_mean, batch, size):
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


def plot_histogram_for_sc(title, df, size=365):  # customizable: ho usato 365 perché divisore di 1825
    col = df[title]

    c = pd.DataFrame(abs(complex(value.replace(" ", "").replace("i", "j"))) for value in col)

    print(title)
    column_mean = float(c.mean())
    print("Column mean:", column_mean)

    plottable = True
    for batch in create_batches(df, size):
        if elaborate_batch(column_mean, batch[title], size):
            continue
        plottable = False

    # if plottable:
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


if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as pl

    path = os.getcwd() + '\\csi.csv'

    colnames = ["SC" + str(i) for i in range(0, 256)]
    df = pd.read_csv(path, names=colnames, header=None)

    # colnames = ['SC0', 'SC10', 'SC20', 'SC30', 'SC40', 'SC50', 'SC60', 'SC70', 'SC80', 'SC90', 'SC100', 'SC200',
    # 'SC255']

    for title in colnames:
        plot_histogram_for_sc(title, df)
