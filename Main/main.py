import api
import track
import animation
import helper


if __name__ == "__main__":
       
    session = api.getSession(2021, "Monaco", 'R')
    
    animation.animateDrivers(session, ["TSU", "VER"])
    
    #circuit = track.trackCorners(session)
    
    #circuit.show()
    
    
    
    
    
    
    
    
    
    
    