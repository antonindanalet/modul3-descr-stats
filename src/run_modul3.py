from read_data.read_data import read_data
from descr_stats.descr_stats import descr_stats


def run_modul3():
    code_of_delivery = '20222329'
    df_module3 = read_data(code_of_delivery)
    descr_stats(df_module3, code_of_delivery)


if __name__ == '__main__':
    run_modul3()
