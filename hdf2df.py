import os.path

import h5py
import pandas as pd


def hdf2csv(hdf_file: str, outdir: str):
    """
    Convert the hdf5 file to csv files. This method is used to convert the hdf5 files from the Antisense project to csv.
    Data can be retrieved at: https://zenodo.org/records/5885636
    File structure is described in the README file of the Antisense project.
    Compatibility with other hdf5 files is not guaranteed.
    :param hdf_file: path to the hdf5 file
    :param outdir: directory to save the csv files
    """
    type = ['training', 'testing']
    with h5py.File(hdf_file, 'r') as f:
        for i in range(1, 6):
            for t in type:
                re = pd.DataFrame(f.get('rx' + str(i)).get(t)[:, :, 0])
                im = pd.DataFrame(f.get('rx' + str(i)).get(t)[:, :, 1])
                df = pd.DataFrame()
                df = df.append(re + 1j * im)
                for j in range(0, 8):
                    df[1000 * j:1000 * (j + 1)].to_csv(os.path.join(outdir, 'rx' + str(i) + '_' + t + str(j) + '.csv'),
                                                       index=False,
                                                       header=False)
