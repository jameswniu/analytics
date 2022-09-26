#! /usr/bin/python3
import sys
import re
import json

from collections import defaultdict


custname = {    ## SPECIFY
    "321": "ApolloMD Athena",
    "405": "ApolloMD Athena",
    "67": "ApolloMD IDX",
    "484": "AULTMAN HOSPITAL",
    "497": "Logix Health",
    "530": "Western Medical Associates",
    "565": "EMA",
    "564": "VEP",
    "538": "Team Health",
    "171": "Texas Health Resources",
    "483": "Texas Health Resources",
    "366": "Beaumont Health",
    "18": "Adventist System",
    "227": "Johns Hopkins",
    "646": "AULTMAN PROFESSIONAL",
    "678": "Western Medical Associates",
    "631": "Alteon Health",
    "710": "TeamHealth Work Comp",
    "734": "Team Health AutoPR"
}
factype = {
    "11": "Provider's Office",
    "12": "Patient's Home",
    "13": "Assisted Living Facility",
    "17": "Walk-in Retail Health Clinic",
    "18": "Place of Employment - Worksite",
    "20": "Urgent Care Facility",
    "21": "Inpatient Hospital",
    "22": "Outpatient Hospital",
    "23": "Emergency Room - Hospital",
    "24": "Ambulatory Surgical Center",
    "25": "Birthing Center",
    "26": "Military Treatment Facility",
    "31": "Skilled Nursing Facility",
    "32": "Nursing Facility",
    "33": "Custodial Care Facility",
    "34": "Hospice"
}
cnt = defaultdict(int)

