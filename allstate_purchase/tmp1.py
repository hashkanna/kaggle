with open('result6.csv.bak') as r, open('result3.csv') as f:
	for line1, line2 in zip(r,f) :
		#print line1.strip() + '|' + line2.strip()
		result1 = line1.strip()
		result2 = line2.strip()
		#print result2[:11]
		result = result1[:11] + str(result2[11]) + result1[12:]
		print result