import pandas as pd

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")
'''
train_df = train_df[['VisitNumber', 'Weekday', 'DepartmentDescription', 'TripType']]
grouped_concat = train_df.groupby(['VisitNumber', 'Weekday', 'TripType']).apply(lambda x: ','.join(str(v) for v in x.DepartmentDescription))
grouped_concat.to_csv('train_groupby_day_description.csv', sep=',')
'''

train_df = train_df[['Weekday', 'TripType']]
grouped_concat = train_df.groupby(['Weekday']).apply(lambda x: max(set(x.TripType), key=x.TripType.count))
#header = ['VisitNumber', 'Weekday', 'TripType']
grouped_concat.to_csv('train_groupby_day.csv', sep=',', header=True)

'''
test_df = test_df[['VisitNumber', 'Weekday']]
grouped_concat = test_df.groupby(['VisitNumber', 'Weekday']).apply(lambda x: " ")
test_final_df = grouped_concat[['VisitNumber']]
test_final_df.to_csv('test_groupby_day.csv', sep=',', header=True)
'''
