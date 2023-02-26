import pandas as pd
import numpy as np
import re

df = pd.read_csv('glassdoor_jobs_250.csv')




# Salary parsing

df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: re.sub(r'(\d+)(T)',r'0.\1L',x)) #Convert salaries in 'Thousand' to 'Lacs'
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)

df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_rs = salary.apply(lambda x: x.replace('₹','').replace('L',''))

minus_txt = minus_rs.apply(lambda x: x.lower().replace('employer provided salary:','')).replace(' ','')

df['min_salary'] = minus_txt.apply(lambda x: float(x.split('-')[0]))
df['max_salary'] = minus_txt.apply(lambda x: float(x.split('-')[-1]))
df['avg_salary'] = (df['min_salary'] + df['max_salary'])/2

# Company name text only
df['company_txt']= df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3],axis=1)

# Age of the Company
df['age'] = df['Founded'].apply(lambda x: 2023-x if x != -1 else x)

# Parsing of job description (python, SQL etc.)
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['SQL_yn'] = df['Job Description'].apply(lambda x: 1 if 'SQL' in x.lower() else 0)
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

df_out = df.drop(['Unnamed: 0'],axis=1)
df_out.to_csv('glassdoor_jobs_cleaned.csv',index=False)