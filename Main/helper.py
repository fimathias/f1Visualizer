# This provides helper functions to the other parts
from imports import np, pd

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def getAllDrivers(session):
    drivers = pd.unique(session.laps['Driver'])
    return drivers

def getDriverNumber(session, driver: int):
    driver = session.get_driver(driver)
    return driver["DriverNumber"]


# DONT USE
def getMinMaxFromSession(session):
    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()
    
    min_x = pos['X'].min()
    max_x = pos['X'].max()
    min_y = pos['Y'].min()
    max_y = pos['Y'].max()
    
    return min_x, max_x, min_y, max_y

def getMinMaxFromTrack(track):
    ax = track.gca()
    
    # Get the minimum and maximum values of x and y from the plot
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    
    return x_min, x_max, y_min, y_max