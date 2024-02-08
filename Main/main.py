import api
import track
import animation
import helper
import opengl


if __name__ == "__main__":
       
    session = api.getSession(2021, "Monaco", 'R')
    
    opengl.animateDrivers(session)
        
    #animation.animateDrivers(session,["VER", "HAM", "TSU", "GAS", "LEC"])
    
    #circuit = track.trackCorners(session)
    
    #circuit.show()
    
    
    
    
    
    
    
    
    
    
    