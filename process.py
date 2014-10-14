import pygame, sys

def process(fish,  FPS, total_frames): 
	
	# PROCESSING 
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			pygame.quit() 
			sys.exit() 
		keys = pygame.key.get_pressed() 
		if keys[pygame.K_RIGHT]: 
			fish.image = pygame.image.load("images/shark.png") 
			fish.velx = 5 
		elif keys[pygame.K_LEFT]:
			fish.image = pygame.image.load("images/shark.png") 
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

	sixty_seconds = FPS * 15 #spaws a new shark every sixty seconds

	if total_frames % sixty_seconds == 0:

	
		r = random.randint(1,2)
		x = 1
		if r == 2:
			x = 640 - 40
		classes.Sharks(x, 130, "images/shark.png")
		
	# PROCESSING
	
	
	
	
	
	
	
	
	
	