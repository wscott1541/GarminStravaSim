# GarminStravaSim
An attempt to recreate Strava's month-by-month progress graph that snowballed.

## data-init.py

Dependent on garmin-connect, https://pypi.org/project/garminconnect/.  
Creates Activities.csv with information about activities that can be used in plots.  
Run file, input username and password when prompted.  
Tested up to 268 activities. 

Manual alternative:  
Download data manually from connect.garmin.com => Activities => All Activities => Export CSV.  
Ensure that all data is included by scrolling down to earliest date.  
Move file to correct location.

## data-import.py

Dependent on garmin-connect, https://pypi.org/project/garminconnect/.  
Updates an existing Activities.csv with any activities since creation or last update.  
Run file, input username and password when prompted.  
Requires existing Activities.csv, which will be archived with yyyy-mm-dd string.

## functions.py

Script containing functions to plot graphs using matplotlib, and associated functions.  
Requires Activities.csv.

## plots.py

Script to plot graphs based on Activities.csv and functions.py.  
Current graphs are:

• Current month and previous, run distance and run duration

• All previous months, run distance and run duration

• All time cumulative run distances 

• Current week and previous, run distance
