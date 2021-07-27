import pygame
import random
class Player(pygame.sprite.Sprite):
    def __init__(self, cha_surf):
        pygame.sprite.Sprite.__init__(self)
        '''self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False'''
        self.loc_x = 720
        self.loc_y = 360
        self.hv = 10
        self.vv = 10
        self.image = pygame.Surface((30, 60))
        self.image.set_colorkey((255, 255, 255))
        self.image.blit(cha_surf, (-5, -10), (0, 0, 430, 130))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))



    def update(self, size_x, size_y, top, down, right, left):

        if top:
            self.loc_y-=self.hv
        if down:
            self.loc_y+=self.hv
        if left:
            self.loc_x-=self.vv
        if right:
            self.loc_x+=self.vv

        '''if self.rect.top>size_y or self.rect.bottom<0 or self.rect.left>size_x or self.rect.right<0:
            self.kill()'''

    def draw(self, win_surf):
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

