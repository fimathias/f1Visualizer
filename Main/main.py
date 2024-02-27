import api
import helper
import dataExporting
import getSettings
import frameFunctions
from imports import html, dcc, dash, datetime, Input, Output, State
import globalVariables

def startDashApp():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.H1(children=globalVariables.season['OfficialEventName'][globalVariables.eventN], style={'textAlign':'center'}),
        html.Div([
            html.P(id='timeDisplay'),
            html.P(id='lapCounter')
        ]),
        dcc.Graph(id='trackMap'),
        globalVariables.standingsTable,
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
        
        # Increment the global currentTime variable by one second
        globalVariables.currentTime += datetime.timedelta(seconds=1)
        
        return time
    
    # Lap Counter updating
    @app.callback(
        Output('lapCounter', 'children'),
        Input('intervalComponent', 'n_intervals')
    )
    def updateLapCounter(n):
        # TODO Add current lap of total laps
        helper.getCurrentLap()
        lap = globalVariables.lapCurrent
        return lap
    
    # Track Map updating
    @app.callback(
        Output('trackMap', 'figure'),
        Input('intervalComponent', 'n_intervals'),
    )
    def updateTrackMap(n):              
        frameFunctions.trackMapFrame()
        return globalVariables.trackMap
    
    # Update standings table
    # TODO Fix standings table
    @app.callback(
        Output('standingsTable', 'data'),
        Input('intervalComponent', 'n_intervals'),
        State('standingsTable', 'data'),
    )
    def updateStandingsTable(n):
        frameFunctions.positionFrames()
        print("updating standings")

    app.run_server()

if __name__ == "__main__":
    
    # Always to be run, determines season, event, drivers etc.
    # Determines which part of the app to run
    getSettings.getSessionSettings()
    getSettings.getFunctionality()
    
    # Placeholder for testing
    globalVariables.currentTime = globalVariables.startTime
    globalVariables.currentTime += datetime.timedelta(minutes=30)   
    
    # Check functionality
    if globalVariables.function == 1:
        api.getTelemetry()
        api.getLapData()
        api.helper.getLapTimings()
        helper.getLapStandings()
        helper.getCurrentLap()
        frameFunctions.positionFrames()
        
        startDashApp()
        
    elif globalVariables.function == 2:
        dataExporting.exportGeneralLapData(globalVariables.session, globalVariables.selectedDrivers)
    elif globalVariables.function == 0:
        # USE FOR AD-HOC TESTING, NOT FINAL
        api.getLapData()
        api.helper.getLapTimings()
        api.getTelemetry()        
        helper.getCurrentLap()
        
        helper.getLapStandings()
        
        frameFunctions.positionFrames()
    

    
    
    