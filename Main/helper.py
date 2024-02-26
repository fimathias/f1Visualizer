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

def getMinMaxFromTrack(track):
    ax = track.gca()
    
    # Get the minimum and maximum values of x and y from the plot
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    
    return x_min, x_max, y_min, y_max

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
    
    