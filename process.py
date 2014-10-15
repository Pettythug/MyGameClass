import pygame, sys, classes, random
from PIL import Image

def process(fish,  FPS, total_frames): 
	
	# PROCESSING 
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			pygame.quit() 
			sys.exit() 
		keys = pygame.key.get_pressed() 
		if keys[pygame.K_RIGHT]: 
			classes.Fish.going_right = True
			fish.image = pygame.image.load("images/cartoon-goldfish.png") 
			fish.velx = 5 
		elif keys[pygame.K_LEFT]:
			classes.Fish.going_right = False
			fish.image = pygame.image.load("images/cartoon-goldfish-reverse.png") 
			fish.velx = -5 
		else: 
			fish.velx = 0 
			
		if keys[pygame.K_DOWN]: 			
			fish.vely = 5 
		elif keys[pygame.K_UP]:			
			fish.vely = -5 
		else: 
			fish.vely = 0 
			
	spawn(FPS, total_frames)
			
def spawn(FPS, total_frames):

	image_shark = "images/shark2.png"
	img = Image.open(image_shark)
	# get the image's width and height in pixels
	width, height = img.size
	sixty_seconds = FPS * 15 #spawns a new shark every sixty seconds

	if total_frames % sixty_seconds == 0:


	
		r = random.randint(1,3)
		x = 1
		y = 1
		if r == 2:
			x = 800 - 200
			y = 600 - height
		elif r == 3:
			x = 0
			y = 600 / 2 - height / 2
		classes.Shark(x, y, image_shark)
		
	# PROCESSING
	
	
	
	
	
	
	
	
	
	