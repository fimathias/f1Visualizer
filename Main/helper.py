# This provides helper functions to the other parts
from imports import np, pd, datetime
import globalVariables

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def getAllDrivers(session):
    drivers = pd.unique(session.laps['Driver'])
    return drivers

def getDriverNumber(driver):
    driver = globalVariables.session.get_driver(driver)
    return driver["DriverNumber"]

def getMinMax():
    # Returns the min and max for the x and y coordinates based on the fastest lap
    fastestLap = globalVariables.session.laps.pick_fastest().get_telemetry(frequency=1)
    
    for i, (x, y) in enumerate(zip(fastestLap['X'], fastestLap['Y'])):
        xyCoords = (x,y)
        rotatedCoords = rotate(xy=xyCoords, angle=globalVariables.trackAngle)
        fastestLap['X'][i] = rotatedCoords[0]
        fastestLap['Y'][i] = rotatedCoords[1]
    
    xDeltaPct = abs((fastestLap['X'].max() - fastestLap['X'].min()) * 0.10)
    yDeltaPct = abs((fastestLap['Y'].max() - fastestLap['Y'].min()) * 0.10)
    
    globalVariables.x_min = fastestLap['X'].min() - xDeltaPct
    globalVariables.x_max = fastestLap['X'].max() + xDeltaPct

    globalVariables.y_min = fastestLap['Y'].min() - yDeltaPct
    globalVariables.y_max = fastestLap['Y'].max() + yDeltaPct
    
    
    #print("here are the min and max values")
    #print(globalVariables.x_min, globalVariables.x_max, globalVariables.y_min, globalVariables.y_max)
    

def getFramesFromTime(data):
    # Takes a datetime object and a data object as inputs
    # Returns the same object but with only the closest data points
    
    dataAtTime = {}
    timeString = globalVariables.currentTime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    for i in data:
        dataSingle = data[i]
        dataSingle['Date'] = pd.to_datetime(dataSingle['Date'])
        
        time_timestamp = pd.Timestamp(timeString)

        # Find the closest timestamp in telemetry data
        closest_entry = min(dataSingle['Date'], key=lambda x: abs(x - time_timestamp))
        
        # Retrieve telemetry data at the closest timestamp for each driver
        dataAtTime[i] = dataSingle[dataSingle['Date'] == closest_entry].iloc[0]

    return(dataAtTime)
    
    