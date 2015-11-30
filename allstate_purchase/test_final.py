# Get the last occurring line for each ID

prev_key = ''
prev_result = ''
with open('test_v2.csv', 'r') as f:
	for line in f:
		features = line.rstrip('\n').split(',')
		curr_key = features[0]
		curr_result = line.rstrip('\n')
		if prev_key != '' and curr_key != prev_key:
			print prev_result
		prev_key = curr_key
		prev_result = curr_result

# handle last line
print prev_result