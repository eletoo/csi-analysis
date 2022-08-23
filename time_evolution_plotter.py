import os

from matplotlib import pyplot as pl


def plot_time_evolution_for_sc(df):
    if not os.path.exists("time_evolution"):
        os.mkdir("time_evolution")

    for title in df:
        pl.plot(df[title])
        pl.xlabel("Packet")
        pl.ylabel("Magnitude")
        pl.savefig(os.path.join(os.getcwd(), 'time_evolution', 'figure' + title + '.png'))
        pl.close()
        print("plotting graph " + title)
