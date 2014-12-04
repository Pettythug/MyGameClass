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

        if keys[pygame.K_RETURN] and self.state == classes.FISH_IN_WATER:
            self.state = classes.FISH_PLAYING

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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

        if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[2]:
            def direction():
                if classes.Fish.going_right:
                    p.velx = 8
                else:
                    p.image = pygame.transform.flip(p.image, True, False)  # flips the image when shooting the other direction
                    p.velx = -8

            if classes.Fish.going_right:
                p = classes.FishProjectile(fish.rect.x, fish.rect.y, classes.Fish.going_right, "images/green_pebble.png")
                direction()
            else:
                p = classes.FishProjectile(fish.rect.x, fish.rect.y, classes.Fish.going_right, "images/green_pebble.png")
                direction()


    # spawn(self, FPS, total_frames)
    # collisions(self)
    classes.projectile_collisions()



def spawn(self, FPS, total_frames):
    image_shark = "images/shark2.png"
    img = Image.open(image_shark)
    # get the image's width and height in pixels
    width, height = img.size
    sixty_seconds = FPS * 5  # spawns a new shark every 4 seconds

    if total_frames % sixty_seconds == 0:

        r = random.randint(1, 3)
        y = 1
        if r == 2:
            y = 600 - height
        elif r == 3:
            y = 600 / 2 - height / 2
        classes.Shark(0, y, image_shark)


    r = random.randint(1, 3)
    if r == 1: 
        image_jelly = "images/bag.png"
    elif r == 2:
        image_jelly = "images/jelly.png"
    elif r == 3:
        image_jelly = "images/can.png"
    img = Image.open(image_jelly)

    if total_frames % (FPS * 2.5)  == 0:

        r = random.randint(1, 3)
        if r == 1: 
            x = random.randint(1, 450)
            y = 0
            self.velx, self.vely = 0,0
        elif r == 2:
            x = 0
            y = random.randint(1, 450)
        elif r == 3:
            x = 0
            y = random.randint(1, 200)
        classes.Jellyfish(x, y, image_jelly)

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
                classes.Shark.remove(sharks)
                for num in classes.Shark.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Shark.destroy(num)
                classes.Fish.destroy(fish)


                if self.lives > 0:
                    self.fish = classes.Fish(0, classes.SCREENHEIGHT - 80, "images/cartoon-goldfish.png")
                    self.state = classes.FISH_IN_WATER
                else : self.state = classes.FISH_GAME_OVER

def jelly_collisions(self):
    #  Freeze jellyfishes
    #  widthpx projectiles

    for fish in classes.Fish.List:

        for jellyfishes in classes.Jellyfish.List:

            col = fish.rect.colliderect(jellyfishes.rect)

            if col:
                self.lives -= 1
                classes.Fish.remove(fish)
                classes.BaseClass.allsprites.remove(fish)
                classes.Jellyfish.remove(jellyfishes)
                for num in classes.Jellyfish.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Jellyfish.destroy(num)
                classes.Fish.destroy(fish)


                if self.lives > 0:
                    self.fish = classes.Fish(0, classes.SCREENHEIGHT - 80, "images/cartoon-goldfish.png")
                    self.state = classes.FISH_IN_WATER
                else : self.state = classes.FISH_GAME_OVER

def projectile_collisions():

    for enemies in classes.Shark.List:

        projectiles = pygame.sprite.spritecollide(enemies, classes.FishProjectile.List, True) # when a player projectile collides with a enemy it returns the projectiles in the projectiles list

        for projectile in projectiles:


            enemies.health -= enemies.half_health
            enemies.image = pygame.image.load("images/shark3.png") # changed shark

            if enemies.health == 0:
                classes.BaseClass.allsprites.remove(enemies)
                classes.Shark.destroy(enemies)


            projectile.rect.x = 2 * -projectile.rect.width
            projectile.destroy()
        # PROCESSING









