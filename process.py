import pygame, sys, classes, random
from PIL import Image
import Game
from random import randint
global PELLETS


def process(self, fish, FPS, total_frames, play_frames):
    # PROCESSING

                   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()


        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == classes.START_SCREEN:
                if classes.Button.instructions.pressed(pygame.mouse.get_pos()):
                    self.state = classes.INSTRUCTIONS
                    pygame.mixer.music.load('music/blop.ogg')
                    pygame.mixer.music.play(0)
                elif classes.Button.credits.pressed(pygame.mouse.get_pos()):
                    self.state = classes.CREDITS
                    pygame.mixer.music.load('music/blop.ogg')
                    pygame.mixer.music.play(0)
                elif classes.Button.Button1.pressed(pygame.mouse.get_pos()):
                    pygame.mixer.music.load('music/bubbles.ogg')
                    pygame.mixer.music.play(0)
                    self.state = classes.FISH_PLAYING
            elif self.state == classes.INSTRUCTIONS or self.state == classes.CREDITS:
                if classes.Button.back.pressed(pygame.mouse.get_pos()):
                    self.state = classes.START_SCREEN
                    pygame.mixer.music.load('music/blop.ogg')
                    pygame.mixer.music.play(0)
            elif self.state == classes.FISH_IN_WATER:
                self.play_frames = 0
                if classes.Button.Button1.pressed(pygame.mouse.get_pos()):
                    self.state = classes.FISH_PLAYING
                    pygame.mixer.music.load('music/blop.ogg')
                    pygame.mixer.music.play(0)
            elif self.state == classes.FISH_GAME_OVER :
                if classes.Button.Button1.pressed(pygame.mouse.get_pos()):
                    pygame.mixer.music.load('music/bubbles.ogg')
                    pygame.mixer.music.play(0)
                    self.state = classes.FISH_PLAYING
                    self.score = 0
                    self.flip_count = 0
                    self.total_frames = 0
                    self.play_frames = 0
                    self.lives = 3
                    classes.LEVEL = 1
                    self.fish = classes.Fish(0, 520, "images/cartoon-goldfish.png")
        elif keys[pygame.K_RETURN] and self.state == classes.FISH_WON:
            self.state = classes.FISH_PLAYING
            self.score = 0
            self.flip_count = 0
            self.lives = 3
            self.total_frames = 0

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

        if self.state == classes.FISH_PLAYING:
            self.play_frames +=1
            if self.play_frames > 3: # so that clicking the start button doesn't also fire a pebble
                if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[1] or pygame.mouse.get_pressed()[2]:
                    def direction():
                        if classes.Fish.going_right:
                            p.velx = 8
                        else:
                            p.image = pygame.transform.flip(p.image, True, False)  # flips the image when shooting the other direction
                            p.velx = -8
                    if classes.Fish.pellets > 0:
                        r = random.randint(0,4)
                        if r == 1:
                            pebble_img = "images/pebble1.png"
                        elif r == 2:
                            pebble_img = "images/pebble2.png"
                        elif r == 3:
                            pebble_img = "images/pebble3.png"
                        elif r== 4:
                            pebble_img = "images/pebble4.png"
                        else:
                            pebble_img = "images/pebble.png"
                        p = classes.FishProjectile(fish.rect.x, fish.rect.y, classes.Fish.going_right, pebble_img)
                        direction()                        
                        pygame.mixer.music.load('music/fire.ogg')
                        pygame.mixer.music.play(0)

                

    # spawn(self, FPS, total_frames)
    # collisions(self)
    classes.projectile_collisions(self)



def spawn(self, FPS, total_frames):
    LEVEL = classes.LEVEL
    if total_frames % (FPS * (LEVEL - (LEVEL / 2))) == 0:  # spawns a new shark every 4 seconds
        image_shark = "images/shark2.png"
        img = Image.open(image_shark)
        r = random.randint(1, 3)
        y = 1
        if r == 2:
            y = 600 - 74
        elif r == 3:
            y = 600 / 2 - 150 / 2
        classes.Shark(0, y, image_shark)

    if total_frames % (FPS * (LEVEL - (LEVEL / 2))) == 0:  # spawns a new jelly every 2 seconds

        image_bag = "images/jelly.png"
        img = Image.open(image_bag)
        if random.randint(1, 2) == 1:
            x = 0
        else:
            x = 800
        y = random.randint(100, 450)
        classes.Jellyfish(x, y, image_bag)


    if total_frames % (FPS * 5)  == 0:  # spawns a new bag every 8 seconds
        r = random.randint(1, 3)

        y = 0
        if r == 1:
            if random.randint(1, 2) == 1:
                image_bag = "images/bag.png"
            else:
                image_bag = "images/trashbag.png"

        elif r == 2:
            image_bag = "images/can.png"

        elif r == 3:
            image_bag = "images/can.png"

        img = Image.open(image_bag)
        width, height = img.size
        x = random.randint(0, classes.SCREENWIDTH - width)
        classes.Bag(x, y, image_bag)
    
    if total_frames % (FPS * 5)  == 0:  # spawns a new Pellet every 6 seconds
        r = random.randint(1, 3)

        y = 0
        if r == 1:
            if random.randint(1, 2) == 1:
                image_pellet = "images/pebble1.png"
            else:
                image_pellet = "images/pebble2.png"

        elif r == 2:
            image_pellet = "images/pebble3.png"

        elif r == 3:
            image_pellet = "images/pebble4.png"

        img = Image.open(image_pellet)
        width, height = img.size
        x = random.randint(0, classes.SCREENWIDTH - width)
        classes.Pellet(x, y, image_pellet)
        

