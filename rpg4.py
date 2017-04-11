import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
# Nazwy plikow png -------------------------------------------------------------------------------------------------------
heart = "heart.png"
flower = "flower.png"
tadeusz = "tadeusz.png"
mushroom = "mushroom.png"

pygame.init()
points = { 'zosia': 0, 'hrabia': 0, 'mushroom': 0}
score = 0
showme = ""
myfont = pygame.font.SysFont("Arial", 15)
class Character(pygame.sprite.Sprite):
    def __init__(self, name, x, y, pic , text):
        super().__init__()
        self.image = pygame.image.load(pic )
        self.name = name
        self.text = text

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# definicje postaci -------------------------------------------------------------------------------------------------------
hrabia =Character("hrabia",60,300,tadeusz,"jestem hrabia")
zosia = Character("zosia", 10, 200, heart, "jestem Zosia")


class Wall(pygame.sprite.Sprite):

    def __init__(self, name, x, y, pic):
        super().__init__()
        self.image = pygame.image.load(pic )
        self.name = name
        
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Player(pygame.sprite.Sprite):

    change_x = 0
    change_y = 0

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(tadeusz)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def move(self, walls, chars):

        global showme

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if block.name == "mushroom":
                showme = "you chose wisely"
                if points['mushroom']==0:
                    points['mushroom']=1
                    global score
                    score+=1
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
        #################################################################33
        char_hit_list = pygame.sprite.spritecollide(self, chars, False)
        for character in char_hit_list:
            showme = character.text
            if self.change_x > 0:
                self.rect.right = character.rect.left
            else:
                self.rect.left = character.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
        #########################################################################
        char_hit_list = pygame.sprite.spritecollide(self, chars, False)
        for character in char_hit_list:
            showme = character.text
            if self.change_y > 0:
                self.rect.bottom = character.rect.top
            else:
                self.rect.top = character.rect.bottom

class Room(object):
    """ Base class for all rooms. """
    wall_list = None
    char_list = None
    enemy_sprites = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.char_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


class Room1(Room):
    """ wszystko co jest w 1. pokoju"""

    def __init__(self):
        super().__init__()

        walls = [["a",50, 0, flower],
                 ["b",150, 250, flower],
                 ["c",250, 480, flower]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)
        ##############################################################3
        self.char_list.add(zosia)
        self.char_list.add(hrabia)


class Room2(Room):
    """wszystko w 2. pokoju"""

    def __init__(self):
        super().__init__()

        walls = [["d",0, 0, flower],
                 ["e",0, 350, flower],
                 ["f",780, 0, flower],
                 ["mushroom",680, 350, mushroom]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2],item[3])
            self.wall_list.add(wall)


class Room3(Room):
    """wszystko w 3. pokoju"""

    def __init__(self):
        super().__init__()

        #DO ZMIANY
        walls = [["h",200, 0, flower]
                 ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

def main():
    """ Main Program """
    #
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Nazwa')
    player = Player(50, 50)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    rooms = []

    room = Room1()
    rooms.append(room)

    room = Room2()
    rooms.append(room)

    room = Room3()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    clock = pygame.time.Clock()
    # --------------------------------------------------------------
    f = pygame.font.SysFont('Bevan', 70);
    t = f.render('GTA', True, (255, 255, 255));
    screen.fill(GREEN)
    screen.blit(t, (170, 120));
    pygame.display.update();
    pygame.time.wait(1100);
    #-------------------------------------------------------------------
    done = False

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            global showme
            if event.type == pygame.KEYDOWN:
                showme=""
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -5)

        # --- Game Logic ---

        player.move(current_room.wall_list, current_room.char_list)

        if player.rect.x < -15:
            if current_room_no == 0:
                current_room_no = 2
                current_room = rooms[current_room_no]
                player.rect.x = 790
            elif current_room_no == 2:
                current_room_no = 1
                current_room = rooms[current_room_no]
                player.rect.x = 790
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.x = 790

        if player.rect.x > 801:
            if current_room_no == 0:
                current_room_no = 1
                current_room = rooms[current_room_no]
                player.rect.x = 0
            elif current_room_no == 1:
                current_room_no = 2
                current_room = rooms[current_room_no]
                player.rect.x = 0
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.x = 0

        # --- Drawing on screen---
        screen.fill(WHITE)
        global score
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen) # wyswietlanie scian
        current_room.char_list.draw(screen) # wyswietlanie postaci
        label = myfont.render(showme, 1, (5, 5, 0))  # TEKST postaci
        screen.blit(label, (200, 100))
        points = myfont.render("Wynik: " + str(score), 1, (5, 5, 0)) # WYNIK
        screen.blit(points, (600,10))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
