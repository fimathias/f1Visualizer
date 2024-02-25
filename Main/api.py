# This is for handling the api part of the code
from imports import fastf1, datetime, pd


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

def getTelemetry(session: str, driverN = None):
    if driverN is None:
        return session.pos_data
    else:
        return session.pos_data[driverN]
    
def getCarData(session: str, driverN = None):
    if driverN is None:
        return session.car_data
    else:
        return session.car_data[driverN]
    
def plotting():
    return fastf1.plotting