from imports import animation, plt, np
import api
import helper
import track

def animateDrivers(session, drivers = None):
    session.load(telemetry=True)
    
    # Rotating the circuit
    circuit_info = session.get_circuit_info()
    # Convert the rotation angle from degrees to radian.
    trackAngle = circuit_info.rotation / 180 * np.pi
    trackPlot = track.trackCorners(session)
    
    # Get all drivers of the session   
    if drivers is None:
        drivers = helper.getAllDrivers(session)
    
    # Telemetry data from session
    telemetryData = api.getTelemetry(session)
    min_x, max_x, min_y, max_y = helper.getMinMaxFromTrack(trackPlot)
    plt.close()
    

    # Set starting frame for telemetry
    startingFrame = 15000
    frames = None
    
    for driver in drivers:
        driverN = helper.getDriverNumber(session, driver)
        telemetryData[driverN] = telemetryData[driverN].iloc[startingFrame:]
        frames = len(telemetryData[driverN])
    

    # Create a function to update the plot
    def update_plot(frame):
        ax.clear()  # Clear the previous plot
        ax.set_title('Position Plot')  # Set the title of the plot
        
                
        # Plot the current position for the specified drivers
        for driver in drivers:
            driverN = helper.getDriverNumber(session, driver)
            
            # Get visuals for drivers and teams
            try:
                driverColor = api.plotting().driver_color(driver)
            except:
                driverColor = "#000000"
            
            positionData = telemetryData[driverN]
            
            # Get coords and rotate
            xyCoords = np.column_stack((positionData['X'].iloc[frame], positionData['Y'].iloc[frame]))
            rotatedCoords = helper.rotate(xyCoords, angle=trackAngle)
            
            
            ax.scatter(rotatedCoords[:,0], rotatedCoords[:,1], c= driverColor, marker='o')
            

        # Set the limits for the x and y axes to cover the entire range of coordinates        
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)

    
    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Create an animation
    ani = animation.FuncAnimation(fig, update_plot, frames=frames, interval=1, repeat=False)

    # Show the plot
    plt.show()