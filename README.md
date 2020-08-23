GarminStravaSim
=====================

A weekly email update using Garmin data to replicate some of the graphs that Strava put behind a paywall and adds in a couple of features copied from Endomondo.

Might require [garmin-connect](https://pypi.org/project/garminconnect/), and possibly more.

Dev branch
---------

The branch I actually update but which will likely never be as nice as the master branch, although I'll merge them if I ever reach that stage.  Would suggest trying to use with reference to the master branch.

Currently uses [fitparse](https://pypi.org/project/fitparse/) to read FIT files copied across from the watch manually, with individual activity summary email.

Also set up to send a weekly update email to track progress.

Features:
- Heatmap!  Except not on a map.
- HR graphs and a pie chart!
- Best time calculations across various distances!
- Distance and duration plots for different activities!
- Independence from Garmin servers (although you'll want to get your gpx files from somewhere: maybe try [garmin-connect-export](https://github.com/pe-st/garmin-connect-export) or [tapiriik](https://tapiriik.com/)?)!

Master branch
------------------

Has its own 'documentation' and is structured much more neatly so might actually be useable, except can do much less.
