#! /usr/bin/env python3 
import sys, os
import re
import json

from glob import glob
from datetime import datetime, timedelta

from pytz import timezone


Ymd = datetime.now(tz=timezone('America/New_York')).strftime('%Y%m%d')
md = Ymd[4:]


os.chdir(r'/home/james.niu@revintel.net/production/jsondump/archives/billing')


dicy = {}
suffix = ('edi', 'fax')

Y = Ymd[:4]

cedi = 0
cfax = 0

dayspast = 7    # SPECIFY
c, d = 0, 0
numformat = ':,.0f'

for method in suffix:
    for f in glob(f'*_*_{method}.json'):
        Ymdf = re.search(r'\d{8}', f).group()

        # only want files since previous week
        if (datetime.strptime(Ymd, '%Y%m%d') - datetime.strptime(Ymdf, '%Y%m%d')).days <= dayspast:
            if 'edi' in f:
                if c == 0:
                    print('-' * 38)

                print(f)

                with open(f, 'r') as fr:
                    for line in fr:
                        cedi += 1
                c += 1 

            else:
                if d == 0 and c == 0:
                    print('-' * 38)

                print(f)

                with open(f, 'r') as fr:
                    for line in fr:
                        cfax += 1
                
                d += 1

    
    print('-' * 38)


print(f"""\
EDI bills past {{{numformat}}} days: {{{numformat}}}
Fax bills past {{{numformat}}} days: {{{numformat}}}
--------------------------------------
Total: {{{numformat}}}
Averge: {{{numformat}}}""".format(
    dayspast, cedi,
    dayspast, cfax,
    cedi + cfax,
    (cedi + cfax) / dayspast
))


