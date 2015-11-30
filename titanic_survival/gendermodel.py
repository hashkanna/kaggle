""" This simple code is desinged to teach a basic user to read in the files in python, simply find what proportion of males and females survived and make a predictive model based on this
Author : AstroDave
Date : 18th September, 2012

"""


import csv as csv
import numpy as np

csv_file_object = csv.reader(open('train.csv', 'rb')) #Load in the csv file
header = csv_file_object.next() #Skip the fist line as it is a header
data=[] #Creat a variable called 'data'
for row in csv_file_object: #Skip through each row in the csv file
    data.append(row[1:]) #adding each row to the data variable
data = np.array(data) #Then convert from a list to an array

#Now I have an array of 11 columns and 891 rows
#I can access any element I want so the entire first column would
#be data[0::,0].astype(np.flaot) This means all of the columen and column 0
#I have to add the astype command
#as when reading in it thought it was  a string so needed to convert

number_passengers = np.size(data[0::,0].astype(np.float))
number_survived = np.sum(data[0::,0].astype(np.float))
proportion_survivors = number_passengers / number_survived

# I can now find the stats of all the women on board
women_only_stats = data[0::,3] == "female" #This finds where all the women are
men_only_stats = data[0::,3] != "female" #This finds where all the men are
                                         # != means not equal

#I can now find for example the ages of all the women by just placing
#women_only_stats in the '0::' part of the array index. You can test it by
#placing it in the 4 column and it should all read 'female'

women_onboard = data[women_only_stats,0].astype(np.float)
men_onboard = data[men_only_stats,0].astype(np.float)

proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

print 'Proportion of women who survived is %s' % proportion_women_survived
print 'Proportion of men who survived is %s' % proportion_men_survived

#Now I have my indicator I can read in the test file and write out
#if a women then survived(1) if a man then did not survived (0)
#1st Read in test
test_file_object = csv.reader(open('test.csv', 'rb'))
header = test_file_object.next()

#Now also open the a new file so we can write to it call it something
#descriptive

predictions_file = csv.writer(open("gendermodel.csv", "wb"))
predictions_file.writerow(["PassengerId", "Survived"])

for row in test_file_object:
    if row[3] == 'female':
        predictions_file.writerow([row[0], "1"])
    else:
        predictions_file.writerow([row[0], "0"])