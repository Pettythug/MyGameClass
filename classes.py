from _ast import List
import pygame, math, sys
from random import randint
from process import *
from PIL import Image

SCREENWIDTH, SCREENHEIGHT = 800, 600

FISH_IN_WATER = 0
FISH_PLAYING = 1
FISH_WON = 2
FISH_GAME_OVER = 3
previous_x = [0]
previous_y = 0


class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
        self.clock = pygame.time.Clock()  # object of Clock() class
        self.FPS = 24  # Frames Per Second
        self.total_frames = 0
        self.background = pygame.image.load("images/background.jpg")
        self.fish = Fish(0, SCREENHEIGHT - 80, "images/cartoon-goldfish.png")
        # self.volcano = Volcano(SCREENWIDTH, SCREENHEIGHT, "images/underwater_spout.png")

        self.init_game()

    # -------------Main Program Loop-----------------------

    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = FISH_IN_WATER
        self.flip_count = 0


    def run(self):

        while True:
            process(self, self.fish, self.FPS, self.total_frames)
            self.screen.blit(self.background, (0, 0))
            position = pygame.mouse.get_pos()


            if self.state == FISH_PLAYING:
                self.fish.motion(self.fish, SCREENWIDTH, SCREENHEIGHT)
                Shark.update_all(SCREENWIDTH, SCREENHEIGHT)
                Bag.update_all(SCREENWIDTH, SCREENHEIGHT)
                Jellyfish.update_all(SCREENWIDTH, SCREENHEIGHT)
                spawn(self, self.FPS, self.total_frames)
                collisions(self)
                # jelly_collisions(self)
                BaseClass.allsprites.draw(self.screen)
                FishProjectile.List.draw(self.screen)
                FishProjectile.movement()
                self.score += 1

                # print self.score
                show_score(self, "%s" % (self.score/30))


            if self.state == FISH_IN_WATER:
                show_message(self, "PRESS Enter TO START")
            if self.state == FISH_GAME_OVER:
                show_message(self, "GAME OVER. Your score is %s" % (self.score/30))
            if self.state == FISH_WON:
                show_message(self, "YOU WON! PRESS ENTER TO PLAY AGAIN")
            # LOGIC
            # Logic is movement, functions, etc

            self.total_frames += 1
            # LOGIC

            # DRAW


            #screen.blit(img_goldfish, (100,100) ) # renders image on the screen at spot 100 X 100
            BaseClass.allsprites.draw(self.screen)  # list of everything being drawn on the screen
            pygame.display.flip()  # ensures everything is being drawn on the screen
            #DRAW

            self.clock.tick(self.FPS)

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

        # self.width = width
        #self.height = height

    def destroy(self, ClassName):
        ClassName.List.remove(self)
        BaseClass.allsprites.remove(self)
        del self


class Fish(BaseClass):
    List = pygame.sprite.Group()
    going_right = True
    freeze = True
    lives = 3

    def __init__(self, x, y, image_string):

        BaseClass.__init__(self, x, y, image_string)
        for i in range(3):
            Fish.List.add(self)
        self.velx = 0
        self.vely = 5

        self.health = 100
        self.half_health = self.health / 2.0  # will make it so you have to hit the shark twice in order to kill it

    def motion(self, fish, SCREENWIDTH, SCREENHEIGHT):

        # predicted_locationx = self.rect.x + self.velx
        # predicted_locationy = self.rect.y + self.vely
        #
        # if  predicted_locationx < 0:
        # self.velx = 0
        # elif predicted_locationx + self.rect.width > SCREENWIDTH:
        #     self.velx = 0
        # if predicted_locationy < 0:
        #     self.vely = 0
        # elif predicted_locationy + self.rect.height > SCREENHEIGHT:
        #     self.vely = 0
        #
        # self.rect.x += self.velx
        # self.rect.y += self.vely

        img = Image.open("images/cartoon-goldfish.png")
        width, height = img.size

        pos = pygame.mouse.get_pos()
        previous_x.append(pygame.mouse.get_rel()[0])

        x = pos[0]
        y = pos[1]

        if previous_x[0] > 1:
            fish.image = pygame.image.load("images/cartoon-goldfish.png")
            # print previous_x[0]
            previous_x.pop(0)
            Fish.going_right = True
        elif previous_x[0] < -1:
            fish.image = pygame.image.load("images/cartoon-goldfish-reverse.png")
            previous_x.pop(0)
            Fish.going_right = False
        else:
            previous_x.pop(0)

        if y + height > 0 and y + height < SCREENHEIGHT:
            self.rect.x = x - width / 2
            self.rect.y = y - height / 2


            # if y > height and x + width < SCREENWIDTH:
            #     self.rect.x = x
            #     self.rect.y = y - height

    def draw_fish(self):
        self.fish = Fish(0, SCREENHEIGHT - 80, "images/cartoon-goldfish.png")


    def destroy(self):
        Fish.List.remove(self)
        # fish.normal_list.remove(self)
        del self


