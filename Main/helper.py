# This provides helper functions to the other parts
from imports import np, pd, datetime
import api
import globalVariables

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def getAllDrivers(session):
    drivers = pd.unique(session.laps['Driver'])
    return drivers

def getDriverNumber(driver):
    # Gets the driver number from driver abbreviation
    driver = globalVariables.session.get_driver(driver)
    return driver["DriverNumber"]

def getDriverAbbr(driverN):
    # Gets the driver abbreviation from driver number
    driver = globalVariables.session.get_driver(driverN)
    return driver["Abbreviation"]

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

def getLapTimings():
    # Goes through the lapdata object to find at which points in time the leading driver started the next lap
    
    data = globalVariables.lapData
    data['LapStartDate'] = pd.to_datetime(data['LapStartDate'])
    
    # Check if 'LapStartTime' is of type Timedelta
    if isinstance(data['LapStartDate'].iloc[0], pd.Timedelta):
        # Convert Timedelta to string and format to keep only the time part
        data['LapStartDate'] = data['LapStartDate'].apply(lambda x: str(x).split()[-1])
    else:
        # Convert Timestamp to string and format to keep only the time part
        data['LapStartDate'] = data['LapStartDate'].dt.time.astype(str).apply(lambda x: x.split()[-1])
      
    lapStartTimes = data.groupby('LapNumber')['LapStartDate'].min()
    
    globalVariables.lapTimings = lapStartTimes

def getCurrentLap():    
    # Gets the current lap from the current time
    currentTime = pd.Timestamp(globalVariables.currentTime)
    
    lap_numbers = sorted(globalVariables.lapTimings.keys())
    
    for lap_number in lap_numbers:
        lap_time_str = globalVariables.lapTimings[lap_number]
        
        # Adjust format string to include milliseconds
        lap_time = pd.to_datetime(lap_time_str, format="%H:%M:%S.%f").time()
        lap_time_timestamp = pd.Timestamp.combine(currentTime.date(), lap_time)
        
        if lap_time_timestamp > currentTime:
            globalVariables.lapCurrent = lap_number - 1  # Previous lap
            return
    
    # If the current time is beyond all lap times, set lapCurrent to the last lap number
    
    globalVariables.lapCurrent = len(globalVariables.lapTimings)       