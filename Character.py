import pygame
import random
import Maze
class Player(pygame.sprite.Sprite):
    def __init__(self, cha_surf, loc_x=16.5, loc_y=16.5):
        pygame.sprite.Sprite.__init__(self)
        '''self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False'''

        self.loc_x = loc_x
        self.loc_y = loc_y
        self.hv = 32
        self.vv = 32
        self.image = pygame.Surface((32, 32))
        self.image.set_colorkey((255, 255, 255))
        self.image.blit(cha_surf, (-10, -10), (0, 0, 50, 70))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

        self.col = (int(self.loc_x * 2)-1) // 32
        self.row = (int(self.loc_y * 2)-1) // 32



    def update(self, g, top, down, right, left):
        #  g 已经经过算法生成
        if top:
            if g.cell_at(self.row, self.col).north != None:
                if g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row-1, self.col)):
                    self.loc_y-=self.vv
                    self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

        if down:
            if g.cell_at(self.row, self.col).south != None:
                if g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row +1, self.col)):
                    self.loc_y += self.vv
                    self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

        if left:
            if g.cell_at(self.row, self.col).west != None:
                if g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row , self.col - 1 )):
                    self.loc_x -= self.hv
                    self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

        if right:
            if g.cell_at(self.row, self.col).east != None:
                if g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row , self.col + 1)):
                    self.loc_x += self.hv
                    self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))





    '''def draw(self, win_surf):
        print("draw")
        pygame.draw.rect(win_surf, (0,0,0), self.rect)'''


















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

