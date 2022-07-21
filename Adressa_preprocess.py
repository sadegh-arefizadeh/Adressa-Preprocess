from os import listdir
from os.path import isfile, join
import pandas as pd
import json
import numpy as np

mypath = '../adressa'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
data_for_session_id = []
for i, value in enumerate(onlyfiles):
    # read all data in csv form
    data = pd.read_csv(mypath+value, sep="\n", header=0)
    # since the first row of data is included in column name, we manually add it to the constructed data
    data.loc[data.__len__()] = data.columns[0]
    data.rename(columns={data.columns[0]: 'Whole'}, inplace=True)
    # construct the data
    data_frame = pd.DataFrame([json.loads(d) for d in data['Whole']])
    # There are too many columns. Here we choose what columns we need.
    data_for_session_id.append(data_frame[
                                   ['id', 'url', 'author',
                                    'title', 'keywords', 'category1']])
# Concatenate data of all days into one
whole_data = pd.concat(data_for_session_id, ignore_index=True)

# To assign session i to each record, we use following procedures

# The data is quite large, so we delete unnecessary variables to use the memory more efficiently.
del data_for_session_id
whole_data_ordered = whole_data.sort_values(['userId', 'time'])
del whole_data

# correcting those without start (some ids record are without session start)
start_data = whole_data_ordered[['userId', 'sessionStart', 'eventId']].groupby(['userId']).nth(0)
events_without_start = start_data[start_data['sessionStart'] < 1]['eventId'].to_list()
whole_data_ordered.loc[whole_data_ordered['eventId'].isin(events_without_start), ['sessionStart']] = True
del start_data
del events_without_start

# correcting those without stop (some ids record are without stop)
stop_data = whole_data_ordered[['userId', 'sessionStop', 'eventId']].groupby(['userId']).nth(-1)
events_without_stop = stop_data[stop_data['sessionStop'] < 1]['eventId'].to_list()
whole_data_ordered.loc[whole_data_ordered['eventId'].isin(events_without_stop), ['sessionStop']] = True
del stop_data
del events_without_stop

# to creat session number
# whole_data_ordered contains session id which is ordered starting from 1
whole_data_ordered['tmp'] = 0 + whole_data_ordered['sessionStart']
whole_data_ordered = whole_data_ordered.assign(session_id=whole_data_ordered.tmp.cumsum())
# drop temporary columns
whole_data_ordered.drop(columns=['anomaly', 'cumsum', 'tmp'], inplace=True)