import netCDF4 as nc
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import math
import xarray as xr

# 打开nc文件
with xr.open_dataset('H:\Py-nc-pshw-test\py_nc\PSHW\prob_cd_end_rm_maize_rain_long.nc4') as dataset:

    # 提供要获取值的经纬度坐标
    lon = 115.25
    lat = 34.25

    # 获取特定经纬度上的值
    value = dataset['var'].sel(lon=lon, lat=lat,time='2000-07-18', method='nearest').item()

    # 打印结果
    # print("经度:", lon)
    # print("纬度:", lat)
    # print("对应的值:", value)
    # 获取 time 变量的值数组
    time_values = dataset['time'].values

    # 打印结果
    print("time 变量的值数组：")
    # print(time_values)
    for k,i in enumerate(time_values):
        # print(type(i))
        # print(i)
        value=dataset['var'].sel(lon=lon, lat=lat,time=i, method='nearest').item()
        print(k+1)
        print(value)
# dataset.close()