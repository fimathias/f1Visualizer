# These functions are for generating specific data based on time
# Used in "real-time" visualization of races.
from imports import datetime, np, plt, px, go
import api
import helper
import track
import globalVariables

def getTelemetryAtTime():
    # Gets the current telemetry at a time point
    telemetryAtTime = helper.getFramesFromTime(globalVariables.telemetryData)

    return(telemetryAtTime)

def trackMapFrame():
    # TODO Add Colors and names for the driver points
    
    data = getTelemetryAtTime()
    
    # Rotating the circuit
    globalVariables.circuitInfo = globalVariables.session.get_circuit_info()
    # Convert the rotation angle from degrees to radian.
    globalVariables.trackAngle = globalVariables.circuitInfo.rotation / 180 * np.pi
    
    fig = px.scatter()
    
    # Define min and max of plot
    helper.getMinMax()
    
    fig.update_xaxes(range=[globalVariables.x_min, globalVariables.x_max], fixedrange=True)
    fig.update_yaxes(range=[globalVariables.y_min, globalVariables.y_max], fixedrange=True)
        
    for driverN in data:
        xyCoords = (data[driverN]['X'], data[driverN]['Y'])
        
        rotatedCoords = helper.rotate(xyCoords, angle=globalVariables.trackAngle)
        
        fig.add_trace(go.Scatter(x=[rotatedCoords[0]], y=[rotatedCoords[1]], mode='markers', name=f'Driver {driverN}'))
    
    # Return the scatter plot
    globalVariables.trackMap = fig
        
        