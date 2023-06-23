import netCDF4 as nc
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import math
def depose1(x):
    nearest_number = math.floor(x) + 0.25 if (x % 1) <= 0.5 else math.floor(x) + 0.75
    return nearest_number
def getdate(input_date_str):
    # 将字符串转换为日期格式
    input_date_str=str(input_date_str)
    input_date = datetime.strptime(input_date_str, "%Y%m%d")

    # 获取一年中的第几天
    day_of_year = input_date.timetuple().tm_yday
    return day_of_year
# 读取.nc4文件
nc_file = nc.Dataset(r"H:\Py-nc-pshw-test\py_nc\PSHW\prob_cd_end_rm_maize_rain_long.nc4")
csv_file=r'H:\Py-nc-pshw-test\py_nc\coord.txt'
df = pd.read_csv(csv_file)
# 读取coord字段中的纬度和经度信息
nc_lat = nc_file.variables["lat"][:]
nc_lon = nc_file.variables["lon"][:]
nc_time=nc_file.variables["time"][:]
value_values = nc_file.variables['var'][:]
# print(df['lat'])
# print(nc_lat)
# df.to_csv("your_output.csv", index=False)
# start_date = datetime.datetime(year=1900, month=1, day=1)
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    header = ['lat', 'lon']
    for time_idx, time in enumerate(nc_time):
        # print(time)
        # date = start_date + datetime.timedelta(days=int(time))
        # header.append(date.strftime("%j"))
        # x=getdate(time)
        header.append(str(time_idx+1))
    writer.writerow(header)

    # now=df[["lon", "lat"]]
    # print(now)
    # now=df.iloc[1:]
    for index, row in df.iterrows():
        # print( latlon)
        # print('!')
        df_lat=row['lat']
        df_lon=row['lon']
        df_lat_use=depose1(df_lat)
        df_lon_use=depose1(df_lon)
        input_data=[df_lat,df_lon]
        # for lat_idx, lat in enumerate(nc_lat):
        #     if df_lat_use!=lat:
        #         continue
        #     for lon_idx, lon in enumerate(nc_lon):
        #         if df_lon_use!=lon:
        #             continue
        latitude_index = np.abs(nc_lat - df_lat_use).argmin()
        longitude_index = np.abs(nc_lon - df_lon_use).argmin()
        for time_idx, time in enumerate(nc_time):
            input_data.append(value_values[time_idx,latitude_index,longitude_index])
        writer.writerow(input_data)