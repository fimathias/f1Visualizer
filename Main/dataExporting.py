# This is for handling the data exporting part of the program
# Not to be used within functionality of the program

import helper
import api
from imports import csv, pd, datetime


def exportGeneralLapData(session, drivers = None):
    session.load(telemetry=True)
    
    # Get all drivers of the session   
    if drivers is None:
        drivers = helper.getAllDrivers(session)
    
    lapData = session.laps.pick_drivers(drivers)
    
    print(lapData)
    
    lapData.to_csv('general_lap_data.csv', index=False)