class Shark(BaseClass):
    List = pygame.sprite.Group()
    going_right = True

    def __init__(self, x, y, image_string):

        if len(Shark.List) < 3:
            BaseClass.__init__(self, x, y, image_string)
            Shark.List.add(self)
            self.health = 100
            self.half_health = self.health / 2.0  # will make it so you have to hit the shark twice in order to kill it
            self.velx, self.vely = randint(3, 10), 200
            self.amplitude, self.period = randint(20, 140), randint(4, 5) / 100.0
            self.flip_count = 0
            

    @staticmethod
    def update_all(SCREENWIDTH, SCREENHEIGHT):

        for sharks in Shark.List:

            if sharks.health <= 0:  # if our shark is dead
                if sharks.rect.y + sharks.rect.height < SCREENHEIGHT:  # check to see if it is still above the bottom
                    sharks.velx = 0  # if true it drops down
            else:
                sharks.sharks(SCREENWIDTH, SCREENHEIGHT)  # if false it continues to move.


                # if shark.health <= 0: #destorys the sharks if the health is less than or eaqual to zero
                # shark.destroy(Shark)

    def sharks(self, SCREENWIDTH, SCREENHEIGHT):
        # Keeps the sharks from being dropped outside the screen
        if self.rect.x + self.rect.width > SCREENWIDTH or self.rect.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.velx = -self.velx
            if self.going_right:
                self.going_right = False
            else:
                self.going_right = True

        self.rect.x += self.velx

        #Sin couve is -- (a * sin( bx + c ) + y)
        #self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + 140

    def destroy(self):
        Shark.List.remove(self)
        # Shark.normal_list.remove(self)
        del self

class Jellyfish(BaseClass):
    List = pygame.sprite.Group()

    def __init__(self, x, y, image_string):

        if len(Jellyfish.List) < 8:
            BaseClass.__init__(self, x, y, image_string)
            Jellyfish.List.add(self)
            self.health = 100
            self.half_health = self.health / 2.0  # will make it so you have to hit the shark twice in order to kill it
            self.velx, self.vely = randint(2, 3), randint(2, 4)
            self.amplitude, self.period = randint(20, 140), randint(4, 5) / 100.0

    @staticmethod
    def update_all(SCREENWIDTH, SCREENHEIGHT):

        for jellyfishes in Jellyfish.List:

            if jellyfishes.health <= 0:  # if our shark is dead
                if jellyfishes.rect.y + jellyfishes.rect.height < SCREENHEIGHT:  # check to see if it is still above the bottom
                    jellyfishes.velx = 0  # if true it drops down
            else:
                jellyfishes.jellyfishes(SCREENWIDTH, SCREENHEIGHT)  # if false it continues to move.


                # if shark.health <= 0: #destorys the sharks if the health is less than or eaqual to zero
                # shark.destroy(Shark)

    def jellyfishes(self, SCREENWIDTH, SCREENHEIGHT):
        # Keeps the jellies from being dropped outside the screen
        if self.rect.x > 800: # if outside the right walls
            self.velx = -self.velx
            self.destroy()
            classes.BaseClass.allsprites.remove(self)
        elif self.rect.x < 0: # if outside the left walls
            self.velx = -self.velx
            self.destroy()
            classes.BaseClass.allsprites.remove(self)
        else:
            if self.rect.y + self.rect.height > SCREENHEIGHT:# if outside the bottom wall
                self.vely = -self.vely
            if self.rect.y - self.rect.height < 0: # if outside the top wall
                self.vely = -self.vely
            self.rect.x += self.velx
            if random.randint(1, 2) == 1:
                self.rect.y += .5
            else:
                self.rect.y -= .75

        #Sin couve is -- (a * sin( bx + c ) + y)

        #self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + 140


    def destroy(self):
        Jellyfish.List.remove(self)
        # Jellyfish.normal_list.remove(self)
        del self


