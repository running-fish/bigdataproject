from __future__ import print_function
import sys
from pyspark import SparkContext
from csv import reader
from datetime import datetime

def valid_check(time, date, starttime, startdate):
    try:
        datetime.strptime(time,'%H:%M:%S')
        try:
            # Check that the start time is before the end time
            start = datetime.strptime(startdate + '-' + starttime,'%m/%d/%Y-%H:%M:%S')
            end = datetime.strptime(date + '-' + time,'%m/%d/%Y-%H:%M:%S')
            if end >= start:
                return 'VALID'
            else:
                return 'INVALID'
        except:
            # If cannot compare start and end, asume valid
            return 'VALID'
        return 'VALID'
    except:
        if time == '':
            return 'NULL'
        else:
            return 'INVALID'

if __name__ == "__main__":
    sc = SparkContext()

    lines = sc.textFile(sys.argv[1], 1)
    first_line = lines.first()

    if first_line.split(',')[0] == u'CMPLNT_NUM':
        # First line is header
        # Filter header out
        lines = lines.filter(lambda x: x != first_line)


    lines = lines.mapPartitions(lambda x: reader(x))\
    .map(lambda x: ('%s\tTIME\tEnding time of occurrence for the reported event\t%s' % (x[4], valid_check(x[4], x[3], x[2], x[1]))))\

    lines.saveAsTextFile("col4.out")

    sc.stop()
