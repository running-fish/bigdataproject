from __future__ import print_function
import sys
from pyspark import SparkContext
from csv import reader

if __name__ == "__main__":
    sc = SparkContext()

    lines = sc.textFile(sys.argv[1], 1)
    first_line = lines.first()

    if first_line.split(',')[0] == u'CMPLNT_NUM':
        # First line is header
        # Filter header out
        lines = lines.filter(lambda x: x != first_line)

    def valid_boro(string):
        if string.upper() in ('QUEENS', 'STATEN ISLAND', 'BRONX', 'BROOKLYN', 'MANHATTAN'):
            return 'VALID'
        elif not string.replace(' ', ''):
            return 'NULL'
        else:
            return 'INVALID'

    lines = lines.mapPartitions(lambda x: reader(x))\
    .map(lambda x: '%s\tTEXT\tnyc borough\t%s' % (x[13], valid_boro(x[13])))

    lines.saveAsTextFile("col13.out")

    sc.stop()
