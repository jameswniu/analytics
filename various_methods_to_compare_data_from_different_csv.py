import os
import pandas as pd


os.chdir('L:\\Auto_Opportunity_Analysis\\Temp')

#----
# read txt into pandas dataframe
#----
df0 = pd.read_csv('10_20_thr_accts.txt', delimiter='\t')
df0.columns = ['pat_acct_new']
df0 = df0.drop_duplicates().reset_index(drop=True)
# print(df0.head(3));  print(df0.tail(2))

df1 = pd.read_csv('tpl_client_raw_bills_20201020_1615.csv')
df1 = df1.rename(columns={'pat_acct': 'pat_acct_exist'})
df1 = df1.drop_duplicates().reset_index(drop=True)
# print(df1.head(3));  print(df1.tail(2))

#----
# Method 1 pandas left join
#----
df2 = pd.merge(df0, df1, how='left', left_on='pat_acct_new', right_on='pat_acct_exist')
# print(df2.head(3));  print(df2.tail(2))
df3 = df2[df2.pat_acct_exist.isnull()].pat_acct_new.reset_index(drop=True)
print(df3.head(3));  print(df3.tail(2))

# convert pandas df into txt
df3.to_csv('compare_acct_res.txt', index=False, header=False)

#----
# Method 2 python loop
#----
pat_acct_new = set(df0['pat_acct_new'])
# print(len(pat_acct_new))
pat_acct_exist = set(df1['pat_acct_exist'])
# print(len(pat_acct_exist))
compare_acct_res = list()
for i in pat_acct_new:
    if i not in pat_acct_exist:
        compare_acct_res.append(i)
    else:
        continue
df2 = pd.DataFrame(compare_acct_res)
df2 = df2.sort_values(by=[0], ascending=[True]).reset_index(drop=True)
print(df2.head(3));  print(df2.tail(2))

df2.to_csv('compare_acct_res_v2.txt', index=False, header=False)


#----
# Method 3 python set differences or - operator
#----
# compare_acct_res = list(set(df0['pat_acct_new']).difference(set(df1['pat_acct_exist'])))
compare_acct_res = list(set(df0['pat_acct_new']) - set(df1['pat_acct_exist']))
df2 = pd.DataFrame(compare_acct_res)
df2 = df2.sort_values(by=[0], ascending=[True]).reset_index(drop=True)
print(df2.head(3));  print(df2.tail(2))

df2.to_csv('compare_acct_res_v4.txt', index=False, header=False)

