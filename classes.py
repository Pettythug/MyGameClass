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
CREDITS = 4
INSTRUCTIONS = 5
START_SCREEN = 6
LEVEL = 1


previous_x = [0]
previous_y = 0


class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
        self.clock = pygame.time.Clock()  # object of Clock() class
        self.FPS = 24  # Frames Per Second
        self.total_frames = 0
        self.play_frames = 0
        self.background = pygame.image.load("images/background.jpg")
        self.fish = Fish(SCREENWIDTH - 180, SCREENHEIGHT - 500, "images/cartoon-goldfish.png")
        # self.volcano = Volcano(SCREENWIDTH, SCREENHEIGHT, "images/underwater_spout.png")

        self.init_game()

    # -------------Main Program Loop-----------------------

    def init_game(self):
        self.lives = 3
        self.kills = 0
        self.score = 0
        self.state = START_SCREEN
        self.flip_count = 0
        Button.Button1 = Button()
        Button.Button2 = Button()
        Button.back = Button()
        Button.credits = Button()
        Button.instructions = Button()


    def run(self):

        while True:
            process(self, self.fish, self.FPS, self.total_frames, self.play_frames)
            self.screen.blit(self.background, (0, 0))
            position = pygame.mouse.get_pos()

            if self.state == FISH_PLAYING:
                if LEVEL == 1 :
                    self.background = pygame.image.load("images/Level1-3.jpg")
                elif LEVEL >= 3 and LEVEL < 5:
                    self.background = pygame.image.load("images/Level3-5.jpg")
                elif LEVEL >= 5 and LEVEL <= 9:
                    self.background = pygame.image.load("images/Level5-9.jpg")
                elif LEVEL ==10:
                    self.background = pygame.image.load("images/Level10.jpg")

                self.fish.motion(self.fish, SCREENWIDTH, SCREENHEIGHT)
                Shark.update_all(SCREENWIDTH, SCREENHEIGHT)
                Bag.update_all(SCREENWIDTH, SCREENHEIGHT)
                Jellyfish.update_all(SCREENWIDTH, SCREENHEIGHT)
                Pellet.update_all(SCREENWIDTH, SCREENHEIGHT)
                spawn(self, self.FPS, self.total_frames)
                collisions(self)
                # jelly_collisions(self)
                BaseClass.allsprites.draw(self.screen)
                FishProjectile.List.draw(self.screen)
                FishProjectile.movement()
                # print self.score
                # show_cleanup(self, "%s" % (self.kills))
                # show_cleanup_left(self, "Cleanups to Next Level")
                show_level(self, "%s" % (LEVEL))
                show_lives(self, "Lives: ")
                show_level_text(self, "LEVEL: ")
                #create our fancy text renderer
                bigfont = pygame.font.Font(None, 60)
                white = 255, 255, 255
                renderer = TextProgress(bigfont, "Next Level", white, (40, 40, 40))
                text = renderer.render(0)
                progress = (self.kills/float(LEVEL+3)) * 120
                text = renderer.render(progress)
                self.screen.blit(text, (0, 0))

            elif self.state == FISH_IN_WATER:
                show_message(self, "PRESS the Button to START", 30, "MIDDLE")
                Button.Button1.update_display(self.screen, (107,142,35), (SCREENWIDTH - 200) / 2, (SCREENHEIGHT + 100) / 2 , 200,    50,    0,        "Try Again?", (255,255,255))

            elif self.state == START_SCREEN:
                show_message(self, "KOI", 200, "TOP_MIDDLE_TOP")
                Button.Button1.update_display(self.screen, (107,142,35), (SCREENWIDTH - 300) / 2, (SCREENHEIGHT) / 2 , 300,    75,    0,        "Start Game", (255,255,255))
                Button.instructions.update_display(self.screen, (100,149,237), (SCREENWIDTH - 450) / 2, (SCREENHEIGHT + 450) / 2, 200,    50,    0,        "Tutorial", (255,255,255))
                Button.credits.update_display(self.screen, (100,149,237), (SCREENWIDTH + 50) / 2, (SCREENHEIGHT + 450) / 2 , 200,    50,    0,        "Credits", (255,255,255))

            elif self.state == FISH_GAME_OVER:
                show_message(self, "GAME OVER",50, "MIDDLE")
                Button.Button1.update_display(self.screen, (230,52,35), (SCREENWIDTH - 200) / 2, (SCREENHEIGHT + 100) / 2 , 200,    50,    0,        "Try Again?", (255,255,255))

            elif self.state == CREDITS:
                show_message(self, "Team Ant Informatics 125" , 30,  "TOP_MIDDLE_CENTER")
                Button.back.update_display(self.screen, (102,205,170), (SCREENWIDTH - 200) / 2, (SCREENHEIGHT + 100) / 2 , 200,    50,    0,        "Back", (255,255,255))

            elif self.state == INSTRUCTIONS:
                show_message(self, "You Have 3 Lives", 30,"TOP_MIDDLE_TOP")
                show_message(self, "Destroy the Trash to Level Up", 30,"TOP_MIDDLE_TOP2")
                show_message(self, "Pick up Pebbles and CLICK to shoot them at Trash", 30,"TOP_MIDDLE_CENTER")
                show_message(self, "Reach Level 10 to win the game", 30,"TOP_MIDDLE_BOTTOM")
                Button.back.update_display(self.screen, (102,205,170), (SCREENWIDTH - 200) / 2, (SCREENHEIGHT + 100) / 2 , 200,    50,    0,        "Back", (255,255,255))

            elif LEVEL == 10:
                self.state = FISH_WON
                show_message(self, "YOU WON! PRESS ENTER TO PLAY AGAIN", 30, "BOTTOM_MIDDLE")
            # LOGIC
            # Logic is movement, functions, etc

            self.total_frames += 1
            # LOGIC
  


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

