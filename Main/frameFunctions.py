# These functions are for generating specific data based on time
# Used in "real-time" visualization of races.
from imports import datetime, np, plt, px, go
import api
import helper
import track
import globalVariables

def getTelemetryAtTime(telemetry: api.getTelemetryFiltered):
    # Gets the current telemetry at a time point
    telemetryAtTime = helper.getFramesFromTime(telemetry)

    return(telemetryAtTime)

def plotTrackPositionsAtTime(telemetry: api.getTelemetryFiltered):
    # TODO Add Colors and names for the driver points
    
    data = getTelemetryAtTime(telemetry)
    
    # Rotating the circuit
    circuit_info = globalVariables.session.get_circuit_info()
    # Convert the rotation angle from degrees to radian.
    trackAngle = circuit_info.rotation / 180 * np.pi
    
    fig = px.scatter()
        
    for driverN in data:
        xyCoords = (data[driverN]['X'], data[driverN]['Y'])
        
        print(xyCoords)
        
        rotatedCoords = helper.rotate(xyCoords, angle=trackAngle)
        
        fig.add_trace(go.Scatter(x=[rotatedCoords[0]], y=[rotatedCoords[1]], mode='markers', name=f'Driver {driverN}'))
    
    # Return the scatter plot
    return fig
        
        