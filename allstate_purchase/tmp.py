# calculate most occurring values for each of A, B, C, D, E, F, G

from collections import defaultdict
from collections import Counter

result_dict = defaultdict(list)
with open('tmp.csv', 'r') as f:
	for line in f:
		val = line.rstrip('\n').split(',')[1]
		for i,c in enumerate(val):
			result_dict[i].append(c)

for i in result_dict:
	print i, Counter(result_dict[i])
