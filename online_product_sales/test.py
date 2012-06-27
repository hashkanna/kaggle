#! /usr/bin/env python

import sys

sum = 0
count = 0
for line in sys.stdin:
  words = line.strip('\n').split(',')
  try:
    sum += int(words[0])
    count += 1
  except:
    pass
print sum*1.0/count
