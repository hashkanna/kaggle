class AutoVivification(dict):
	"""Implementation of perl's autovivification feature."""
	def __getitem__(self, item):
		try:
			return dict.__getitem__(self, item)
		except KeyError:
			value = self[item] = type(self)()
			return value

sales_dict = AutoVivification()
with open('walmart_test_full.csv', 'r') as f:
	f.next()
	for line in f:
		terms = line.strip().split(',')
		(store, dept, week_date) = terms[:3]
		sales_dict[store][dept][week_date] = {}

all_test_dates = sorted(sales_dict['1']['1'].keys())
#print all_test_dates

for i in range(1,46):
	for j in range(1,100):
		for k in all_test_dates:
			#if sales_dict[str(i)][str(j)][str(k)] == {}:
			#	sales_dict[str(i)][str(j)][str(k)] = 0
			#print '%s,%s,%s,%s' % (i, j, k, sales_dict[str(i)][str(j)][str(k)])
			print '%s_%s_%s' % (i, j, k)