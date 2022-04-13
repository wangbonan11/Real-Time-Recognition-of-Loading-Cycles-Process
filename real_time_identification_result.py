import time
import matplotlib.pyplot as plt
def show_cut_data(df_combine_0,cut_data_result,angle_cycle_time,input_time_seg_start,input_time_seg_end,key_parameter):
    """
    :param df_combine_0:realorignal data
    :param cut_data_result:loading cycles [[],[],[]]
    :param angle_cycle_time:key point of each loading cycle
    :param input_time_seg_start:start time
    :param input_time_seg_end:end time
    :param shovel_cycles:number
    :return: result plot
    """
    timeArray_1 = time.strptime(input_time_seg_start, "%Y-%m-%d %H:%M:%S")
    timeArray_2 = time.strptime(input_time_seg_end, "%Y-%m-%d %H:%M:%S")
    tex1 = int(time.mktime(timeArray_1))
    tex2 = int(time.mktime(timeArray_2))
    fig = plt.figure(figsize=(8, 3), dpi=180)
    axes_yaw = fig.add_subplot(1, 1, 1)
    axes_yaw.spines['top'].set_linewidth(1.5)
    axes_yaw.spines['left'].set_linewidth(1.5)
    axes_yaw.spines['right'].set_linewidth(1.5)
    axes_yaw.spines['bottom'].set_linewidth(1.5)
    plt.grid(b=True, axis='both', color='grey', linestyle='-.', linewidth=0.15)
    plt.rc("font", family="Times New Roman")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    axes_yaw.plot(df_combine_0['update_time'], df_combine_0[key_parameter], "--", markersize=0.4, linewidth=0.5, color='black', alpha=0.9)
    plt.xlim(tex1, tex2)
    plt.ylim(-100, 260)
    plt.ylabel("swing angle /o", fontsize=12)
    plt.xlabel("time /s", fontsize=12)
    plt.title("Original Signal", fontsize=12)
    plt.tick_params(axis='both', labelsize=10, direction='in', pad=2.5)

    fig2 = plt.figure(figsize=(8, 3), dpi=180)
    axes_yaw_dec = fig2.add_subplot(1, 1, 1)
    axes_yaw_dec.spines['top'].set_linewidth(1.5)
    axes_yaw_dec.spines['left'].set_linewidth(1.5)
    axes_yaw_dec.spines['right'].set_linewidth(1.5)
    axes_yaw_dec.spines['bottom'].set_linewidth(1.5)
    plt.grid(b=True, axis='both', color='grey', linestyle='-.', linewidth=0.15)
    p=0
    shovel_short_num=0
    shovel_long_num = 0
    for cut_data_result_item in cut_data_result:
        circle_data = cut_data_result_item
        circle_data_len = len(circle_data)
        circle_data_arr = circle_data.index
        start1 = circle_data_arr[0]
        end1 = start1 + circle_data_len - 1
        if angle_cycle_time.loc[p, "class"] ==1:
            Ct="red"
            shovel_long_num += 1
        elif angle_cycle_time.loc[p, "class"] ==2:
            Ct="blue"
            shovel_short_num += 1
        else:
            Ct = "w"
        p += 1
        axes_yaw_dec.plot(df_combine_0.loc[start1:end1, 'update_time'], df_combine_0.loc[start1:end1,key_parameter], "-", linewidth=1,color=Ct, alpha=0.9)
        axes_yaw_dec.plot(df_combine_0.loc[start1, 'update_time'], df_combine_0.loc[start1, key_parameter], "o", c="black",linewidth=0.5,markersize=3, markerfacecolor='none', alpha=0.9)
        axes_yaw_dec.plot(df_combine_0.loc[end1, 'update_time'], df_combine_0.loc[end1, key_parameter], "o", c="black",linewidth=0.5,markersize=3, markerfacecolor='none', alpha=0.9)
    shovel_cycles_num=shovel_short_num+shovel_long_num
    plt.rc("font", family="Times New Roman")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    axes_yaw_dec.plot(df_combine_0['update_time'], df_combine_0[key_parameter], "--", markersize=0.4, linewidth=0.5,color='black', alpha=0.9)
    plt.xlim(tex1, tex2)
    plt.ylim(-100, 260)
    plt.ylabel("swing angle /o", fontsize=12)
    plt.xlabel("time /s", fontsize=12)
    plt.tick_params(axis='both', labelsize=10, direction='in', pad=2.5)
    plt.title(f"All Cycles: {shovel_cycles_num}  Short Cycles: {shovel_short_num}  Long Cycles: {shovel_long_num}  DTW=0.54", fontsize=10)
    plt.show()

