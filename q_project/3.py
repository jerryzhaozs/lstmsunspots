# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 15:57:21 2023

@author: Administrator
"""

import tushare as ts

ts.set_token('c139c984c30f6866e073c740b379696dc86d5ad00b12f662d91776e8')
pro = ts.pro_api()
df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20230415')