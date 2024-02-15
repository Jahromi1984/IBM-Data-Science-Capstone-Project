#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:58:50 2024

@author: alikazemijahromi
"""

import csv, sqlite3
import pandas as pd
import os
os.chdir('/Users/alikazemijahromi/Library/CloudStorage/OneDrive-Personal/Machine Learning/Coursera/IMB Data Science Specialization/Course 10/Week 2')

# %load_ext sql # This is to emulate Jupyter for online database handling

con = sqlite3.connect("my_data1.db")
cur = con.cursor()
%sql sqlite:///my_data1.db

df = pd.read_csv('Spacex.csv')
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")
# OR:
%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null


### Tasks
# Now write and execute SQL queries to solve the assignment tasks.
# Note: If the column names are in mixed case enclose it in double quotes For 
#Example "Landing_Outcome"


## Task 1: Display the names of the unique launch sites in the space mission
cur.execute("SELECT DISTINCT(Launch_Site) FROM SPACEXTABLE")
cur.fetchall()
 

## Task 2: Display 5 records where launch sites begin with the string 'CCA'
cur.execute("SELECT Launch_Site FROM SPACEXTABLE WHERE Launch_Site LIKE 'CCA%' LIMIT 5")
cur.fetchall()


## Task 3: Display the total payload mass carried by boosters launched by NASA (CRS)
cur.execute("SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE Customer='NASA (CRS)'")
cur.fetchall()


## Task 4: Display average payload mass carried by booster version F9 v1.1
cur.execute("SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE Booster_Version='F9 v1.1'")
cur.fetchall()


## Task 5: List the date when the first succesful landing outcome in ground pad was acheived.
cur.execute("SELECT MIN(DATE) FROM SPACEXTABLE WHERE Landing_Outcome LIKE 'Success (ground pad)'")
cur.fetchall()


## Task 6: List the names of the boosters which have success in drone ship and 
#have payload mass greater than 4000 but less than 6000
cur.execute("SELECT Booster_Version FROM SPACEXTABLE WHERE Landing_Outcome LIKE 'Success (ground pad)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000")
cur.fetchall()


## Task 7: List the total number of successful and failure mission outcomes
cur.execute("SELECT Mission_Outcome, Count(Mission_Outcome) FROM SPACEXTBL GROUP BY Mission_Outcome")
cur.fetchall()


## Task 8: List the names of the booster_versions which have carried the 
#maximum payload mass. Use a subquery
cur.execute("SELECT DISTINCT(Booster_Version) FROM SPACEXTABLE WHERE PAYLOAD_MASS__KG_=(SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE)")
cur.fetchall()


































