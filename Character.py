import pygame
import random
class Player(pygame.sprite.Sprite):
    def __init__(self, cha_surf):
        pygame.sprite.Sprite.__init__(self)
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.loc_x = 20
        self.loc_y = 30
        self.hv = 5
        self.vv = 5


        self.surf = pygame.Surface((10,15))
        self.surf.blit(cha_surf, (0,0), (32, 32, 10, 15))
        self.rect = self.surf.get_rect()

        '''self.size_x = 30
        self.size_y = 40
        self.loc_x = pos_x
        self.loc_y = pos_y
        self.image = pygame.Surface((self.loc_x,self.loc_y))
        self.image.blit(image_surf, (0, 0), (4, 13, 29, 27))'''



    def update(self, size_x, size_y ):
        if self.move_left :
            self.rect.move_ip(-1,0)
        if self.move_right :
            self.rect.move_ip(1,0)
        if self.move_up:
            self.rect.move_ip(0,-1)
        if self.move_down:
            self.rect.move_ip(0,1)

        if self.rect.top>size_y or self.rect.bottom<0 or self.rect.left>size_x or self.rect.right<0:
            self.kill()








class Gadgets(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.appear = False
        self.size_x = 30
        self.size_y = 30

class Mine(Gadgets):
    '''if a mine is reached by a player, the player will be sent to somewhere adjacent'''
    def __init__(self):
        super().__init__()

class Transporter(Gadgets):
    '''if a transporter is reached by a player, '''
    def __init__(self):
        super().__init__()
class Bomb(Gadgets):
    def __init__(self):
        super().__init__()

class Shoes(Gadgets):
    def __init__(self):
        super().__init__()

class Converse(Gadgets):
    def __init__(self):
        super().__init__()

class PassWall(Gadgets):
    def __init__(self):
        super().__init__()

