
import pygame,sys
from classes import *
from process import *

pygame.init()

SCREENWIDTH, SCREENHEIGHT = 800, 600
screen = pygame.display.set_mode( (SCREENWIDTH, SCREENHEIGHT),0,32 )
clock = pygame.time.Clock() #object of Clock() class
FPS = 24 # Frames Per Second
total_frames = 0
fish = Fish(0,SCREENHEIGHT - 80, "images/cartoon-goldfish.png")


# -------------Main Program Loop-----------------------

while True:

    process(fish,  FPS, total_frames)

#LOGIC
# Logic is movement, functions, etc
    fish.motion(SCREENWIDTH, SCREENHEIGHT)
    Shark.update_all(SCREENWIDTH, SCREENHEIGHT)
    total_frames += 1
#LOGIC

#DRAW
    screen.fill((0,0,255))


    #screen.blit(img_goldfish, (100,100) ) # renders image on the screen at spot 100 X 100
    BaseClass.allsprites.draw(screen) # list of everything being drawn on the screen
    pygame.display.flip() #ensures everything is being drawn on the screen
#DRAW

    clock.tick(FPS)



  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