#----
# check only specified fields in json while also showing customer
#----
for line in sys.stdin :
    if not re.match(r'\s{0,6}{', line):
       continue

    dicy = json.loads(line)
    
    cnt[dicy['vx_claim_type'], dicy['vx_carrier_lob']] += 1

    #cnt[dicy['vx_pm_sk'], type(dicy['vx_pm_sk'])] += 1
    #cnt[dicy['vx_src_sk'], type(dicy['vx_src_sk'])] += 1

    #cnt[dicy['vx_accident_state']] += 1
    #cnt[dicy['accident_state']] += 1

    #cnt[dicy['total_charges']] += 1

    #for k in dicy:
    #    if 'LX' in k and 'modifier' in k:
    #        cnt[f"{dicy['vx_pm_sk']} {k} {dicy[k]}"] += 1         

    #cnt[f"{dicy['cust_id']} {custname[dicy['cust_id']]}, {dicy['vx_carrier_name']}"] += 1
    #cnt[f"{dicy['cust_id']} {custname[dicy['cust_id']]}: {dicy['claim_type']}"] += 1 

    #try:
    #    cnt[f"{dicy['admission_date']}-{dicy['discharge_date']} | {dicy['LX01_service_date']}"] += 1 
    #except:
    #    print(f"{dicy['pat_acct']}")

    #cnt[f"{dicy['facility_code']} {factype[dicy['facility_code']]}"] += 1

    #try:
    #    cnt[f"""{dicy['vx_pm_sk']} | "diagnoses": "{dicy['diagnoses']}" | "dx_code_desc": "{dicy['dx_code_desc'][:40]}..." """] += 1
    #except:
    #    cnt[f"{dicy['vx_pm_sk']} : no dx_code_desc"] += 1

    #try:
    #    if dicy['diagnoses'] == '':
    #        raise ValueError

    #    cnt[dicy['diagnoses'][:30]] += 1
    #except:
    #    cnt[f"{dicy['vx_pm_sk']} : empty diagnoses"] += 1

    #cnt['{}-{}'.format(dicy['vx_cust_id'], dicy['vx_carrier_name'])] += 1

    #cnt[dicy['diagnoses']] += 1
    #cnt[dicy['LX01_dx_code_pointer']] += 1
    #cnt[dicy['vx_carrier_address_1']] += 1
  
    #cnt[f"{dicy['vx_carrier_name']}|{dicy['vx_carrier_lob']}|{dicy['edi_payer_id']}"] += 1
    #cnt[dicy['vx_carrier_lob']] += 1
    #cnt[dicy['vx_carrier_name']] += 1

    #if dicy['vx_carrier_lob'] == 'AUTO (COMMERCIAL)':
        #cnt[dicy['vx_carrier_insured_last_name']] += 1    

    #cnt[f"{dicy['cust_id']}, {dicy['pat_acct']}"] += 1    
 
    #try:
    #    cnt[dicy['vx_pm_sk']] += 1 
    #except:
    #    cnt[dicy['pat_acct']] += 1
    #    cnt[dicy['cust_id']] += 1 
    #    cnt[dicy['claim_type']] += 1

    #cnt[dicy['holding_flag']] += 1
    #cnt[dicy['reject_flag']] += 1

    #if dicy['cust_id'] in ('538', '734'):
    #    cnt[dicy['cust_id']] += 1
    #    cnt[dicy['pay_to_addr1']] += 1 
    #    cnt[dicy['pay_to_city']] += 1
    #    cnt[dicy['pay_to_state']] += 1
    #    cnt[dicy['pay_to_zip']] += 1

    #try:
    #    cnt[f"{dicy['vx_pm_sk']} | {dicy['vx_carrier_insured_zip']}"] += 1 
    #except:
    #    cnt[f"{dicy['vx_pm_sk']} | "] += 1 

    #try:
    #    cnt[f"{dicy['vx_pm_sk']} | {dicy['facility_zip']}"] += 1 
    #except:
    #    cnt[f"{dicy['vx_pm_sk']} | "] += 1 

    #cnt['{}: {}|{}'.format(dicy['vx_carrier_lob'], dicy['vx_carrier_insured_first_name'], dicy['vx_carrier_insured_last_name'])] += 1
    #cnt['{} {}'.format(dicy['patient_firstname'], dicy['patient_lastname'])] += 1
   
    #for suffix in ('charge', 'procedure_code', 'service_date'): 
    #    for k in dicy:
    #         if re.match(rf'\bLX\d+_{suffix}\b', k):
    #            cnt[f'{k}: {dicy[k]}'] += 1
    
    #try:
    #    cnt[f"{dicy['cust_id']} | {dicy['roswell_mailbox']}"] += 1 
    #except:
    #    cnt[f"{dicy['cust_id']} | "] += 1 

    #try:
    #    svc = dicy['LX01_service_date']

    #    try: 
    #        cnt[f"{dicy['vx_pm_sk']}--{dicy['pat_acct']}: accident_date {dicy['accident_date']} | vx_date_of_loss {dicy['vx_date_of_loss']} [<?] {dicy['LX01_service_date']} LX01_service_date"] += 1
    #    except: 
    #        cnt[f"{dicy['vx_pm_sk']}--{dicy['pat_acct']}: accident_date '' | vx_date_of_loss {dicy['vx_date_of_loss']} [<?] {dicy['LX01_service_date']} LX01_service_date | '' accident_date"] += 1
    #except:
    #    svc = dicy['LX001_service_date']

    #    try: 
    #        cnt[f"{dicy['vx_pm_sk']}--{dicy['pat_acct']}: accident_date {dicy['accident_date']} | vx_date_of_loss {dicy['vx_date_of_loss']} [<?] {dicy['LX001_service_date']} LX001_service_date"] += 1
    #    except: 
    #        cnt[f"{dicy['vx_pm_sk']}--{dicy['pat_acct']}: accident_date '' | vx_date_of_loss {dicy['vx_date_of_loss']} [<?] {dicy['LX001_service_date']} LX001_service_date | '' accident_date"] += 1

    #cnt[dicy['vx_carrier_claim_number']] += 1

    #cnt[dicy['attending_physician_npi']] += 1


prev = ''
for k, v in cnt.items():
    #if k != prev:
    #    print()

    print(f"{k}: {v}")   

    #prev = k
    #print(prev)
print(len(cnt))

