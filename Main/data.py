# This is for handling the data part of the program
import helper
import api
from imports import csv, pd

def exportData(session, drivers = None):
    session.load(telemetry=True)
    
    # Get all drivers of the session   
    if drivers is None:
        drivers = helper.getAllDrivers(session)
        
    driversN = []
    carData = {}
    
    for driver in drivers:
        driverN = helper.getDriverNumber(session, driver)
        driversN.append(driverN)
    
    for N in driversN:
        car_data = api.getCarData(session, N)
        car_data['DriverNumber'] = N
        carData[N] = car_data
    
    all_data = pd.concat(carData.values(), ignore_index=True)
    
    all_data.to_csv("test.csv", index=False)

    
    
    
    