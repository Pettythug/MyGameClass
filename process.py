import pygame, sys, classes, random
from PIL import Image
import Game


def process(self, fish, FPS, total_frames):
    # PROCESSING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.state == classes.FISH_IN_WATER:
            self.state = classes.FISH_PLAYING

        elif keys[pygame.K_RIGHT]:
            fish.image = pygame.image.load("images/cartoon-goldfish.png")
            fish.velx = 5
        elif keys[pygame.K_LEFT]:
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




    spawn(self, FPS, total_frames)
    collisions(self)



def spawn(self, FPS, total_frames):
    image_shark = "images/shark2.png"
    img = Image.open(image_shark)
    # get the image's width and height in pixels
    width, height = img.size
    sixty_seconds = FPS * 15  # spawns a new shark every sixty seconds

    if total_frames % sixty_seconds == 0:


        r = random.randint(1, 3)
        x = 1
        y = 1
        if r == 2:
            x = 800 - 200
            y = 600 - height
        elif r == 3:
            x = 0
            y = 600 / 2 - height / 2
        classes.Shark(x, y, image_shark)


def collisions(self):
    #  Freeze sharks
    #  widthpx projectiles

    for fish in classes.Fish.List:

        for sharks in classes.Shark.List:

            col = fish.rect.colliderect(sharks.rect)

            if col:
                self.lives -= 1
                classes.Fish.remove(fish)
                classes.BaseClass.allsprites.remove(fish)
                self.fish = classes.Fish(0, classes.SCREENHEIGHT - 80, "images/cartoon-goldfish.png")
                if self.lives > 0:
                    self.state = classes.FISH_IN_WATER



def handle_collisions(self):
        for fish in classes.Fish.List:
            for sharks in classes.Shark.List:
                if self.fish.rect.colliderect(sharks.rect):
                    self.lives -= 1
                    classes.Fish.remove(fish)
                    break
            if self.lives > 0:
                self.state = classes.FISH_IN_WATER
            else:
                self.state = classes.FISH_GAME_OVER

        if len(classes.Shark.List) == 0:
            self.state = classes.FISH_WON




        # PROCESSING









