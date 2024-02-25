# Finds a certain session to use
from imports import fastf1, os
from helper import getAllDrivers
from api import getSession
from animation import animateDrivers
from data import exportGeneralLapData


def mainGUI():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Command line "GUI" for getting a session and other settings
    print("WELCOME TO THE F1 VISUALIZER")
    year = int(input("Which years season would you like to use? "))
    
    print(f"Thank you, using the F1 {year} season")
    season = fastf1.get_event_schedule(year)
    
    print("The selected season has the following GPs:\n")
    for index, row in season.iterrows():
        print(f"{row['RoundNumber']:<5} {row['EventName']}")
        
    eventNumber = int(input("\nPlease use the round number to select an event: "))
    
    print(f"Thank you, using the F1 {year} season and event nr. {eventNumber}")
    session = getSession(year, eventNumber, "R")
    
    session.load()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("The following drivers took part in the session:\n")
    drivers = getAllDrivers(session)
    for i in drivers:
        print(i)
    
    print("\nTo select drivers, type one abbreviation at a time. When ready, press empty enter\nPress enter to select all drivers\n")
    
    selectedDrivers = []
    
    while True:
        userInput = input("Input: ")
        if userInput:
            selectedDrivers.append(userInput)
        else:
            break
    
    if not selectedDrivers:
        print(selectedDrivers)
        selectedDrivers = drivers
    
    print("Thank you, here are the selected drivers:\n")
    for i in selectedDrivers:
        print(i)
        
    print("To animate the session, press 1\nTo export the lap data, press 2")
    
    function = int(input("\nInput: "))
    
    if function == 1:
        animateDrivers(session,selectedDrivers)
    elif function == 2:
        exportGeneralLapData(session, selectedDrivers)
        
       
    

    