import pygame, math
from random import randint


class BaseClass(pygame.sprite.Sprite):
	
	allsprites = pygame.sprite.Group()
	def __init__(self, x, y, image_string):
		
		pygame.sprite.Sprite.__init__(self)
		BaseClass.allsprites.add(self)

		self.image = pygame.image.load(image_string)
		self.image = pygame.transform.flip(self.image, True, False);
		
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		#self.width = width
		#self.height = height
		
	def destroy(self, ClassName):
		
		ClassName.List.remove(self)
		BaseClass.allsprites.remove(self)
		del self


class Fish(BaseClass):

	List = pygame.sprite.Group()
	
	
	def __init__(self, x, y,image_string):
		
		BaseClass.__init__(self, x, y, image_string)
		Fish.List.add(self)
		self.velx = 0
		self.vely = 5

	def motion(self, SCREENWIDTH, SCREENHEIGHT):

		predicted_locationx = self.rect.x + self.velx
		predicted_locationy = self.rect.y + self.vely

		if  predicted_locationx < 0:
			self.velx = 0
		elif predicted_locationx + self.rect.width > SCREENWIDTH:
			self.velx = 0
		if predicted_locationy < 0:
			self.vely = 0 
		elif predicted_locationy + self.rect.height > SCREENHEIGHT:
			self.vely = 0 

		self.rect.x += self.velx
		self.rect.y += self.vely
		
class Shark(BaseClass):

	List = pygame.sprite.Group()
	
	
	def __init__(self, x, y, image_string):
		
		if len(Shark.List) < 6:
			BaseClass.__init__(self, x, y, image_string)
			Shark.List.add(self)
			self.health = 100
			self.half_health = self.health ## / 2.0 will make it so you have to hit the shark twice in order to kill it
			self.velx, self.vely = randint(1, 4), 2
			self.amplitude, self.period = randint(20, 140), randint(4, 5)/ 100.0

	@staticmethod
	def update_all(SCREENWIDTH, SCREENHEIGHT):
		
		for sharks in Shark.List:

			if sharks.health <= 0: # if our shark is dead
				if sharks.rect.y + sharks.rect.height < SCREENHEIGHT: # check to see if it is still above the bottom 
					sharks.velx = 0 # if true it drops down
			else:
				sharks.sharks(SCREENWIDTH) # if false it continues to move.

			
			# if shark.health <= 0: #destorys the sharks if the health is less than or eaqual to zero
			# 	shark.destroy(Shark)

	def sharks(self, SCREENWIDTH):
		#Keeps the sharks from being dropped outside the screen
		if self.rect.x + self.rect.width > SCREENWIDTH or self.rect.x < 0:
			self.image = pygame.transform.flip(self.image, True, False)
			self.velx = -self.velx

		self.rect.x += self.velx

		#Sin couve is -- (a * sin( bx + c ) + y)

		#self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + 140

	# @staticmethod
	# def movement(SCREENWIDTH):
	# 	for sharks in Shark.List:
	# 		sharks.sharks(SCREENWIDTH)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	