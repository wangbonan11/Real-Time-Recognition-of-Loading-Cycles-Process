import time
def checkUpdateTime(data,time_key, input_time_start, input_time_end):
    timeArray_1 = time.strptime(input_time_start, "%Y-%m-%d %H:%M:%S")
    timeArray_2 = time.strptime(input_time_end, "%Y-%m-%d %H:%M:%S")
    output_time_min = int(time.mktime(timeArray_1))
    output_time_max = int(time.mktime(timeArray_2))
    first_valid_data_index = 0
    for x in data.index:
        if (x > 0):
            last_index = x-1
            last_update_time = data.loc[last_index, time_key]
            if (last_update_time >= output_time_min ):
                if (last_update_time <= output_time_max):
                    if (first_valid_data_index != 0):
                        first_valid_data_index = x - 2;
                        while (first_valid_data_index >= 0):
                            data.loc[first_valid_data_index, time_key] = data.loc[first_valid_data_index + 1, time_key]
                            first_valid_data_index -=1
                        first_valid_data_index = 0

                    update_time = data.loc[x, time_key]
                    if(update_time < output_time_min or update_time > output_time_max):
                        data.loc[x, time_key] = last_update_time + 1
            else:
                first_valid_data_index +=1