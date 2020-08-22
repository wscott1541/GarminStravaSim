GarminStravaSim
=====================

A basic weekly email update using Garmin data to replicate some of the graphs that Strava put behind a paywall.

Requires [garmin-connect](https://pypi.org/project/garminconnect/), and possibly more.


Master branch
------------------

- setup.py
  Downloads past data from Garmin; creates relevant csv files.
- add_user.py
  As above, if you can persuade a friend to give you their Garmin password.  Allows comparative graphs.
- email_setup.py
  Sets up details for generating emails.
- plots.py
  Displays various graphs for Running, Cycling, Hiking, Walking, Cardio and All activities, including:
  - Distances and durations over the current & prior weeks & months
  - All previous distances and durations by months
  - Cumulative distances by months
  Modify as desired.
- email_gen.py
  As plots.py, but puts them into an email which it sends to yourself.
  Modify as desired.
- update.py
  Pulls new activity information from Garmin and updates activities.csv
- email_shell.py
  Groups update.py and email_gen.py.
  Used to automate weekly summary emails without repeating each day.
  Modify as desired.
- Miscellaneous
  - data_read.py: functions to read activities.csv
  - primary_user_functions.py & multiple_user_functions.py: functions to plot graphs
  - pull_activity.py: function to pull relevant information from Garmin
  - today_string.py: functions for today's date


Dev branch
---------

The much more exciting branch that I use and update but which is not nearly as systematic and probably never will be.  

Includes more and neater graphs.  The emails are completely html too, which is nice.

Scans GPX files for best times and keeps track of PBs.  Did use [garmin-connect-export](https://github.com/pe-st/garmin-connect-export) for this, but that didn't appear to survive the Garmin hack and I've not used since.  Might work again now; who knows?

Uses [fitparse](https://pypi.org/project/fitparse/) to read FIT files copied across from the watch manually.  Scans these and emails a nice summary, including a heatmap, HR graphs and best times.