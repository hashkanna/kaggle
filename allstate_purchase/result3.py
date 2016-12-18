# Get the last occurring values for each ID
from collections import defaultdict
from collections import OrderedDict

result_dict = defaultdict(str)
prev_key = ''
prev_result = ''
with open('test_v2.csv', 'r') as f:
	for line in f:
		features = line.rstrip('\n').split(',')
		curr_key = features[0]
		curr_result = ''.join(features[17:24])
		if prev_key != '' and curr_key != prev_key:
			print prev_key + ',' + prev_result
		prev_key = curr_key
		prev_result = curr_result

# handle last line
print prev_key + ',' + prev_result