class Bag(BaseClass):
    List = pygame.sprite.Group()

    def __init__(self, x, y, image_string):

        if len(Bag.List) < 4:
            BaseClass.__init__(self, x, y, image_string)
            Bag.List.add(self)
            self.health = 100
            self.half_health = self.health / 2.0  # will make it so you have to hit the shark twice in order to kill it
            self.velx, self.vely = randint(1, 2), randint(1, 2)
            self.amplitude, self.period = randint(20, 140), randint(4, 5) / 100.0
            self.direction = 0

    @staticmethod
    def update_all(SCREENWIDTH, SCREENHEIGHT):

        for bags in Bag.List:

            if bags.health <= 0:  # if our shark is dead
                if bags.rect.y + bags.rect.height < SCREENHEIGHT:  # check to see if it is still above the bottom
                    bags.velx = 0  # if true it drops down
            else:
                bags.bags(SCREENWIDTH, SCREENHEIGHT)  # if false it continues to move.


                # if shark.health <= 0: #destorys the sharks if the health is less than or eaqual to zero
                # shark.destroy(Shark)

    def bags(self, SCREENWIDTH, SCREENHEIGHT):
        # Keeps the jellies from being dropped outside the screen
        if self.rect.y + self.rect.height > 0: # if above top wall
            if self.direction == 0:
                if random.randint(0,1) ==1:
                    self.direction = 1
                else:
                    self.direction = -1
            self.rect.x += self.velx * self.direction
            if self.rect.y + self.rect.height > SCREENHEIGHT or self.rect.y + self.rect.height < 0: # if outside the bottom wall
                self.destroy()
                classes.BaseClass.allsprites.remove(self)
        else:
            self.rect.y -= self.vely

    def destroy(self):
        Bag.List.remove(self)
        # Shark.normal_list.remove(self)
        del self

class Volcano(BaseClass):
    image_volcano = "images/underwater_spout.png"
    img = Image.open(image_volcano)

    List = pygame.sprite.Group()

    def __init__(self, x, y, image_string):
        img = Image.open(image_string)
        width, height = img.size
        BaseClass.__init__(self, x - width, y - height, image_string)
        Volcano.List.add(self)


    def volcano(self, SCREENWIDTH):
        # Keeps the volcano from being dropped outside the screen
        if self.rect.x + self.rect.width > SCREENWIDTH or self.rect.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.velx = -self.velx

        self.rect.x += self.velx


class FishProjectile(pygame.sprite.Sprite):
    List = pygame.sprite.Group()
    normal_list = []
    freeze = True

    def __init__(self, x, y, going_right, image_string):

        pygame.sprite.Sprite.__init__(self)
        img = Image.open("images/cartoon-goldfish.png")
        width, height = img.size

        self.image = pygame.image.load(image_string)

        self.rect = self.image.get_rect()
        if going_right:
            self.rect.x = x + width
        else:
            self.rect.x = x
        self.rect.y = y + height / 2
        self.width = width
        self.height = height

        try:
            last_element = FishProjectile.normal_list[-1]
            difference = abs(self.rect.x - last_element.rect.x)

            if difference < self.width:
                return

        except Exception:
            pass

        FishProjectile.normal_list.append(self)
        FishProjectile.List.add(self)
        self.velx = None

    @staticmethod
    def movement():
        for projectile in FishProjectile.List:
            projectile.rect.x += projectile.velx

    def destroy(self):
        FishProjectile.List.remove(self)
        FishProjectile.normal_list.remove(self)
        del self


def show_message(self, message):
    self.font = pygame.font.Font(None, 30)
    size = self.font.size(message)
    font_surface = self.font.render(message, False, (255, 255, 255))
    x = (SCREENWIDTH - size[0]) / 2
    y = (SCREENHEIGHT - size[1]) / 2
    self.screen.blit(font_surface, (x, y))

def show_score(self, message):
    self.font = pygame.font.Font(None, 100)
    size = self.font.size(message)
    font_surface = self.font.render(message, False, (255, 255, 255))
    x = 15
    y = 15
    self.screen.blit(font_surface, (x, y))
    i = 1
    while i < self.lives+1:
        self.screen.blit(pygame.image.load("images/lives.png"), (i * 50 + 100, y))
        i += 1











