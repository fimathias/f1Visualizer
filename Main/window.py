from imports import animation, plt, np, os, pygame
import api
import helper
import track
from OpenGL.GL import glClear, glBegin, GL_QUADS, glEnd, glVertex2f, glFlush, glColor3f, GL_COLOR_BUFFER_BIT



def initWindow():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    windowSize = (1280, 800)
    pygame.display.set_mode(windowSize, pygame.DOUBLEBUF | pygame.OPENGL)
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break


        
        
        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_QUADS)

        glColor3f(0.0, 0.0, 1.0)  # Blue
        glVertex2f(-0.5, -0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, -0.5)
        
        glEnd()

        glFlush()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    
    
initWindow()