import pandas as pd
import numpy as np
from math import isnan
from sklearn import feature_extraction
import csv
# Set ipython's max row display
pd.set_option('display.max_row', 10)

# Set iPython's max column width to 50
pd.set_option('display.max_columns', 50)

train = pd.read_csv("fineline_features_raw_train.csv")
test = pd.read_csv("fineline_features_raw_test.csv")

fineline_uniq_train = pd.unique(train.FinelineNumber.ravel())
fineline_uniq_test = pd.unique(test.FinelineNumber.ravel())
fineline_uniq = set(fineline_uniq_train) | set(fineline_uniq_test)
fineline_uniq = [int(x) for x in fineline_uniq if x==x] # x==x to remove nan

fineline_dict = {j:i for i,j in enumerate(fineline_uniq)}
day_dict = {}
day_dict["Sunday"] = ','.join([str(x) for x in [0,0,0,0,0,0]])
day_dict["Monday"] = ','.join([str(x) for x in [1,0,0,0,0,0]])
day_dict["Tuesday"] = ','.join([str(x) for x in [0,1,0,0,0,0]])
day_dict["Wednesday"] = ','.join([str(x) for x in [0,0,1,0,0,0]])
day_dict["Thursday"] = ','.join([str(x) for x in [0,0,0,1,0,0]])
day_dict["Friday"] = ','.join([str(x) for x in [0,0,0,0,1,0]])
day_dict["Saturday"] = ','.join([str(x) for x in [0,0,0,0,0,1]])

#'''
with open("fineline_features_raw_train.csv") as f, open("keras_fineline_train.csv", "w") as g:
#with open("a.csv") as f, open("t.csv", "w") as g:
    f.readline()
    data = f.readlines()
    result_str = "VisitNumber," + ','.join([str(x) for x in fineline_uniq]) + ',TripType\n'
    old_visitnum = 0
    result = [0]*len(fineline_uniq)
    for line in data:
        VisitNumber, FinelineNumber, ScanCount, TripType = line.strip('\n').split(',')
        if old_visitnum != int(VisitNumber):
            g.write(result_str)
            result = [0]*len(fineline_uniq)
            old_visitnum = int(VisitNumber)
        if FinelineNumber != 'NULL':
            result[fineline_dict[int(FinelineNumber)]] += int(ScanCount)
        result_str = VisitNumber + ',' + ','.join([str(x) for x in result]) + ',' + TripType + '\n'
    g.write(VisitNumber + ',' + ','.join([str(x) for x in result]) + ',' + TripType + '\n')
#'''

with open("fineline_features_raw_test.csv") as f, open("keras_fineline_test.csv", "w") as g:
#with open("a.csv") as f, open("t.csv", "w") as g:
    f.readline()
    data = f.readlines()
    result_str = "VisitNumber," + ','.join([str(x) for x in fineline_uniq]) + '\n'
    old_visitnum = 0
    result = [0]*(len(fineline_uniq) - 1)
    for line in data:
        VisitNumber, FinelineNumber, ScanCount = line.strip('\n').split(',')
        if old_visitnum != int(VisitNumber):
            g.write(result_str)
            result = [0]*(len(fineline_uniq) - 1)
            old_visitnum = int(VisitNumber)
        if FinelineNumber != 'NULL':
            result[fineline_dict[int(FinelineNumber)]] += int(ScanCount)
        result_str = VisitNumber + ',' + ','.join([str(x) for x in result]) + ',' + '\n'
    g.write(VisitNumber + ',' + ','.join([str(x) for x in result]) + ',' + '\n')
