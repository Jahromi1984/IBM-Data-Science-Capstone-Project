#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:57:07 2024

@author: alikazemijahromi
"""

import pandas as pd
import numpy as np

file = r'C:\Users\KAZ76504\OneDrive - Personal\OneDrive\Machine Learning\Coursera\IMB Data Science Specialization\Course 10\Week 1\dataset_part_1.csv'
df = pd.read_csv(file)
df.head(10)

print(df.isnull().sum()/len(df)*100)
df.dtypes


### TASK 1: Calculate the number of launches on each site
df['LaunchSite'].value_counts()


### TASK 2: Calculate the number and occurrence of each orbit
print(df['Orbit'].value_counts())


### TASK 3: Calculate the number and occurence of mission outcome of the orbits
landing_outcomes = df['Outcome'].value_counts()
print(landing_outcomes)

for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)

bad_outcomes = set(landing_outcomes.keys()[[1,3,5,6,7]])
bad_outcomes


### TASK 4: Create a landing outcome label from Outcome column
landing_class = []
for outcome in df['Outcome']:
    if outcome in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)
        
df['Class'] = landing_class
df[['Class']].head(8)
print(df["Class"].mean())

df.to_csv("dataset_part_2.csv", index=False)























