# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 19:53:25 2018

@author: Malini
"""

import sqlite3
import pandas as pd
#import pandas.io.sql as pd_sql
from pandas import DataFrame, Series
#cols = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country', 'label']
data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data', sep='\s*,\s*',header=None, encoding='ascii', engine='python')
print(data.head())

#Rename the columns
data.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country', 'label']

#print(data.dtypes)
# Create a sql db from adult dataset and name it sqladb
connection = sqlite3.connect("sqladb") 
#pd_sql.write_frame(data, "tbldata2", connection)
#cursor is used to execute sql Queries
cursor = connection.cursor()
#1. Select 10 records from the  sqladb
data.to_sql("sqladb", connection, if_exists = "replace", index = False)
#cursor.execute("drop table sqladb")
cursor.execute('SELECT * FROM sqladb limit 10')
#Result = pd.DataFrame(cursor.fetchall())
#Result1 = cursor.fetchall()
#print(Result1)
result2 = pd.read_sql_query("SELECT * FROM sqladb limit 10", connection)
result2

#2. Show me the average hours per week of all men who are working in private sector
Avg_Hours = pd.read_sql_query("SELECT avg(hours_per_week) FROM sqladb where workclass='Private'and sex='Male'", connection)
Avg_Hours
#3. Show me the frequency table for education, occupation and relationship, separately
Freq = pd.read_sql_query("SELECT education, COUNT(*) FROM sqladb GROUP BY education", connection)
Freq
Freq_occupation = pd.read_sql_query("SELECT occupation, COUNT(*) FROM sqladb GROUP BY occupation", connection)
Freq_occupation
Freq_relationship = pd.read_sql_query("SELECT occupation, COUNT(*) FROM sqladb GROUP BY occupation", connection)
Freq_relationship

#4. Are there any people who are married, working in private sector and having a masters degree
#cursor.close()
Population = pd.read_sql_query("SELECT count(*) FROM sqladb where workclass='Private' and education='Masters' and marital_status!='Never-married'", connection)
Population
#print(data.dtypes)
#5. What is the average, minimum and maximum age group for people working in different sectors
sector_pop = pd.read_sql_query("SELECT workclass, avg(age),min(age),max(age) FROM sqladb GROUP BY workclass", connection)
sector_pop
#6. Calculate age distribution by country
distr = data.pivot_table(columns='native_country')
distr

#7. Compute a new column as 'Net-Capital-Gain' from the two columns 'capital-gain' and 'capital-loss'
Net_Capital_Gain = pd.read_sql_query("SELECT *, capital_gain-capital_loss AS Net_Capital_Gain FROM sqladb ORDER BY Net_Capital_Gain DESC", connection)
Net_Capital_Gain
#connection.close()