class TextProgress:
    def __init__(self, font, message, color, bgcolor):
        self.font = font
        self.message = message
        self.color = color
        self.bgcolor = bgcolor
        self.offcolor = [c^40 for c in color]
        self.notcolor = [c^0xFF for c in color]
        self.text = font.render(message, 0, (255,0,0), self.notcolor)
        self.text.set_colorkey(1)
        self.outline = self.textHollow(font, message, color)
        self.bar = pygame.Surface(self.text.get_size())
        self.bar.fill(self.offcolor)
        width, height = self.text.get_size()
        stripe = pygame.Rect(0, height/2, width, height/4)
        self.bar.fill(color, stripe)
        self.ratio = width / 100.0

    def textHollow(self, font, message, fontcolor):
        base = font.render(message, 0, fontcolor, self.notcolor)
        size = base.get_width() + 2, base.get_height() + 2
        img = pygame.Surface(size, 16)
        img.fill(self.notcolor)
        base.set_colorkey(0)
        img.blit(base, (0, 0))
        img.blit(base, (2, 0))
        img.blit(base, (0, 2))
        img.blit(base, (2, 2))
        base.set_colorkey(0)
        base.set_palette_at(1, self.notcolor)
        img.blit(base, (1, 1))
        img.set_colorkey(self.notcolor)
        return img

    def render(self, percent=50):
        surf = pygame.Surface(self.text.get_size())
        if percent < 100:
            surf.fill(self.bgcolor)
            surf.blit(self.bar, (0,0), (0, 0, percent*self.ratio, 100))
        else:
            surf.fill(self.color)
        surf.blit(self.text, (0,0))
        surf.blit(self.outline, (-1,-1))
        surf.set_colorkey(self.notcolor)
        return surf




class Button(BaseClass):
    def __init__(self):
        this = 1

    #Update the display and show the button
    def update_display(self, surface, color, x, y, length, height, width, text, text_color):
        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.create_button(surface, color, x, y, length, height, width, text, text_color)



    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):           
        for i in range(1,10):
            s = pygame.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)  
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


class Fish(BaseClass):
    List = pygame.sprite.Group()
    going_right = True
    freeze = True
    lives = 3
    pellets = 0


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

        if y + height > 0 and y < SCREENHEIGHT:
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

        if len(Shark.List) < (LEVEL/2) - 1:
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

        if len(Jellyfish.List) < LEVEL:
            BaseClass.__init__(self, x, y, image_string)
            Jellyfish.List.add(self)
            self.health = 100
            self.half_health = self.health / 2.0  # will make it so you have to hit the shark twice in order to kill it
            self.velx, self.vely = randint(2, 3), randint(2, 4)
            self.amplitude, self.period = randint(20, 140), randint(4, 5) / 100.0
            self.direction = 0

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
        if self.rect.x > 750: # if outside the right walls
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
            if self.direction == 0:
                self.direction = random.randint(0,1)
                if self.direction == 1:
                    self.vely = -self.vely

            self.rect.y += self.vely

        #Sin couve is -- (a * sin( bx + c ) + y)

        #self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + 140


    def destroy(self):
        Jellyfish.List.remove(self)
        # Jellyfish.normal_list.remove(self)
        del self

class Pellet(BaseClass):
    List = pygame.sprite.Group()

    def __init__(self, x, y, image_string):

        if len(Pellet.List) + Fish.pellets < 2:
            BaseClass.__init__(self, x, y, image_string)
            Pellet.List.add(self)
            self.health = 100
            self.velx, self.vely = randint(1, 2), randint(1, 5)
            self.amplitude, self.period = randint(20, 140), randint(4, 5) / 100.0

    @staticmethod
    def update_all(SCREENWIDTH, SCREENHEIGHT):

        for pellets in Pellet.List:

            if pellets.health <= 0:  # if our shark is dead
                if pellets.rect.y + pellets.rect.height < SCREENHEIGHT:  # check to see if it is still above the bottom
                    pellets.velx = 0  # if true it drops down
            else:
                pellets.pellets(SCREENWIDTH, SCREENHEIGHT)  # if false it continues to move.


                # if shark.health <= 0: #destorys the sharks if the health is less than or eaqual to zero
                # shark.destroy(Shark)

    def pellets(self, SCREENWIDTH, SCREENHEIGHT):
        # Keeps the jellies from being dropped outside the screen
        if self.rect.y + self.rect.height > SCREENHEIGHT or self.rect.y < 0:
            self.vely = 0

        if self.rect.y != SCREENHEIGHT:
            self.rect.y += self.vely


    def destroy(self):
        Pellet.List.remove(self)
        # Shark.normal_list.remove(self)
        del self


