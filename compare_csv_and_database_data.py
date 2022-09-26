import os
import sys
import re
import psycopg2.extras

from config import user_db, passwd_db


os.chdir(r'L:\worktemp\James\check_reading')


params = {
    'host': 'revpgdb01.revintel.net',
    'database': 'tpliq_tracker_db',
    'user': user_db,
    'password': passwd_db}
con = psycopg2.connect(**params)


dicy = {}
dicy1 = {}
c = 0

with open(r'DetailIndex_20210205.csv', 'r') as fr:
    next(fr)
    for line in fr:
        tmp = line.strip().split(',')
        if (tmp[0] != '' and tmp[0] != '0.00') and 'NOCHECK' not in tmp[3]:
            name = '{} {}'.format(tmp[7], tmp[6])
            # print(name)

            sql = """\
select concat(split_part(patient_name, ' ', 2), ' ', split_part(patient_name, ' ', 1)), pat_acct, \
charges::text from tpl_billing_records where patient_name ~* '{}';""".format(name)
            # print(sql)

            cur = con.cursor()
            cur.execute(sql)
            key = '{} {}'.format(tmp[7], tmp[6])
            accts = [key + '|' + row[1] for row in cur]
            # print(accts)
            for i in accts:
                dicy[i] = 1    #dict of patname-acct from db

            if 'V' in tmp[5]:
                raw = re.search(r'\d*?(?=V)', tmp[5]).group()
            else:
                raw = tmp[5]
            dicy1[key + '|' + raw] = '|{}|{}'.format(''.join(tmp[8].replace('-', '').split()), ''.join(tmp[9].split()))    #dict of patname-acct: claim-policy from csv

            # c += 1
            # if c == 5:
            #     break
# print(dicy)
# print(dicy1)
print('patient_name|pact_acct|claim_num|policy_number')

for k in dicy1:
    if k not in dicy:
        print(k + dicy1[k])

