from numpy import array, zeros, argmin, inf, equal, ndim
import pandas as pd
from sklearn.metrics.pairwise import manhattan_distances
import numpy as np

def noramlization(data):
  minVals = data.min(0)
  maxVals = data.max(0)
  ranges = maxVals - minVals
  np.zeros(np.shape(data))
  m = data.shape[0]
  normData = data - np.tile(minVals, (m, 1))
  normData = normData/np.tile(ranges, (m, 1))
  return normData

def test_template(data):
    """
    :param data:
    :return:
    """
    result_long_data=[]
    s1 = pd.read_csv('D:/Doctor/date/shoveldata/shovel417/wait_class/wait_class.csv', sep=',', encoding='UTF-8-sig')
    s1 = list(map(lambda x: x[0], noramlization(s1).values.tolist()))
    for i in range(len(data)):
        cycle_date = data[i]
        s2 = cycle_date[:][['yaw']]
        t_data= noramlization(s2).values.tolist()
        s2 = list(map(lambda x:x[0],t_data))
        r, c = len(s1), len(s2)
        D0 = zeros((r+1,c+1))
        D0[0,1:] = inf
        D0[1:,0] = inf
        D1 = D0[1:,1:]
        for i in range(r):
            for j in range(c):
                D1[i,j] = manhattan_distances(s1[i],s2[j])
        M = D1.copy()
        for i in range(r):
            for j in range(c):
                D1[i,j] += min(D0[i,j],D0[i,j+1],D0[i+1,j])
        i,j = array(D0.shape) - 2
        p,q = [i],[j]
        while(i>0 or j>0):
            tb = argmin((D0[i,j],D0[i,j+1],D0[i+1,j]))
            if tb==0 :
                i-=1
                j-=1
            elif tb==1 :
                i-=1
            else:
                j-=1
            p.insert(0,i)
            q.insert(0,j)
        dis=D1[-1,-1]
        result_long_data.append(dis)
    result_short_data = []
    short = pd.read_csv('D:/Doctor/date/shoveldata/shovel417/classtemplate/shortclass.csv', sep=',', encoding='UTF-8-sig')
    short = list(map(lambda x: x[0], noramlization(short).values.tolist()))
    for i in range(len(data)):
        cycle_date = data[i]
        s2 = cycle_date[:][['yaw']]
        t_data = noramlization(s2).values.tolist()
        s2 = list(map(lambda x: x[0], t_data))
        r, c = len(short), len(s2)
        D0 = zeros((r + 1, c + 1))
        D0[0, 1:] = inf
        D0[1:, 0] = inf
        D1 = D0[1:, 1:]
        for i in range(r):
            for j in range(c):
                D1[i, j] = manhattan_distances(short[i], s2[j])
        M = D1.copy()
        for i in range(r):
            for j in range(c):
                D1[i, j] += min(D0[i, j], D0[i, j + 1], D0[i + 1, j])
        i, j = array(D0.shape) - 2
        p, q = [i], [j]
        while (i > 0 or j > 0):
            tb = argmin((D0[i, j], D0[i, j + 1], D0[i + 1, j]))
            if tb == 0:
                i -= 1
                j -= 1
            elif tb == 1:
                i -= 1
            else:
                j -= 1
            p.insert(0, i)
            q.insert(0, j)
        dis = D1[-1, -1]
        result_short_data.append(dis)
    return result_short_data,result_long_data
