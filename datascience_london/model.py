import sys
from sklearn.ensemble import RandomForestClassifier
import csv as csv
import numpy as np

#Open up the csv file in to a Python object
train = csv.reader(open('train.csv', 'rb'))
test = csv.reader(open('test.csv', 'rb'))

