from read_data.read_data import read_data
from descr_stats.descr_stats import descr_stats


def run_modul3():
    df_module_3 = read_data()
    descr_stats(df_module_3)


if __name__ == '__main__':
    run_modul3()
