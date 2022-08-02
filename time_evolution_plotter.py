import os

from matplotlib import pyplot as pl


def plot_time_evolution_for_sc(df, unnecessary_plots):
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
