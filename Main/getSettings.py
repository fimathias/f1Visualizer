# Finds a certain session to use
from imports import fastf1, os, datetime, px
from helper import getAllDrivers
from api import getEvent, getSession, getTelemetryFiltered
from dataExporting import exportGeneralLapData
from frameFunctions import getTelemetryAtTime, trackMapFrame
import globalVariables


def getSessionSettings():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Command line "GUI" for getting a session and other settings
    print("WELCOME TO THE F1 VISUALIZER")
    globalVariables.year = int(input("Which years season would you like to use? "))
    
    print(f"Thank you, using the F1 {globalVariables.year} season")
    globalVariables.season = fastf1.get_event_schedule(globalVariables.year)
    
    print("The selected season has the following GPs:\n")
    for index, row in globalVariables.season.iterrows():
        print(f"{row['RoundNumber']:<5} {row['EventName']}")
        
    globalVariables.eventN = int(input("\nPlease use the round number to select an event: "))
    globalVariables.event = getEvent(globalVariables.year, globalVariables.eventN)
    
    print(f"Thank you, using the F1 {globalVariables.year} season and event nr. {globalVariables.eventN}")
    globalVariables.session = getSession(globalVariables.year, globalVariables.eventN, "R")
    
    globalVariables.session.load()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    globalVariables.startTime = globalVariables.season['Session5DateUtc'][globalVariables.eventN]
    print(f"The selected event took part at \n{globalVariables.startTime}")
    
    print("The following drivers took part in the session:\n")
    globalVariables.drivers = getAllDrivers(globalVariables.session)
    for i in globalVariables.drivers:
        print(i)
    
    print("\nTo select drivers, type one abbreviation at a time. When ready, press empty enter\nPress enter to select all drivers\n")
    
    while True:
        userInput = input("Input: ")
        if userInput:
            globalVariables.selectedDrivers.append(userInput)
        else:
            break
    
    
    if not globalVariables.selectedDrivers:
        globalVariables.selectedDrivers = globalVariables.drivers
    
    print("\nThank you, here are the selected drivers:\n")
    for i in globalVariables.selectedDrivers:
        print(i)
    
    
def getFunctionality():    
    print("\nWIP! To launch Dashboard, press 1\nTo export the lap data, press 2\n\nFor testing, press 0")
    
    globalVariables.function = int(input("\nInput: "))
    

    