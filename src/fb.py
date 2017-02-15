"""
Loads the stored linear regressions, pulls the latest travel time,
saves the prediction as times.json

@author Trevor Blanarik
"""

import json
import datetime

def predict():
    """
    Loads the stored linear regressions, pulls the latest travel time,
    saves the prediction as times.json
    """
    lynncsv = r'/home/tblanarik/wsdot/data/Lynnwood_to_Downtown_Seattle.csv'
    last_line = open(lynncsv).readlines()[-1]
    last_data = last_line.strip().split(',')
    curtime = int(last_data[1])
    mdt = datetime.datetime.strptime(last_data[-1], "%Y%m%d_%H%M")
    is_weekday = 0 if mdt.isoweekday() < 5 else 1

    regressions_1_hour = json.load(open(r'/home/tblanarik/wsdot3/regressions_1_hour.json'))

    linreg = regressions_1_hour[str(is_weekday)][str(mdt.hour)][str(mdt.minute)]

    predict = linreg['slope']*curtime + linreg['intercept']

    prev_data = json.load(open(r'/home/tblanarik/mysite/data/times.json'))

    data = {"LynnwoodToSeattleCurrent": curtime,
            "LynnwoodToSeattlePrediction": int(predict),
            "LynnwoodToSeattlePreviousPrediction":int(prev_data["LynnwoodToSeattlePrediction"]),
            "LastUpdated": mdt.strftime("%H:%M")}

    outfile = open(r'/home/tblanarik/mysite/data/times.json', 'w')
    json.dump(data, outfile)
    outfile.close()

predict()
