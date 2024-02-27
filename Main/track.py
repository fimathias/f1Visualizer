# This handles the visual part of the track
from imports import pd, np, plt, os, px, go
import globalVariables
import helper



# Creates a pyplot of a track in a session, then overlays the corner numbers onto the track layout
def generateTrackMapEmpty():  
    
    # Check for missing required data and fix if missing
    if not globalVariables.circuitInfo:
        # Rotating the circuit
        globalVariables.circuitInfo = globalVariables.session.get_circuit_info()
        
    if not globalVariables.trackAngle:
        # Convert the rotation angle from degrees to radian.
        globalVariables.trackAngle = globalVariables.circuitInfo.rotation / 180 * np.pi
    
    if not globalVariables.x_min:
        # Define min and max of plot
        helper.getMinMax()
    
    
    # Load empty trackMap
    fig = px.scatter()
    
    fig.update_xaxes(range=[globalVariables.x_min, globalVariables.x_max], fixedrange=True)
    fig.update_yaxes(range=[globalVariables.y_min, globalVariables.y_max], fixedrange=True)
    
    lap = globalVariables.session.laps.pick_fastest().get_telemetry(frequency=20)
    filteredLap = lap[['X', 'Y']]
    
    rotatedTrack = filteredLap

    # Rotate and plot the track map.
    for i, (x, y) in enumerate(zip(filteredLap['X'], filteredLap['Y'])):
        xyCoords = (x,y)
        rotatedCoords = helper.rotate(xy=xyCoords, angle=globalVariables.trackAngle)
        
        rotatedTrack['X'][i] = rotatedCoords[0]
        rotatedTrack['Y'][i] = rotatedCoords[1]
    
    
    # Replace last 5 data points with first 5 data points, fixes clipping at end of data
    rotatedTrack.iloc[-10:] = rotatedTrack.iloc[:10].values
    
    fig.add_trace(go.Scatter(x=rotatedTrack['X'], y=rotatedTrack['Y'], mode='lines'))
    
    
    # TODO Add corner naming
    
    offset_vector = [500, 0]  # offset length is chosen arbitrarily to 'look good'
    
    """
    
    # Iterate over all corners.
    for _, corner in globalVariables.circuitInfo.corners.iterrows():
        # Create a string from corner number and letter
        txt = f"{corner['Number']}{corner['Letter']}"

        # Convert the angle from degrees to radian.
        offset_angle = corner['Angle'] / 180 * np.pi

        # Rotate the offset vector so that it points sideways from the track.
        offset_x, offset_y = helper.rotate(offset_vector, angle=offset_angle)

        # Add the offset to the position of the corner
        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y

        # Rotate the text position equivalently to the rest of the track map
        text_x, text_y = helper.rotate([text_x, text_y], angle=globalVariables.trackAngle)

        # Rotate the center of the corner equivalently to the rest of the track map
        track_x, track_y = helper.rotate([corner['X'], corner['Y']], angle=globalVariables.trackAngle)

        # Draw a circle next to the track.
        plt.scatter(text_x, text_y, color='grey', s=140)

        # Draw a line from the track to this circle.
        plt.plot([track_x, text_x], [track_y, text_y], color='grey')

        # Finally, print the corner number inside the circle.
        plt.text(text_x, text_y, txt,
                va='center_baseline', ha='center', size='small', color='white')
    
    
    """
    
    # Sets the generated trackMap as the empty trackMap
    globalVariables.trackMapEmpty = fig

  
def trackImage(session):
    # TODO FIX!
    script_dir = os.path.dirname(os.path.realpath(__file__))
    media_dir = os.path.join(script_dir, "..", "media", "track")
    
    plt = trackPlt(session)
    name = session.event["OfficialEventName"]
    
    # Ensure the directory exists, create if not
    os.makedirs(media_dir, exist_ok=True)
    
    # Save the plot to the specified folder
    plt.savefig(os.path.join(media_dir, f'{name}.png'))
    plt.close()
    
