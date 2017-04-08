from __future__ import print_function
import sys
from pyspark import SparkContext
import csv, StringIO
from datetime import datetime
from datetime import timedelta

def fix_date(date):
    try:
        right_date = datetime.strptime(date,'%m/%d/%Y') + timedelta(days=1)
        return datetime.strftime(right_date,'%m/%d/%Y')
    except:
        return ''

def fix_y0xx_to_20xx(date):
    try:
        if date[7] == '0' and date[6] != '2':
            newdate = date[:6]+ '20' + date[8:]
            return newdate
        else:
            return date
    except:
        return ''

def check_and_fix(row):
    #Fixes '24:00:00' times 
    if row[2] == '24:00:00':
        row[2] = '00:00:00'
        row[1] = fix_date(row[1])
    if row[4] == '24:00:00':
        row[4] = '00:00:00'
        row[3] = fix_date(row[3])

    #Fixes years with y0xx where y != 2 to 20xx
    row[1] = fix_y0xx_to_20xx(row[1])
    row[3] = fix_y0xx_to_20xx(row[3])
    row[5] = fix_y0xx_to_20xx(row[5])

    #Combines categories in column 7
    lookup7 = col7.get(row[7], None)
    if lookup7 is not None:
        row[7] = lookup7

    #Fixes column 15
    row[15] = row[15].strip()

    return row

col7 = {'ADMINISTRATIVE CODES': 'ADMINISTRATIVE CODE',
        'INTOXICATED/IMPAIRED DRIVING': 'INTOXICATED & IMPAIRED DRIVING',
        'KIDNAPPING': 'KIDNAPPING & RELATED OFFENSES',
        'KIDNAPPING AND RELATED OFFENSES': 'KIDNAPPING & RELATED OFFENSES',
        'OTHER STATE LAWS (NON PENAL LA': 'OTHER STATE LAWS (NON PENAL LAW)'}

def list_to_csv_str(x):
    """Given a list of strings, returns a properly-csv-formatted string."""
    output = StringIO.StringIO("")
    csv.writer(output).writerow(x)
    return output.getvalue().strip() # remove extra newline

if __name__ == "__main__":
    sc = SparkContext()

    lines = sc.textFile(sys.argv[1], 1)
    first_line = lines.first()

    if first_line.split(',')[0] == u'CMPLNT_NUM':
        # First line is header
        # Filter header out
        lines = lines.filter(lambda x: x != first_line)

    lines = lines.mapPartitions(lambda x: csv.reader(x))\
   .map(lambda x: check_and_fix(x))\
   .map(list_to_csv_str)

    lines.saveAsTextFile("output.out")

    sc.stop()
