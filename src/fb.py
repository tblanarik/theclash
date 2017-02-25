"""
Loads the stored linear regressions, pulls the latest travel time,
saves the prediction as times.json

@author Trevor Blanarik
"""

import json
import datetime
import copy

def predict_time(name, data_file, regress_file):
    """
    Loads the stored linear regressions, pulls the latest travel time,
    saves the prediction as times.json
    """
    csv_file = data_file
    last_line = open(csv_file).readlines()[-1]
    last_data = last_line.strip().split(',')
    curtime = int(last_data[1])
    mdt = datetime.datetime.strptime(last_data[-1], "%Y%m%d_%H%M")
    is_weekday = 0 if mdt.isoweekday() < 5 else 1

    regressions_1_hour = json.load(open(regress_file))

    linreg = regressions_1_hour[str(is_weekday)][str(mdt.hour)][str(mdt.minute)]

    predict = linreg['slope']*curtime + linreg['intercept']

    rsq = linreg['r-value']*linreg['r-value']

    prev_data = json.load(open(r'/home/tblanarik/mysite/data/times.json'))

    new_data = copy.copy(prev_data)

    new_data["%sCurrent" % name] = curtime
    new_data["%sPrediction" % name] = int(predict)
    new_data["%sPreviousPrediction" % name] = int(prev_data["%sPrediction" % name]),
    new_data["%sLastUpdated" % name] = mdt.strftime("%H:%M")
    new_data["%sRSquared" % name] = int(rsq*100.0)

    history_file = open(r'/home/tblanarik/mysite/data/%s.csv' % name, 'a')
    history_file.write("%s,%s,%s\n" % (mdt.strftime("%H:%M"),
                                       int(curtime),
                                       int(prev_data["%sPrediction" % name])))
    history_file.close()

    outfile = open(r'/home/tblanarik/mysite/data/times.json', 'w')
    json.dump(new_data, outfile)
    outfile.close()

predict_time("LynnwoodToSeattle",
             r'/home/tblanarik/wsdot/data/Lynnwood_to_Downtown_Seattle.csv',
             r'/home/tblanarik/wsdot3/regressions_lynnwood_to_seattle.json')

predict_time("SeattleToBellevue520",
             r'/home/tblanarik/wsdot/data/Downtown_Seattle_to_Downtown_Bellevue_via_SR_520.csv',
             r'/home/tblanarik/wsdot3/regressions_seattle_to_bellevue520.json')

predict_time("SeattleToLynnwood",
             r'/home/tblanarik/wsdot/data/Downtown_Seattle_to_Lynnwood.csv',
             r'/home/tblanarik/wsdot3/regressions_seattle_to_lynnwood.json')

predict_time("RentonToSeattle",
             r'/home/tblanarik/wsdot/data/Renton_to_Downtown_Seattle.csv',
             r'/home/tblanarik/wsdot3/regressions_renton_to_seattle.json')
