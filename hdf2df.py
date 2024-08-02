import h5py
import pandas as pd


def hdf2df(hdf_file: str):
    with h5py.File(hdf_file, 'r') as f:
        re = pd.DataFrame(f.get('rx1').get('training')[:, :, 0])
        im = pd.DataFrame(f.get('rx1').get('training')[:, :, 1])
        # create a dataframe from the dictionary where each row is a CSI, made of 242 elements
        # each element is a string in the form re+i*im
        df = pd.DataFrame()
        return df.append(re + 1j * im)
