import os

import pandas as pd

import quantize
from setup import set_params


def clean(capturepath, outpath, bw, STD, unneeded_dir, q_ampl):
    # remove any spurious data
    num_sc, colnames, _ = set_params(bw, STD, unneeded_dir)
    capture = pd.read_csv(capturepath, names=colnames, header=None)
    capture = capture.dropna(axis=1)
    for title in capture:  # todo: do this on a copy of the dataframe and save the filtered original to file
        capture[title] = pd.DataFrame(
            abs(complex(value.replace(" ", "").replace("i", "j").replace("(", "").replace(")", ""))) for value
            in capture[title])

    mean_csi = quantize.mean_csi_comp(capture[0:30]).round()  # compute the mean csi of the first 100 traces
    indexes = []
    for index, csi in capture.iterrows():
        normfact = num_sc * ((2 ** q_ampl) - 1)
        if sum(pd.Series(abs(mean_csi - csi))) / normfact > 0.2:  # todo: change threshold if more precision is needed
            # if the csi is too different from the mean csi drop it
            indexes.append(index)

    for e in indexes:
        capture.drop(e, inplace=True)

    capture.to_csv(outpath, index=False, header=False)  # N.B. the content of the file is no double values, not complex
    return 0


if __name__ == '__main__':
    unneeded_dir = 'dontPlot/unnecessaryPlots' + str(80) + "ax"  # list of suppressed sub-carriers

    out = '80ax/0ppl/'
    if not os.path.exists(out):
        os.makedirs(out)

    for i in range(3, 6):  # TODO: change range after tests are finished
        clean("80ax/0ppl/unfiltered/capture" + str(i) + ".csv",
              out + "capture" + str(i) + ".csv",
              80,
              'ax',
              unneeded_dir,
              10)
