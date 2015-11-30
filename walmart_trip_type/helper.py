matches = {"3": 1, "4":2, "5":3, "6":4, "7":5, "8":6, "9":7, "12":8, "14":9, "15":10, "18": 11, "19":12, "20": 13}
for i in range(21, 45):
    matches[str(i)] = i-7
matches['999'] = 38
matches["TripType"] = "TripType"
#print matches
with open("result3_h2o_rf.csv.prep") as f:
    data = f.readlines()
    print '"VisitNumber","TripType_3","TripType_4","TripType_5","TripType_6","TripType_7","TripType_8","TripType_9","TripType_12","TripType_14","TripType_15","TripType_18","TripType_19","TripType_20","TripType_21","TripType_22","TripType_23","TripType_24","TripType_25","TripType_26","TripType_27","TripType_28","TripType_29","TripType_30","TripType_31","TripType_32","TripType_33","TripType_34","TripType_35","TripType_36","TripType_37","TripType_38","TripType_39","TripType_40","TripType_41","TripType_42","TripType_43","TripType_44","TripType_999"'
    for line in data:
        result = [0]*38
        trip_type = line.strip('\n').split(',')[1].strip('"')
        visit_number = line.strip('\n').split(',')[0].strip('"')
        #print visit_number
        if trip_type != 'TripType':
            #print trip_type, matches[trip_type]
            ind = matches[trip_type]-1
            result[ind] = 1
            print visit_number + ',' + ','.join(str(v) for v in result)
