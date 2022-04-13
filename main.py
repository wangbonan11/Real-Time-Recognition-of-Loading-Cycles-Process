import pandas as pd
from datetime import datetime
import aread_data
import time_check
import TimeCheck
import CutData_angle as cda
import dtw_test,dtw_class
import real_time_identification_result
floor_h=230
input_time_start = '2021-4-23 00:00:00'
input_time_end = '2021-4-23 23:59:59'

def time2stamp(cmnttime):
    cmnttime = datetime.strptime(str(cmnttime), '%Y/%m/%d %H:%M:%S')
    stamp = datetime.timestamp(cmnttime)
    return stamp
df_data,df_motor=aread_data.read_file_csv('D:/Doctor/date/shoveldata/shovel423/2021-4-23')
time_value_name = ['update_time']
params_motor = ['h_cur', 'h_vol', 'h_set', 'c_cur', 'c_vol', 'c_set', 's_cur', 's_vol', 's_set',
                'h_tor', 'h_pow','unknow_1','c_vel', 'c_pow', 'c_tor', 'unknow_5', 's_pow', 'unknow_6', 's_vel']
params_gps = ['x', 'y', 'z', 'yaw', 'mode']
df_motor.loc[:,time_value_name[0]] =df_motor.loc[:, time_value_name[0]].apply(time2stamp)
df_1=df_motor.reset_index(drop=True)
time_check.checkUpdateTime(df_1, "update_time", input_time_start, input_time_end)
df_1.drop_duplicates(subset=time_value_name, keep='first', inplace=True)
df2 = df_data.loc[:, time_value_name + params_gps]
df2['yaw'] = df2['yaw'].astype(str)
df2 = df2[df2['yaw'].str.contains('[+]?[\d]{1,3}[\.][\d]+')]
df2=df2[(df2['z']<floor_h+10) ]
df2=df2[(df2['z']>floor_h-10)]
df_2=df2[df2['mode']==4].copy()
df_2.loc[:,'update_time']= df_2.loc[:, 'update_time'].apply(time2stamp)
df_2.drop_duplicates(subset=time_value_name, keep='first', inplace=True)
df3= pd.merge(df_1, df_2, on=time_value_name[0])
df_combine_0=df3.fillna(0)
df_combine_0["h_power_value"]=df_combine_0["h_tor"].mul(df_combine_0["h_cur"])
df_combine_0["c_power_value"]=df_combine_0["c_vel"].mul(df_combine_0["c_pow"])
df_combine_0 =df_combine_0.reset_index(drop=True)
print(f" Data rows and columns: {df_combine_0.shape}" )
start_time,end_time=TimeCheck.checkTime(df_combine_0, input_time_start)
df_combine_0.loc[:,'yaw'] = df_combine_0.loc[:,'yaw'].astype(float).round(1)
for current_index in df_combine_0.loc[:,'yaw'].index:
    if current_index == 0:
        continue
    front_index = current_index - 1
    if df_combine_0.loc[front_index,'yaw']-df_combine_0.loc[current_index,'yaw'] >100 :
        origin_data = df_combine_0.loc[current_index,'yaw']
        add_after_value = origin_data + (df_combine_0.loc[front_index,'yaw']-df_combine_0.loc[current_index,'yaw'])
        df_combine_0.loc[current_index, 'yaw'] = add_after_value
    if df_combine_0.loc[current_index, 'yaw'] <150:
        df_combine_0.loc[current_index, 'yaw'] = df_combine_0.loc[front_index, 'yaw']
df_combine_0 = df_combine_0.apply(lambda x: (x*(-1)+620-260) if x.name in ['yaw'] else x)
angle_cycle_time={}
angle_cycle_time = pd.DataFrame(angle_cycle_time)
cut_data_result_cycle = cda.cut_data(df_combine_0, "update_time", "yaw", 'h_tor',angle_cycle_time)
shovel_cycles=len(cut_data_result_cycle)
print(f' Working cycles number = {shovel_cycles} ')
input_time_seg_start = '2021-4-23 13:28:40'
input_time_seg_end = '2021-4-23 13:40:59'
dis_short_result,dis_long_result=dtw_test.test_template(cut_data_result_cycle)
dtw_class.dtw_detec(cut_data_result_cycle, angle_cycle_time,dis_short_result,dis_long_result)
real_time_identification_result.show_cut_data(df_combine_0,cut_data_result_cycle,angle_cycle_time,input_time_seg_start,input_time_seg_end,"yaw")

