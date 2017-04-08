from __future__ import print_function
import sys
from pyspark import SparkContext
from csv import reader
from numpy import np

if __name__ == "__main__":
    sc = SparkContext()

    lines = sc.textFile(sys.argv[1], 1)

    def valid_string(string):
        chars = set('qwertyuiopasdfghjklzxcvbnm')
        try:
            if any((c in chars) for c in string.lower()):
                return 'VALID'
            else:
                return 'INVALID'
        except:
            if string.replace(' ', '') == '' or np.isnan(string):
                return 'NULL'
            else:
                return 'INVALID'

    lines = lines.mapPartitions(lambda x: reader(x))\
    .map(lambda x: '%s TEXT park of occurrence if applicable %s' % (x[17], valid_string(x[17])))

    lines.saveAsTextFile("col17.out")

    sc.stop()
