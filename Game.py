
import pygame,sys
from classes import *
from process import *

pygame.init()

SCREENWIDTH, SCREENHEIGHT = 800, 600
screen = pygame.display.set_mode( (SCREENWIDTH, SCREENHEIGHT) )
clock = pygame.time.Clock() #object of Clock() class
FPS = 60 # Frames Per Second
img_goldfish = pygame.image.load("images/shark.png") #image to be loaded

fish = Fish(0,SCREENHEIGHT - 80, 201, 101,"images/shark.png")
shark = Shark(40, 100, 200, 101, "images/shark.png")

# -------------Main Program Loop-----------------------

while True:

    process(fish, FPS, total_frames)

#LOGIC
# Logic is movement, functions, etc
    fish.motion(SCREENWIDTH, SCREENHEIGHT)
    Shark.update_all(SCREENWIDTH, SCREENHEIGHT)
    
#LOGIC

#DRAW
    screen.fill((0,0,255))


    #screen.blit(img_goldfish, (100,100) ) # renders image on the screen at spot 100 X 100
    BaseClass.allsprites.draw(screen) # list of everything being drawn on the screen
    pygame.display.flip() #ensures everything is being drawn on the screen
#DRAW

    clock.tick(FPS)



  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
