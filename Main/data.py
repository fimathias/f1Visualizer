# This is for handling the data part of the program
import helper
import api
from imports import csv, pd

def exportGeneralLapData(session, drivers = None):
    session.load(telemetry=True)
    
    # Get all drivers of the session   
    if drivers is None:
        drivers = helper.getAllDrivers(session)
    
    lapData = session.laps.pick_drivers(drivers)
    lapData.to_csv('general_lap_data.csv', index=False)
        



    
    
    
    