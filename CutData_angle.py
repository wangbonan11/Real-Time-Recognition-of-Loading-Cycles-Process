import pandas as pd
def cut_data(data,time_key,jiaodu_key,hoist_key,angle_cycle_time):
    data_result = []
    time_min_interval = 25
    down_time_min_interval = 5
    jiaodu_qujian_min =30
    jiaodu_qujian_max =135
    start_min_index = 0
    start_max_index = 0
    maxIndex = len(data)
    current_circle_start_index = 0;
    search_status=0
    t_num=0
    down_num=0
    t_dig=5
    t_down=6
    jiaodu_down_min=20
    for x in data.index:
        if (x == 0) :
            start_max_index = 0;
            start_min_index=0;
            current_circle_start_index = 0;
        elif((x + 1) == maxIndex):
            data.loc[current_circle_start_index: x, :]
        else:
            last_jioaodu = data.loc[x - 1, jiaodu_key]
            current_jioadu = data.loc[x, jiaodu_key]
            next_jiaodu = data.loc[x + 1, jiaodu_key]
            current_time = data.loc[x, time_key]
            if search_status==0:
                    if current_jioadu-next_jiaodu<=-2 or current_jioadu-next_jiaodu<=2:
                        t_num+=1
                        if t_num>=t_dig:
                          search_status =1
                          current_circle_start_index = x -5
                    else:
                        search_status == 0
                        t_num=0
                        continue
            elif search_status==1:
                if (current_jioadu >= last_jioaodu):
                    max_jiaodu = data.loc[start_max_index, jiaodu_key];
                    if (current_jioadu > max_jiaodu):
                        start_max_index = x;
                        search_status = 1
                        max_jiaodu = data.loc[start_max_index, jiaodu_key]
                else:
                    down_num += 1
                    min_jiaodu = data.loc[start_min_index, jiaodu_key]
                    if (current_jioadu < min_jiaodu):
                        start_min_index = x;
                        search_status = 1
                    if (current_jioadu <= next_jiaodu) and down_num>=t_down and max_jiaodu-current_jioadu>=jiaodu_down_min:
                        current_circle_start_time = data.loc[current_circle_start_index, time_key]
                        time_interval = current_time - current_circle_start_time
                        if (time_interval >= time_min_interval):
                            max_jiaodu = data.loc[start_max_index, jiaodu_key]
                            min_jiaodu = data.loc[start_min_index, jiaodu_key]
                            jiaodu_chazhi = max_jiaodu - min_jiaodu
                            if (jiaodu_chazhi > jiaodu_qujian_max):
                                start_min_index = x;
                                start_max_index = x;

                            if (jiaodu_chazhi >= jiaodu_qujian_min and jiaodu_chazhi <= jiaodu_qujian_max):
                                if (x - start_max_index <=down_time_min_interval):
                                    continue
                                if (isInvalidData(data, current_circle_start_index, x)):
                                    createDateFrame(angle_cycle_time, current_circle_start_index, x, time_interval, min_jiaodu, max_jiaodu, jiaodu_chazhi, start_min_index, start_max_index)
                                    result_to_add = data.loc[current_circle_start_index: x, :]
                                    data_result.append(result_to_add);
                                    t_num = 0
                                    down_num=0
                                    t_dig = 5
                                    t_down = 5
                                    jiaodu_down_min = 25
                                    search_status=0
                                    start_min_index = x+1 ;
                                    start_max_index = x+1;
                                    current_circle_start_index = x+1;
    return data_result

def createDateFrame(angle_cycle_time, startIndex, endIndex, timeInterval, jiaoduMin, jiaoduMax, jiaoduChazhi, jiaoduMin_index, jiaoduMax_index):
    data_length = len(angle_cycle_time);
    angle_cycle_time.loc[data_length, 'startIndex'] = startIndex
    angle_cycle_time.loc[data_length, 'endIndex'] = endIndex
    angle_cycle_time.loc[data_length, 'timeInterval'] = timeInterval
    angle_cycle_time.loc[data_length, 'jiaoduMin'] = jiaoduMin
    angle_cycle_time.loc[data_length, 'jiaoduMax'] = jiaoduMax
    angle_cycle_time.loc[data_length, 'jiaoduChazhi'] = jiaoduChazhi
    angle_cycle_time.loc[data_length, 'jiaoduMin_index'] = jiaoduMin_index
    angle_cycle_time.loc[data_length, 'jiaoduMax_index'] = jiaoduMax_index

def isInvalidData(data, circle_start_index, circleEndIndex):
    h_cur_valid = 400
    c_cur_valid = 150
    hCurIsValid = 0
    cCurValid = 0
    for x in range(int(circle_start_index), int(circleEndIndex)):
        h_curValue = data.loc[x, "h_power_value"];
        c_curValue = data.loc[x, "c_power_value"];
        if (hCurIsValid == 0 and h_curValue >= h_cur_valid):
            hCurIsValid = 1
        if (cCurValid == 0 and c_curValue >= c_cur_valid):
            cCurValid = 1
    if (hCurIsValid == 1 and cCurValid == 1 ):
        return True
    else:
        return False
