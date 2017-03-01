"""
Loads traffic data from a CSV file, creates linear regression
models and saves them to a JSON file

@author Trevor Blanarik
"""

import numpy as np
import pandas as pd
import datetime
from scipy.stats import linregress
import json

def create_and_save_all_regressions(input_csv, output_json):
    #f = open(r"C:\Users\tblan\Desktop\all_regressions\Renton_to_Downtown_Seattle.csv")
    data = open(input_csv).readlines()

    all_data = {'traveltime':[], 'date':[]}

    # Skip the header
    for row in data[1:]:
        sep_row = row.strip().split(",")
        all_data['traveltime'].append(int(sep_row[1]))
        a_date = datetime.datetime.strptime(sep_row[5], "%Y%m%d_%H%M")
        dto5 = abs(a_date.minute - 5)
        dto25 = abs(a_date.minute - 25)
        dto45 = abs(a_date.minute - 45)
        # Rectify the minutes to be 5, 25, or 45
        if dto5 < dto25 and dto5 < dto45:
            a_date = a_date.replace(minute=5)
        if dto25 < dto5 and dto25 < dto45:
            a_date = a_date.replace(minute=25)
        if dto45 < dto5 and dto45 < dto25:
            a_date = a_date.replace(minute=45)        
        
        all_data['date'].append(a_date)
        
    l2d = pd.DataFrame(all_data).set_index('date')

    all_hours = [l2d.index.hour == i for i in range(24)]
    days = [l2d.index.weekday == i for i in range(5)]
    weekday = l2d.index.weekday < 5
    weekend = l2d.index.weekday >= 5
    day_type = [weekday, weekend]

    minute05 = l2d.index.minute == 5
    minute25 = l2d.index.minute == 25
    minute45 = l2d.index.minute == 45

    minute_type = [minute05, minute25, minute45]

    # Enumerate all of the time combinations we care about
    time_combos = []
    for ix in range(24):
        for minute in [5,25, 45]:
            time_combos.append((ix, minute))
            
    # Create linear regression models for every pairing of time and time+20 mins        
    all_regressions = {}        
    for i,day_i in enumerate(day_type):
        all_regressions[i] = {}
        for tc1,tc2 in zip(time_combos, time_combos[1:] + time_combos[:1]):
            data1 = l2d[(l2d.index.hour == tc1[0]) & (l2d.index.minute == tc1[1]) & day_i]
            data2 = l2d[(l2d.index.hour == tc2[0]) & (l2d.index.minute == tc2[1]) & day_i]
            npts = min(len(data1['traveltime'].values), len(data2['traveltime'].values)) 
            linreg = linregress(data1['traveltime'].values[:npts], data2['traveltime'].values[:npts])
            if tc1[0] not in all_regressions[i]:
                all_regressions[i][tc1[0]] = {}
            all_regressions[i][tc1[0]][tc1[1]] = {"r-value": linreg.rvalue, 
                                             "slope": linreg.slope,
                                             "intercept": linreg.intercept}

    # Save the models in a json file                                         
    json.dump(all_regressions, open(output_json, 'w'))
    