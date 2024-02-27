import api
import track
import animation
import helper
import dataExporting
import getSettings
import frameFunctions
from imports import fastf1, html, dcc, dash, datetime, Input, Output, px
import globalVariables

def startDashApp():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.H1(children=globalVariables.season['OfficialEventName'][globalVariables.eventN], style={'textAlign':'center'}),
        html.Div([
            html.P(id='timeDisplay'),
        ]),
        dcc.Graph(id='trackMap'),
        dcc.Interval(
            id='intervalComponent',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
    
    # Time updating
    @app.callback(
        Output('timeDisplay', 'children'),
        Input('intervalComponent', 'n_intervals')
    )
    def updateTimeDisplay(n):
        time = globalVariables.currentTime
        return time
    
    # Track Map updating
    @app.callback(
        Output('trackMap', 'figure'),
        Input('intervalComponent', 'n_intervals')
    )
    def updateTrackMap(n):              
        frameFunctions.trackMapFrame()
        
        # Increment the global currentTime variable by one second
        globalVariables.currentTime += datetime.timedelta(seconds=1)

        return globalVariables.trackMap

    app.run_server()

if __name__ == "__main__":
    
    # Always to be run, determines season, event, drivers etc.
    # Determines which part of the app to run
    getSettings.getSessionSettings()
    getSettings.getFunctionality()
    
    # Placeholder for testing
    globalVariables.currentTime = globalVariables.startTime
    globalVariables.currentTime += datetime.timedelta(minutes=3)   
    
    # Check functionality
    if globalVariables.function == 1:
        api.getTelemetryFiltered()
        startDashApp()
    elif globalVariables.function == 2:
        dataExporting.exportGeneralLapData(globalVariables.session, globalVariables.selectedDrivers)
    elif globalVariables.function == 0:
        # USE FOR AD-HOC TESTING, NOT FINAL
        
        track.generateTrackMapEmpty()
        
        globalVariables.trackMapEmpty.show()
    
    
    
    
    
    
    
    
    
    
    