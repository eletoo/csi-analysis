import os

from matplotlib import pyplot as pl


def plot_time_evolution_for_sc(df, path: str = ""):
    if path != "" and not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(os.path.join(path, "time_evolution")):
        os.mkdir(os.path.join(path, "time_evolution"))

    for title in df:
        pl.plot(df[title])
        pl.xlabel("Packet")
        pl.ylabel("Magnitude")
        pl.savefig(os.path.join(os.getcwd(), path, 'time_evolution', 'figure' + str(title) + '.png'))
        pl.close()
        print("plotting graph " + str(title))
