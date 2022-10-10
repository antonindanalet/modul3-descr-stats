import pandas as pd
from pathlib import Path


def read_data():
    try:
        df_module_3 = pd.read_csv(Path('../data/input/modul3.csv'))
    except FileNotFoundError:
        raise Exception('No raw data file in data/input/!')
    return df_module_3
