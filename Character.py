import pygame
import random
class Player(pygame.sprite.Sprite):
    def __init__(self, cha_surf, loc_x=720, loc_y=360):
        pygame.sprite.Sprite.__init__(self)
        '''self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False'''

        self.loc_x = loc_x
        self.loc_y = loc_y
        self.hv = 10
        self.vv = 10
        self.image = pygame.Surface((20, 50))
        self.image.set_colorkey((255, 255, 255))
        self.image.blit(cha_surf, (-10, -10), (0, 0, 30, 70))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))



    def update(self, size_x, size_y, top, down, right, left):

        if top:
            self.loc_y-=self.hv
            self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        if down:
            self.loc_y+=self.hv
            self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        if left:
            self.loc_x-=self.vv
            self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        if right:
            self.loc_x+=self.vv
            self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))





    def draw(self, win_surf):
        print("draw")
        pygame.draw.rect(win_surf, (0,0,0), self.rect)


















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

