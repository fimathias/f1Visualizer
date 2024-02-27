# This is for handling the api part of the code
from imports import fastf1, datetime, pd
import helper
import globalVariables


# Variables
currentDate = datetime.date.today()


def getFullSchedule(year: int):
    events = fastf1.get_event_schedule(year)
    
    return(events)

def getRemainingSchedule():
    events = fastf1.get_events_remaining()
    return(events)

def getEvent(year: int, gp):
    event = fastf1.get_event(year, gp)
    return event

def getSession(year: int, gp, session: str):
    session = fastf1.get_session(year, gp, session)    
    return session

def getNextEvent():
    currentSeason = currentDate.year
    
    remaining = getRemainingSchedule()
    nextGP = remaining["EventName"][0]
    nextEvent = getEvent(currentSeason, nextGP)
    
    return nextEvent
    
def getTelemetry():
    # Returns a telemetry object keyed with driver numbers and filtered with selected frequency
    data = {}
    for driver in globalVariables.selectedDrivers:
        driverN = helper.getDriverNumber(driver)
        data[driverN] = globalVariables.session.laps.pick_driver(driver).get_telemetry(frequency=1)
        
    globalVariables.telemetryData = data        
    
def getLapData():
    # Generates a object that has data on a lap per lap basis (positions, timings, sc etc.)
    globalVariables.session.load(laps=True)
    globalVariables.lapData = globalVariables.session.laps
    
def plotting():
    return fastf1.plotting