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
        html.H1(children='Title of Dash App', style={'textAlign':'center'}),
        dcc.Graph(id='trackMap')
    ])

    @app.callback(
        Output('trackMap', 'figure'),
        Input('trackMap', 'id')
    )
    
    def update_track_map(_):      
        data = api.getTelemetryFiltered()
        
        trackMap = frameFunctions.plotTrackPositionsAtTime(data)

        return trackMap

    app.run_server()

if __name__ == "__main__":
    
    # Always to be run, determines season, event, drivers etc.
    # Determines which part of the app to run
    getSettings.getSessionSettings()
    getSettings.getFunctionality()
    
    globalVariables.currentTime = datetime.datetime(2021,5,23,14,43,4)
    
    if globalVariables.function == 1:
        startDashApp()
    elif globalVariables.function == 2:
        dataExporting.exportGeneralLapData(globalVariables.session, globalVariables.selectedDrivers)
    elif globalVariables.function == 0:
        # USE FOR AD-HOC TESTING, NOT FINAL
        
        data = api.getTelemetryFiltered()
        
        trackMap = frameFunctions.plotTrackPositionsAtTime(data)
        
        trackMap.show()
    
    
    
    
    
    
    
    
    
    
    