#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, math
from datetime import datetime

level= {1:'7.1', 2:'7.0', 3:'6.9', 4:'6.7', 5:'6.4', \
        6:'6.2', 7:'6.0', 8:'5.7', 9:'5.5', 10:'5.3', \
        11:'5.1', 12:'4.9', 13:'4.8', 14:'4.6', 15:'4.4'}

def getUsedMonth(dealDate):
    try:
        now, past = datetime.now(), datetime.strptime(dealDate,"%Y%m%d")
        if now < past:
            raise ValueError
        return (now.year - past.year) * 12 + (now.month - past.month) + 1
    except:
        return 0

def getDepreciationLevel(usedMonth):
    a, b = 6.0, 1.7
    depreMonth = (a - b * (usedMonth / 12.)) / b * 12 * 0.25
    years = math.floor((usedMonth + depreMonth)/12. + 0.5)
    if not years in level or usedMonth <= 0:
        return ''
    return level[years]

for line in sys.stdin:
#for line in ['20140506','20130129','20160312','20171212']:
    # line is supposed to be "data_id\tdeal_date"
    # data_id is the key used to join
    line = line.strip().split('\t')
    mon = getUsedMonth(line[1])
    print '\t'.join([line[0], line[1], str(mon), getDepreciationLevel(mon)+'%'])
