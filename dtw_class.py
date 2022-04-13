def dtw_detec(data,angle_cycle_time,result_short_data,result_long_data):
    """
    :param data:is all cycles data
    :param angle_cycle_time: are key point of every cycle(startIndex,endIndex,timeInterval, jiaoduMin,jiaoduMax
                                                          jiaoduChazhi,jiaoduMin_index, jiaoduMax_index)
    :param result_short_data:DTW short score
    :param result_long_data:DTW long score
    :return: angle_cycle_time (class) state=0 is cleaning work; state=1 is loading work; class=1 is long work;class=2 is short work;
    """
    up_num=0
    wait_num=0
    for x in angle_cycle_time.index:
        dtw_short_score=result_short_data[x]
        dtw_long_score = result_long_data[x]
        circle_data = data[x]
        circle_start_index = angle_cycle_time.loc[x, "startIndex"]
        max_jiaodu_index = angle_cycle_time.loc[x, "jiaoduMax_index"]
        angle_cycle_time.loc[x, "up_start_index"] = circle_start_index+5
        for j in range(int(circle_start_index+6), int(max_jiaodu_index - 2)):
            current_yaw = circle_data.loc[j, "yaw"]
            next_yaw = circle_data.loc[j + 1, "yaw"]
            if next_yaw - current_yaw >5:
                up_num += 1
                if up_num > 4:
                    angle_cycle_time.loc[x, "up_start_index"] = j
            else:
                up_num=0
        if dtw_short_score<9 and dtw_long_score<9:
            angle_cycle_time.loc[x, "state"] = 1
            up_start_index=angle_cycle_time.loc[x, "up_start_index"]
            angle_cycle_time.loc[x, "class"] = 2
            for k in range(int(up_start_index), int(max_jiaodu_index - 5)):
                current_yaw = circle_data.loc[k, "yaw"]
                next_yaw = circle_data.loc[k + 1, "yaw"]
                if next_yaw - current_yaw <= 4:
                    wait_num += 1
                    if wait_num >10:
                     angle_cycle_time.loc[x, "class"] = 1
        else:
            angle_cycle_time.loc[x, "state"]=0
            angle_cycle_time.loc[x, "class"] = 0
        up_num = 0
        wait_num = 0
    return angle_cycle_time
