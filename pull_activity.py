#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:23:16 2020

@author: WS
"""

import time

#act = [{'activityId': 5027176995, 'activityName': 'Cardio', 'description': None, 'startTimeLocal': '2020-06-02 08:12:31', 'startTimeGMT': '2020-06-02 07:12:31', 'activityType': {'typeId': 11, 'typeKey': 'indoor_cardio', 'parentTypeId': 29, 'sortOrder': 19}, 'eventType': {'typeId': 9, 'typeKey': 'uncategorized', 'sortOrder': 10}, 'comments': None, 'parentId': None, 'distance': 533.3200073242188, 'duration': 2845.087890625, 'elapsedDuration': 2845087.890625, 'movingDuration': 341.0, 'elevationGain': None, 'elevationLoss': None, 'averageSpeed': 0.18700000643730164, 'maxSpeed': 3.3489999771118164, 'startLatitude': None, 'startLongitude': None, 'hasPolyline': False, 'ownerId': 83784870, 'ownerDisplayName': '965cb392-b599-42f5-9eeb-970c82218448', 'ownerFullName': 'Will Scott', 'ownerProfileImageUrlSmall': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/293a9a88-c7d9-4e8b-911a-2dfefb227548-83784870.png', 'ownerProfileImageUrlMedium': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/399a781c-86ae-414f-a7e9-ecb3b22383bd-83784870.png', 'ownerProfileImageUrlLarge': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/e1165d13-1461-4ab5-9f5a-6468c06e7d0d-83784870.png', 'calories': 304.0, 'averageHR': 108.0, 'maxHR': 150.0, 'averageRunningCadenceInStepsPerMinute': 122.0, 'maxRunningCadenceInStepsPerMinute': 170.0, 'averageBikingCadenceInRevPerMinute': None, 'maxBikingCadenceInRevPerMinute': None, 'averageSwimCadenceInStrokesPerMinute': None, 'maxSwimCadenceInStrokesPerMinute': None, 'averageSwolf': None, 'activeLengths': None, 'steps': 164, 'conversationUuid': None, 'conversationPk': None, 'numberOfActivityLikes': None, 'numberOfActivityComments': None, 'likedByUser': None, 'commentedByUser': None, 'activityLikeDisplayNames': None, 'activityLikeFullNames': None, 'requestorRelationship': None, 'userRoles': ['ROLE_CONNECTUSER', 'ROLE_FITNESS_USER', 'ROLE_WELLNESS_USER'], 'privacy': {'typeId': 3, 'typeKey': 'subscribers'}, 'userPro': False, 'courseId': None, 'poolLength': None, 'unitOfPoolLength': None, 'hasVideo': False, 'videoUrl': None, 'timeZoneId': 159, 'beginTimestamp': 1591081951000, 'sportTypeId': 0, 'avgPower': None, 'maxPower': None, 'aerobicTrainingEffect': None, 'anaerobicTrainingEffect': None, 'strokes': None, 'normPower': None, 'leftBalance': None, 'rightBalance': None, 'avgLeftBalance': None, 'max20MinPower': None, 'avgVerticalOscillation': None, 'avgGroundContactTime': None, 'avgStrideLength': 9.218995625988203, 'avgFractionalCadence': None, 'maxFractionalCadence': None, 'trainingStressScore': None, 'intensityFactor': None, 'vO2MaxValue': None, 'avgVerticalRatio': None, 'avgGroundContactBalance': None, 'lactateThresholdBpm': None, 'lactateThresholdSpeed': None, 'maxFtp': None, 'avgStrokeDistance': None, 'avgStrokeCadence': None, 'maxStrokeCadence': None, 'workoutId': None, 'avgStrokes': None, 'minStrokes': None, 'deviceId': 3317446185, 'minTemperature': None, 'maxTemperature': None, 'minElevation': None, 'maxElevation': None, 'avgDoubleCadence': None, 'maxDoubleCadence': 170.0, 'summarizedExerciseSets': None, 'maxDepth': None, 'avgDepth': None, 'surfaceInterval': None, 'startN2': None, 'endN2': None, 'startCns': None, 'endCns': None, 'summarizedDiveInfo': {'weight': None, 'weightUnit': None, 'visibility': None, 'visibilityUnit': None, 'surfaceCondition': None, 'current': None, 'waterType': None, 'waterDensity': None, 'summarizedDiveGases': [], 'totalSurfaceTime': None}, 'activityLikeAuthors': None, 'avgVerticalSpeed': None, 'maxVerticalSpeed': None, 'floorsClimbed': None, 'floorsDescended': None, 'manufacturer': None, 'diveNumber': None, 'locationName': None, 'bottomTime': None, 'lapCount': 1, 'endLatitude': None, 'endLongitude': None, 'minAirSpeed': None, 'maxAirSpeed': None, 'avgAirSpeed': None, 'avgWindYawAngle': None, 'minCda': None, 'maxCda': None, 'avgCda': None, 'avgWattsPerCda': None, 'flow': None, 'grit': None, 'jumpCount': None, 'caloriesEstimated': None, 'caloriesConsumed': None, 'waterEstimated': None, 'waterConsumed': None, 'maxAvgPower_1': None, 'maxAvgPower_2': None, 'maxAvgPower_5': None, 'maxAvgPower_10': None, 'maxAvgPower_20': None, 'maxAvgPower_30': None, 'maxAvgPower_60': None, 'maxAvgPower_120': None, 'maxAvgPower_300': None, 'maxAvgPower_600': None, 'maxAvgPower_1200': None, 'maxAvgPower_1800': None, 'maxAvgPower_3600': None, 'maxAvgPower_7200': None, 'maxAvgPower_18000': None, 'excludeFromPowerCurveReports': None, 'totalSets': None, 'activeSets': None, 'totalReps': None, 'minRespirationRate': None, 'maxRespirationRate': None, 'avgRespirationRate': None, 'trainingEffectLabel': None, 'activityTrainingLoad': None, 'avgFlow': None, 'avgGrit': None, 'minActivityLapDuration': None, 'startStress': None, 'endStress': None, 'differenceStress': None, 'aerobicTrainingEffectMessage': None, 'anaerobicTrainingEffectMessage': None, 'splitSummaries': [], 'hasSplits': False, 'favorite': False, 'pr': False, 'autoCalcCalories': False, 'parent': False, 'atpActivity': False, 'decoDive': None, 'elevationCorrected': False, 'purposeful': False}]

#sort activity into vaguely useable forms
def pull_from_activity(activity):
    string_activity = str(activity)

    string_activity = string_activity.replace('[{','')
    string_activity = string_activity.replace('}]','')

    list_activity_strings = string_activity.split(',')

    #pull useful information (date, type, duration, distance)
    number_string = list_activity_strings[0][14:]
    date_string = list_activity_strings[3][20:-1]
    type_string = list_activity_strings[6][13:-1]    
    type_string = type_string.capitalize()
    if type_string == 'Indoor_cardio':
        type_string = 'Cardio'
    durs_string = list_activity_strings[16][20:]#16 is elapsed duration (ms), 15 is duration (s)
    dist_string = list_activity_strings[14][13:]
    dist_float = round(float(dist_string)/1000,2)#convert from m to km
    dist_string = str(dist_float)

    durs_float = float(durs_string)/1000#convert from milliseconds to seconds
    durs_string = time.strftime('%H:%M:%S',time.gmtime(durs_float))

    row = [number_string,type_string,date_string,dist_string,durs_string]
    
    return(row)

