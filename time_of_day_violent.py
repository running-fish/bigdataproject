'''
Same as time_of_day_rates.py but for violent crimes.
'''

from __future__ import print_function
import sys
from pyspark import SparkContext
from csv import reader
from datetime import datetime

if __name__ == "__main__":
    sc = SparkContext()

    lines = sc.textFile(sys.argv[1], 1)
    def hour_of_crime(time):
        try:
            crime_time = datetime.strptime(time,'%H:%M:%S').hour
            return crime_time
        except:
            return ''

    lines = lines.mapPartitions(lambda x: reader(x))\
    .filter(lambda x: ('HOMICIDE' in x[7] or 'MURDER' in x[7] or 'ASSAULT' in x[7] or 'RAPE' in x[7] or 'ROBBERY' in x[7]))\
    .map(lambda x: (hour_of_crime(x[2]), 1))\
    .reduceByKey(lambda x,y: x+y)\
    .sortByKey(ascending=True)

    lines.saveAsTextFile("time_of_crime_violent.out")

    sc.stop()

