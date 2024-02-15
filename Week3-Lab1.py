#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:06:38 2024

@author: alikazemijahromi
"""

### Hands-on Lab: Interactive Visual Analytics with Folium lab

import folium
import pandas as pd
from folium.plugins import MarkerCluster
######
# from folium.plugins import MousePosition 
# Note: This plugin seems to have problem #to be installed on most version of 
#Folium and I don't want to install any other #version. So I skipp those tasks 
#related to using this specific plugin in this lab.
#####
from math import sin, cos, sqrt, atan2, radians
from folium.features import DivIcon
import webbrowser
import os
import time
browser = webbrowser.get('chrome')
folder = '//Users//alikazemijahromi//Library//CloudStorage//OneDrive-Personal//Machine Learning//Coursera//IMB Data Science Specialization//Course 10//Week 3//'
os.chdir(folder)


### Task 1: Mark all launch sites on a map
spacex_df = pd.read_csv('spacex_launch_geo.csv')
# Let's take a look at what are the coordinates for each site.
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
print(launch_sites_df)

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)
# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)
site_map.save('mymap.html')
webbrowser.open_new('file://' + os.path.realpath('mymap.html'))


# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. 
#In addition, add Launch site name as a popup label
for index,site in launch_sites_df.iterrows():
    location = [site['Lat'],site['Long']]
    print(site['Launch Site'])
    print(location)

for index,site in launch_sites_df.iterrows():
    location = [site['Lat'],site['Long']]
    circle = folium.Circle(location, radius=1000, color='#d35400', fill= True).add_child(folium.Popup(site['Launch Site']))
    marker = folium.map.Marker(location,
                               icon = DivIcon(
                                   icon_size=(20,20),
                                   icon_anchor=(0,0),
                                   html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % site['Launch Site'],
                               )
                              )
    site_map.add_child(circle)
    site_map.add_child(marker)
site_map.save('mymap.html')
webbrowser.open_new('file://' + os.path.realpath('mymap.html'))




### Task 2: Mark the success/failed launches for each site on the map
# Next, let's create markers for all launch records. If a launch was successful (class=1),
#then we use a green marker and if a launch was failed, we use a red marker (class=0)
marker_cluster = MarkerCluster()
# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
marker_color =[]
for i in spacex_df['class']:
    if i == 1:
        i = 'green'
    else:
        i='red'
    marker_color.append(i)
print(marker_color)
spacex_df['marker_color'] = marker_color # add color to df 
site_map.add_child(marker_cluster)
# Add marker_cluster to current site_map:folium.map.Marker(loc,icon).add_to(map)
for index, record in spacex_df.iterrows():
    location = [record['Lat'],record['Long']]
    marker=folium.map.Marker(location,
                             icon=folium.Icon(color='white', icon_color=record['marker_color'])
                            )
    marker_cluster.add_child(marker) 
site_map.save('mymap.html')
webbrowser.open_new('file://' + os.path.realpath('mymap.html'))




# TASK 3: Calculate the distances between a launch site to its proximities
def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# find coordinate of from KSC LC-39A to the closet coastline
launch_site2_lat = 28.573255
launch_site2_lon = -80.646895
coastline_lat = 28.58109
coastline_lon  = -80.61355
distance_coastline2 = calculate_distance(launch_site2_lat, launch_site2_lon, coastline_lat, coastline_lon)
distance_coastline2

# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
coordinate = [coastline_lat,coastline_lon]
distance_marker = folium.Marker(
    coordinate,
    icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline2),
                ))
site_map.add_child(distance_marker)
# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
lines=folium.PolyLine(locations=[[launch_site2_lat,launch_site2_lon],[coastline_lat,coastline_lon]], weight=1)
site_map.add_child(lines)
site_map.save('mymap.html')
webbrowser.open_new('file://' + os.path.realpath('mymap.html'))

# Create a marker with distance of from KSC LC-39A to a closest city
city_lat = 28.52806
city_lon = -80.65615
distance_city2 = calculate_distance(launch_site2_lat, launch_site2_lon, city_lat, city_lon)
coordinate = [city_lat, city_lon]
distance_marker = folium.Marker(
    coordinate,
    icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_city2),
                ))
site_map.add_child(distance_marker)
# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
lines=folium.PolyLine(locations=[[launch_site2_lat,launch_site2_lon],[city_lat,city_lon]], weight=1)
site_map.add_child(lines)
site_map.save('mymap.html')
webbrowser.open_new('file://' + os.path.realpath('mymap.html'))

# Create a marker with distance of from CCAFS SLC-40 to a closest railway
launch_site1_lat = 28.563197
launch_site1_lon = -80.576820
railway_lat = 28.57246
railway_lon = -80.58507
distance_railway1 = calculate_distance(launch_site1_lat, launch_site1_lon, railway_lat, railway_lon)
coordinate = [railway_lat, railway_lon]
distance_marker = folium.Marker(
    coordinate,
    icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_railway1),
                ))
site_map.add_child(distance_marker)
# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
lines=folium.PolyLine(locations=[[launch_site1_lat,launch_site1_lon],coordinate], weight=1)
site_map.add_child(lines)
site_map.save('mymap.html')
webbrowser.open_new('file://' + os.path.realpath('mymap.html'))

# Create a marker with distance of from CCAFS SLC-40 to a closest highway
highway_lat = 28.54779
highway_lon = -80.56825
distance_highway1 = calculate_distance(launch_site1_lat, launch_site1_lon, highway_lat, highway_lon)
coordinate = [highway_lat, highway_lon]
distance_marker = folium.Marker(
    coordinate,
    icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0),html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_highway1),
                ))
site_map.add_child(distance_marker)
# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
lines=folium.PolyLine(locations=[[launch_site1_lat,launch_site1_lon],coordinate], weight=1)
site_map.add_child(lines)
site_map.save('mymap.html')
webbrowser.open_new('file://' + os.path.realpath('mymap.html'))




















