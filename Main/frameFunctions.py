# These functions are for generating specific data based on time
# Used in "real-time" visualization of races.
from imports import datetime, np, plt, px, go, dash_table, pd
import api
import helper
import track
import globalVariables

def getTelemetryAtTime():
    # Gets the current telemetry at a time point
    telemetryAtTime = helper.getFramesFromTime(globalVariables.telemetryData)

    return(telemetryAtTime)

def trackMapFrame():
    # Get data from current time point
    data = getTelemetryAtTime()
    
    # Check if track exists, if not generate it
    if not globalVariables.trackMapEmpty:
        track.generateTrackMapEmpty()
    
    # Rotating the circuit
    globalVariables.circuitInfo = globalVariables.session.get_circuit_info()
    # Convert the rotation angle from degrees to radian.
    globalVariables.trackAngle = globalVariables.circuitInfo.rotation / 180 * np.pi
    
    fig = go.Figure(data=globalVariables.trackMapEmpty.data)
    
    # Define min and max of plot (if not exists)
    if not globalVariables.x_max:
        helper.getMinMax()
    
    fig.update_xaxes(range=[globalVariables.x_min, globalVariables.x_max], fixedrange=True)
    fig.update_yaxes(range=[globalVariables.y_min, globalVariables.y_max], fixedrange=True)
        
    for driverN in data:
        # Handle color data
        driver = helper.getDriverAbbr(str(driverN))
        try:
            driverColor = api.plotting().driver_color(driver)
        except:
            driverColor = "#000000"
        
        xyCoords = (data[driverN]['X'], data[driverN]['Y'])
        rotatedCoords = helper.rotate(xyCoords, angle=globalVariables.trackAngle)
        
        fig.add_trace(go.Scatter(
            x=[rotatedCoords[0]],
            y=[rotatedCoords[1]],
            mode='markers',
            name=f'{driver} ({driverN})',
            marker=dict(color=driverColor)
        ))
    
    # Configure basic layout
    layout = go.Layout(
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False)
    )
    
    fig.update_layout(layout)
    
    # Return the scatter plot
    globalVariables.trackMap = fig
        
def positionFrames():
    # Creates the table figure for the current standings
    try:
        data = globalVariables.lapStandings[int(globalVariables.lapCurrent)]
        positions = [entry[0] for entry in data]
        driver_names = [entry[1] for entry in data]
    except:
        data = "No data available yet"
        positions = "---"
        driver_names = "---"
    
    # Create a DataFrame from the lap standings data
    lap_standings_df = pd.DataFrame({'Position': positions, 'Driver Name': driver_names})

    # Sort the DataFrame by position
    lap_standings_df = lap_standings_df.sort_values(by="Position")
    
    # Creating the DataTable object
    standingsTable = dash_table.DataTable(
        id='lap-standings-table',
        columns=[{"name": i, "id": i} for i in lap_standings_df.columns],
        data=lap_standings_df.to_dict('records')
    )
    
    globalVariables.standingsTable = standingsTable
    