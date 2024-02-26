# Here are global variables for use in the whole app

# IMPORTANT - Determines the "live" feed of the app 
currentTime = None

# The following settings are taken from the getSessionSettings function and should not be generated elsewhere
year = None
season = None
eventN = None
event = None
sessionType = None
session = None
drivers = None
selectedDrivers = []

# The following variables determine the "part" of the app to use, generated from getFunctionality
function = None

# The following objects are the figures available (px or go object for use in Dash)
trackMap = None
figure2 = None
figure3 = None