#!/usr/bin/env sh
# This transforms the 13 answers to the WORKING column
# into integers 0-12, 5 answers to MUSIC into 0-4,
# normailizes LIST_OWN, and LIST_BACK into integer values
# and drops rows with variations of "16+ hours"
# (loses 2.623031698% of the data)
# Replaces Male with 0 and Female with 1
# Replaces Region with Integer Values
INFILE=$1
sed -e "
  s/\"Employed 30+ hours a week\"/0/g;
  s/\"Employed 8-29 hours per week\"/1/g;
  s/\"Employed part-time less than 8 hours per week\"/2/g;
  s/\"Full-time housewife \/ househusband\"/3/g;
  s/\"Full-time student\"/4/g;
  s/\"In unpaid employment (e.g. voluntary work)\"/5/g;
  s/\"Other\"/6/g;
  s/\"Part-time student\"/7/g;
  s/\"Prefer not to state\"/8/g;
  s/\"Retired from full-time employment (30+ hours per week)\"/9/g;
  s/\"Retired from self-employment\"/10/g;
  s/\"Self-employed\"/11/g;
  s/\"Temporarily unemployed\"/12/g;

  s/\"Music has no particular interest for me\"/0/g;
  s/\"Music is no longer as important as it used to be to me\"/1/g;
  s/\"I like music but it does not feature heavily in my life\"/2/g;
  s/\"Music is important to me but not necessarily more important than other hobbies or interests\"/3/g;
  s/\"Music is important to me but not necessarily more important\"/3/g;
  s/\"Music means a lot to me and is a passion of mine\"/4/g;

  s/\"\([0-9]*\) [a-zA-Z]*\"/\1/g;
  s/\"Less than an hour\"/0/g
  
  s/\"Male\"/0/g;
  s/\"Female\"/1/g;
  
  s/\"Centre\"/0/g;
  s/\"Midlands\"/1/g;
	s/\"North Ireland\"/2/g
	s/\"North\"/3/g
	s/\"Northern Ireland\"/4/g
	s/\"South\"/5/g

  " $INFILE | grep -Ev '"More than 16 hours"|"16\+ hours"'