class Bag(BaseClass):
    List = pygame.sprite.Group()

    def __init__(self, x, y, image_string):

        if len(Bag.List) < 3:
            BaseClass.__init__(self, x, y, image_string)
            Bag.List.add(self)
            self.health = 100
            self.half_health = self.health / 1.0  # will make it so you have to hit the shark twice in order to kill it
            self.velx, self.vely = randint(1, 2), randint(1, 5)
            self.amplitude, self.period = randint(20, 140), randint(4, 5) / 100.0

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
        if self.rect.y + self.rect.height > SCREENHEIGHT or self.rect.y < 0:
            self.vely = -self.vely

        self.rect.y += self.vely

    def destroy(self):
        Bag.List.remove(self)
        # Shark.normal_list.remove(self)
        del self


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

            if difference < self.width * 8:
                return

        except Exception:
            pass

        FishProjectile.normal_list.append(self)
        FishProjectile.List.add(self)
        self.velx = None
        Fish.pellets -= 1

    @staticmethod
    def movement():
        for projectile in FishProjectile.List:
            projectile.rect.x += projectile.velx

    def destroy(self):
        FishProjectile.List.remove(self)
        FishProjectile.normal_list.remove(self)
        del self


def show_message(self, message, font_size, location):
    self.font = pygame.font.Font(None, font_size)
    size = self.font.size(message)
    font_surface = self.font.render(message, False, (255, 255, 255))
    if location == "TOP_MIDDLE_TOP":
        x = (SCREENWIDTH - size[0]) / 2
        y = (SCREENHEIGHT/4) - 50
    elif location == "TOP_MIDDLE_TOP2":
        x = (SCREENWIDTH - size[0]) / 2
        y = (SCREENHEIGHT/4) - 10
    elif location == "TOP_MIDDLE_CENTER":
        x = (SCREENWIDTH - size[0]) / 2
        y = (SCREENHEIGHT/4) + 30
    elif location == "TOP_MIDDLE_BOTTOM":
        x = (SCREENWIDTH - size[0]) / 2
        y = (SCREENHEIGHT/4) + 70

    elif location == "MIDDLE":
        x = (SCREENWIDTH - size[0]) / 2
        y = (SCREENHEIGHT - size[1]) / 2 
    elif location == "BOTTOM_MIDDLE":
        x = (SCREENWIDTH - size[0]) / 2
        y = (SCREENHEIGHT - (size[1] * 2))
    elif location == "BOTTOM_LEFT":
        x = (SCREENWIDTH - size[0]) / 3
        y = (SCREENHEIGHT - size[1] ) / 2 
    elif location == "BOTTOM_RIGHT":
        x = (SCREENWIDTH - size[0])
        y = (SCREENHEIGHT - size[1] ) / 2 
    self.screen.blit(font_surface, (x, y))

def show_lives(self, message):
    self.font = pygame.font.Font(None, 30)
    size = self.font.size(message)
    font_surface = self.font.render(message, False, (255, 255, 255))
    x = 15
    y = 15
    self.screen.blit(font_surface, ((SCREENWIDTH/2) - 30, y))
    i = 1
    while i < self.lives+1:
        self.screen.blit(pygame.image.load("images/lives.png"), ((i * 50 + (SCREENWIDTH/2), y)))
        i += 1
def show_cleanup(self, message):
    self.font = pygame.font.Font(None, 30)
    size = self.font.size(message)
    font_surface = self.font.render(message, False, (255, 255, 255))
    x = 15
    y = 15
    self.screen.blit(font_surface, ((SCREENWIDTH / 2)+30, y+30))

def show_cleanup_left(self, message):
    self.font = pygame.font.Font(None, 20)
    size = self.font.size(message)
    font_surface = self.font.render(message, False, (255, 255, 255))
    x = 15
    y = 15
    self.screen.blit(font_surface, ((SCREENWIDTH/2) - 30, y))

def show_level(self, message):
    self.font = pygame.font.Font(None, 50)
    size = self.font.size(message)
    font_surface = self.font.render(message, False, (255, 255, 255))
    y = 15
    self.screen.blit(font_surface, (SCREENWIDTH - 100, y + 30))
def show_level_text(self, message):
    self.font = pygame.font.Font(None, 30)
    size = self.font.size(message)
    font_surface = self.font.render(message, False, (255, 255, 255))
    y = 15
    self.screen.blit(font_surface, (SCREENWIDTH - 100, y))

