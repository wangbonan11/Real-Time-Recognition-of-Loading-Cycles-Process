import time
def checkTime(data, input_time_start):
    timeArray_1 = time.strptime(input_time_start, "%Y-%m-%d %H:%M:%S")
    output_time_min = int(time.mktime(timeArray_1))
    workTime = 0
    restTime = 0
    reset_min_time = 15 * 60
    reset_arr=[]
    previousWorkTime = output_time_min
    s_time=data.loc[0, "update_time"]
    start_timeArray = time.localtime(s_time)
    start_time=time.strftime("%Y-%m-%d %H:%M:%S",start_timeArray)
    e_time=data.loc[len(data)-1, "update_time"]
    end_timeArray = time.localtime(e_time)
    end_time = time.strftime("%H:%M:%S", end_timeArray)
    for x in data.index:
        currentTime = data.loc[x, "update_time"]
        if (x == 0):
            restTime += currentTime - output_time_min;
            previousWorkTime = currentTime
            if (restTime >0 ):
                reset_arr.append(output_time_min)
            continue
        timeInterval = currentTime - previousWorkTime
        if (timeInterval >= reset_min_time):  # 休息
            restTime += timeInterval
            reset_arr.append(previousWorkTime)
        if(0 <timeInterval < reset_min_time):
            workTime += timeInterval
        previousWorkTime = currentTime
    mw,sw=divmod(workTime, 60)
    hw, mw = divmod(mw, 60)
    mr,sr=divmod(restTime, 60)
    hr, mr = divmod(mr, 60)
    print(f" Time {start_time} to {end_time}  ;  Total time of shovel loading operation = {int(hw)}h {int(mw)}m {int(sw)}s ; Total downtime of shovel  ={int(hr)}h {int(mr)}m {int(sr)}s")
    return start_time,end_time

