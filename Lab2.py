# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 16:35:04 2024

@author: KAZ76504
"""

### In this lab, you will perform Exploratory Data Analysis and Feature Engineering.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

Mac = 1
if Mac==0:
    folder = r'C:\Users\KAZ76504\OneDrive - Personal\OneDrive\Machine Learning\Coursera\IMB Data Science Specialization\Course 10\Week 2'
    slash = '\\'
else:
    folder = r'/Users/alikazemijahromi/Library/CloudStorage/OneDrive-Personal/Machine Learning/Coursera/IMB Data Science Specialization/Course 10/Week 2'
    slash = '/'
    
filename = 'dataset_part_2.csv'
path = folder + slash + filename
df = pd.read_csv(path)
print(df.head())

fontsize = 12
# We can plot out the FlightNumber vs. PayloadMassand overlay the outcome of the 
#launch. We see that as the flight number increases, the first stage is more
#likely to land successfully. The payload mass is also important; it seems the 
#more massive the payload, the less likely the first stage will return.
plt.figure()
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect=4)
plt.xlabel("Flight Number",fontsize=fontsize)
plt.ylabel("Pay load Mass (kg)",fontsize=fontsize)


### TASK 1: Visualize the relationship between Flight Number and Launch Site
plt.figure()
sns.catplot(data=df, y="LaunchSite", x="FlightNumber", hue="Class", aspect=3)
plt.xlabel("Flight Number",fontsize=fontsize)
plt.ylabel("Launch Site",fontsize=fontsize)


### TASK 2: Visualize the relationship between Payload and Launch Site
plt.figure()
sns.catplot(data=df, y="PayloadMass", x="LaunchSite", hue="Class", aspect=3)
plt.xlabel("Launch Site",fontsize=fontsize)
plt.ylabel("Pay load Mass (kg)",fontsize=fontsize)


### TASK 3: Visualize the relationship between success rate of each orbit type
df_orbit = df[['Orbit', 'Class']].groupby(['Orbit']).mean(numeric_only=True).reset_index()
df_orbit.columns = ['Orbit', 'Success Rate']
plt.figure()
sns.barplot(data=df_orbit, y='Success Rate', x="Orbit")
plt.xlabel("Orbit",fontsize=fontsize)
plt.ylabel("Success Rate", fontsize=fontsize)


### TASK 4: Visualize the relationship between FlightNumber and Orbit type
plt.figure()
sns.catplot(data=df, y="Orbit", x="FlightNumber", hue="Class", aspect=3)
plt.xlabel("Flight Number",fontsize=fontsize)
plt.ylabel("Orbit",fontsize=fontsize)


### TASK  5: Visualize the relationship between Payload and Orbit type
plt.figure()
sns.catplot(data=df, y="Orbit", x="PayloadMass", hue="Class", aspect=3)
plt.xlabel("Pay load Mass (kg)",fontsize=fontsize)
plt.ylabel("Orbit",fontsize=fontsize)


### TASK  6: Visualize the launch success yearly trend
df_year = df[['Date', 'Class']]
#df_year['Date'] = df_year['Date'].apply(lambda row: row[0:4])
df_year.loc[:, 'Date'] = df_year['Date'].apply(lambda row: row[0:4])
df_year = df_year.groupby(['Date']).mean(numeric_only=True).reset_index()
df_year.columns = ['Year', 'Success Rate']
plt.figure()
sns.lineplot(data=df_year, x='Year', y='Success Rate')


#####
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
print(features.head())
print(features.info())
#####


### TASK  7: Create dummy variables to categorical columns
features_one_hot = pd.get_dummies(features,columns = ['Orbit','LaunchSite','Serial','LandingPad'])
print(features_one_hot.head())


### TASK  8: Cast all numeric columns to `float64`
features_one_hot = features_one_hot.astype('float64')
features_one_hot.dtypes


features_one_hot.to_csv('dataset_part_3.csv', index=False)
























