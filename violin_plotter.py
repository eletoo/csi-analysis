import os
import matplotlib.pyplot as pl


def plot_violin(df, path=""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "violin")):
        os.mkdir(os.path.join(path, "violin"))

    # plot violin plot for mean values
    pl.violinplot(df.diff().drop(labels=0, axis=0).mean())
    pl.title('Mean - violin plot')
    pl.savefig(os.path.join(os.getcwd(), path, 'violin', 'mean_violin.png'))
    pl.grid()
    pl.close()

    # plot violin plot for variances
    pl.violinplot(df.diff().drop(labels=0, axis=0).var())
    pl.title('Variance - violin plot')
    pl.savefig(os.path.join(os.getcwd(), path, 'violin', 'variance_violin.png'))
    pl.grid()
    pl.close()
