import os

import matplotlib.pyplot as pl


def plot_increments_for_sc(df, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "increments_hist")):
        os.mkdir(os.path.join(path, "increments_hist"))

    # plot(df.diff(), path)
    sum = 0
    for column in df.diff().drop(labels=0, axis=0):
        sum = sum + df.diff().drop(labels=0, axis=0)[column].mean()
    with open(os.path.join(path, "mean_increments.txt"), "w") as f:
        f.write(str(sum / len(df.columns)))
    with open(os.path.join(path, "variance_incr.txt"), "w") as f:
        f.write(str(max([df[title].diff().dropna().var() for title in df])))


def plot_superimposed_increments(real, artificial, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "superimposed_increments")):
        os.mkdir(os.path.join(path, "superimposed_increments"))

    for title in real:
        pl.hist(real[title], label="Real", bins=100, alpha=0.5)
        pl.hist(artificial[title].diff(), label="Artificial", bins=100, alpha=0.5)
        pl.xlabel('Increment')
        pl.ylabel('Frequency')
        pl.title(title)
        pl.rcParams.update({'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large',
                            'ytick.labelsize': 'large'})
        pl.legend()
        pl.savefig(os.path.join(os.getcwd(), path, 'superimposed_increments', 'figure' + str(title) + '.pdf'))
        print("Plotting superimposed increments " + str(title))
        pl.close()


def plot(df, path):
    for title in df:
        pl.figure(figsize=(6, 2.5))
        df[title].hist(bins=100)
        pl.xlabel('Increment', fontsize=12)
        pl.ylabel('Frequency', fontsize=12)
        lim = max(abs(df[title].min()), abs(df[title].max()))
        pl.xlim(-lim, lim)
        # pl.title(title)
        pl.rcParams.update({'axes.titlesize': 'large', 'axes.labelsize': 'large', 'xtick.labelsize': 'large',
                            'ytick.labelsize': 'large'})
        pl.savefig(os.path.join(os.getcwd(), path, 'increments_hist', 'figure' + str(title) + '.pdf'),
                   bbox_inches='tight')
        print("Plotting histogram " + str(title))
        pl.close()
