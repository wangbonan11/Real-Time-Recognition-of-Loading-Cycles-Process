import os
import pandas as pd
import numpy as np
import matplotlib
def read_file_csv(data_route_csv):
    '''
    :param data_route_csv:read csv
    :return: df is data
    '''
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.rcParams['agg.path.chunksize'] = 10000
    pd.set_option('display.max_columns', 2000)
    pd.set_option('display.max_rows', 2000)
    pd.set_option('display.width', 2000)
    os.chdir(data_route_csv)
    file_chdir = os.getcwd()
    filecsv = []
    for root, dirs, files in os.walk(file_chdir):
        for file in files:
            if os.path.splitext(file)[1] == '.csv':
                filecsv.append(file)
    df = pd.DataFrame()
    for csv in filecsv:
        df = df.append(pd.read_csv(csv, header=0, sep=',', encoding='UTF-8-sig', low_memory=False))

    time_value_name = ['update_time']
    params_motor = ['h_cur', 'h_vol', 'h_set', 'c_cur', 'c_vol', 'c_set', 's_cur', 's_vol', 's_set','h_tor', 'h_pow','unknow_1',
                    'c_vel', 'c_pow', 'c_tor', 'unknow_5', 's_pow',  'unknow_6','s_vel']
    params_gps = ['x', 'y', 'z', 'yaw', 'mode']
    df1 = df.loc[:, time_value_name + params_motor]
    a = list(range(-10, 10, 1))
    df1 = df1.replace(a, np.nan)
    df1 = df1.dropna(thresh=4)
    df_1v = df1.apply(lambda x: x * (1 / 15) if x.name in ['h_vol', 'c_vol', 's_vol', 'lw_vol', 'rw_vol','c_cur',"s_cur"] else x)
    df_1hc = df_1v.apply(lambda x: x * (1 / 10) if x.name in ['h_cur'] else x)
    df_1hp = df_1hc.apply(lambda x: x * (1 / 4) if x.name in ['unknow_1'] else x)
    df_1cp = df_1hp.apply(lambda x: x * (1 / 20) if x.name in ['c_tor','unknow_6'] else x)
    df_1set = df_1cp.apply(lambda x: x * (1 / -2.5) if x.name in ['h_set','c_set','s_set'] else x)
    df_1hv = df_1set.apply(lambda x: (x * (-1 / 20))+100 if x.name in ['h_tor'] else x)
    df_1htor = df_1hv.apply(lambda x: x * (-5) if x.name in ['h_pow'] else x)
    df_1cv = df_1htor.apply(lambda x: x * (-1 / 22) if x.name in ['c_vel'] else x)
    df_1ctor = df_1cv.apply(lambda x: x * (-1/13) if x.name in ['c_pow'] else x)
    df_1sv = df_1ctor.apply(lambda x: x * (-1 / 20) if x.name in ['unknow_5'] else x)
    df_1stor = df_1sv.apply(lambda x: x * (-1 /22) if x.name in ['s_pow'] else x)
    data_part = df_1stor.apply(lambda x: x * (1 / -4) if x.name in ['s_vel'] else x)
    return df,data_part