def collisions(self):
    #  Freeze sharks
    #  widthpx projectiles

    for fish in classes.Fish.List:

        for sharks in classes.Shark.List:

            col = fish.rect.colliderect(sharks.rect)

            if col:
                pygame.mixer.music.load('music/slap.ogg')
                pygame.mixer.music.play(0)
                self.lives -= 1
                classes.Fish.remove(fish)
                classes.BaseClass.allsprites.remove(fish)
                classes.Shark.remove(sharks)
                for num in classes.Jellyfish.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Jellyfish.destroy(num)
                for num in classes.Shark.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Shark.destroy(num)
                for num in classes.Bag.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Bag.destroy(num)
                for num in classes.Pellet.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Pellet.destroy(num)
                classes.Fish.destroy(fish)


                if self.lives == 3:
                     x = 0
                elif self.lives > 0:
                    self.fish = classes.Fish(0, classes.SCREENHEIGHT - 80, "images/cartoon-goldfish.png")
                    self.state = classes.FISH_IN_WATER
                else : 
                    self.state = classes.FISH_GAME_OVER
                    pygame.mixer.music.load('music/end.ogg')
                    pygame.mixer.music.play(0)

        for jellyfishes in classes.Jellyfish.List:

            col = fish.rect.colliderect(jellyfishes.rect)

            if col:
                pygame.mixer.music.load('music/slap.ogg')
                pygame.mixer.music.play(0)
                self.lives -= 1
                classes.Fish.remove(fish)
                classes.BaseClass.allsprites.remove(fish)
                classes.Jellyfish.remove(jellyfishes)
                for num in classes.Jellyfish.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Jellyfish.destroy(num)
                for num in classes.Shark.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Shark.destroy(num)
                for num in classes.Bag.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Bag.destroy(num)
                for num in classes.Pellet.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Pellet.destroy(num)
                classes.Fish.destroy(fish)

                if self.lives == 3:
                     x = 0
                elif self.lives > 0:
                    self.fish = classes.Fish(0, classes.SCREENHEIGHT - 80, "images/cartoon-goldfish.png")
                    self.state = classes.FISH_IN_WATER
                else : 
                    self.state = classes.FISH_GAME_OVER
                    pygame.mixer.music.load('music/end.ogg')
                    pygame.mixer.music.play(0)

        for bags in classes.Bag.List:

            col = fish.rect.colliderect(bags.rect)

            if col:
                pygame.mixer.music.load('music/slap.ogg')
                pygame.mixer.music.play(0)
                self.lives -= 1
                classes.Fish.remove(fish)
                classes.BaseClass.allsprites.remove(fish)
                classes.Bag.remove(bags)
                for num in classes.Jellyfish.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Jellyfish.destroy(num)
                for num in classes.Shark.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Shark.destroy(num)
                for num in classes.Bag.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Bag.destroy(num)
                for num in classes.Pellet.List:
                        classes.BaseClass.allsprites.remove(num)
                        classes.Pellet.destroy(num)
                classes.Fish.destroy(fish)

                if self.lives == 3:
                    self.lives == 3
                elif self.lives == 1 or self.lives == 2:
                    self.fish = classes.Fish(0, classes.SCREENHEIGHT - 80, "images/cartoon-goldfish.png")
                    self.state = classes.FISH_IN_WATER
                else: 
                    self.state = classes.FISH_GAME_OVER
                    pygame.mixer.music.load('music/end.ogg')
                    pygame.mixer.music.play(0)

        for pellet in classes.Pellet.List:

            col = fish.rect.colliderect(pellet.rect)

            if col:
                classes.Fish.pellets += 1
                classes.BaseClass.allsprites.remove(pellet)
                classes.Pellet.destroy(pellet)






def projectile_collisions(self):
    
    for enemies in classes.Bag.List:

        projectiles = pygame.sprite.spritecollide(enemies, classes.FishProjectile.List, True) # when a player projectile collides with a enemy it returns the projectiles in the projectiles list

        for projectile in projectiles:

            enemies.health -= enemies.half_health
            if enemies.health == 0:
                pygame.mixer.music.load('music/trumpet.ogg')
                pygame.mixer.music.play(0)
                # self.font = pygame.font.Font(None, 300)
                # size = self.font.size("2 POINTS")
                # font_surface = self.font.render("2 POINTS", False, (255, 255, 255))
                # self.screen.blit(font_surface, (enemies.rect.x, enemies.rect.y))
                classes.BaseClass.allsprites.remove(enemies)
                classes.Bag.destroy(enemies)
                self.kills += 1
                if self.kills > classes.LEVEL + 1:
                    classes.LEVEL += 1
                    self.kills = 0



            projectile.rect.x = 2 * -projectile.rect.width
            projectile.destroy()







