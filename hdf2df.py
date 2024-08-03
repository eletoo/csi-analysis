import os.path

import h5py
import pandas as pd


def hdf2csv(hdf_file: str, dir: str):
    """
    Convert the hdf5 file to csv files
    :param hdf_file: path to the hdf5 file
    :param dir: directory to save the csv files
    :param colnames: names of the columns
    :param unneeded: names of the unneeded columns
    """
    type = ['training', 'testing']
    with h5py.File(hdf_file, 'r') as f:
        for i in range(1, 6):
            for t in type:
                re = pd.DataFrame(f.get('rx' + str(i)).get(t)[:, :, 0])
                im = pd.DataFrame(f.get('rx' + str(i)).get(t)[:, :, 1])
                df = pd.DataFrame()
                df = df.append(re + 1j * im)
                # split the df in 8 parts and save them in 8 different csv files
                for j in range(0, 8):
                    df[1000 * j:1000 * (j + 1)].to_csv(os.path.join(dir, 'rx' + str(i) + '_' + t + str(j) + '.csv'),
                                                       index=False,
                                                       header=False)
