import numpy as np
import pandas as pd


range_dict = {
    (0,50): {'pm25': [0,12],
             'pm10': [0,54],
             'O3': [0,54]},
    (51,100): {'pm25': [12.1,35.4],
               'pm10': [55,154],
               'O3': [55,70]},
    (101,150): {'pm25': [35.5,55.4],
                'pm10': [155,254],
                'O3': [71,85]},
    (151,200): {'pm25': [55.5,150.4],
                'pm10': [255,354],
                'O3': [86,105]},
    (201,300): {'pm25': [150.5,250.4],
                'pm10': [355,424],
                'O3': [106,200]},
    (301,99999): {'pm25': [250.5,99999],
                  'pm10': [425,99999],
                  'O3': [201,99999]}
}


pm25_arr = pd.read_csv('data/PM2.5 data.csv').to_numpy()[:,2]
pm10_arr = pd.read_csv('data/PM10 data.csv').to_numpy()[:,2]
o3_arr = pd.read_csv('data/O3 data.csv').to_numpy()[:,2]

pm25_avg = round(sum(pm25_arr) / len(pm25_arr), 1)
pm10_avg = round(sum(pm10_arr) / len(pm10_arr))
o3_avg = round(sum(o3_arr) / len(o3_arr))

for key in range_dict.keys():
    aqi_l, aqi_h = key[0], key[1]
    c_dict = range_dict[key]

    if c_dict['pm25'][0] <= pm25_avg <= c_dict['pm25'][1]:
        pm25_aqi = (aqi_h-aqi_l) / (c_dict['pm25'][1]-c_dict['pm25'][0]) * (pm25_avg - c_dict['pm25'][0]) + aqi_l

    if c_dict['pm10'][0] <= pm10_avg <= c_dict['pm10'][1]:
        pm10_aqi = (aqi_h-aqi_l) / (c_dict['pm10'][1]-c_dict['pm10'][0]) * (pm10_avg - c_dict['pm10'][0]) + aqi_l

    if c_dict['O3'][0] <= o3_avg <= c_dict['O3'][1]:
        o3_aqi = (aqi_h-aqi_l) / (c_dict['O3'][1]-c_dict['O3'][0]) * (o3_avg - c_dict['O3'][0]) + aqi_l


aqi = sum([pm25_aqi, pm10_aqi, o3_aqi])/3
print(aqi)
