import pygame
import random
import Maze
class Player(pygame.sprite.Sprite):
    def __init__(self, cha_surf, loc_x=16.5, loc_y=16.5):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.hv = 32
        self.vv = 32
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(cha_surf, (0, 0), (0, 0, 50, 70))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.col = (int)(self.loc_x + 15.5) // 32 -1
        self.row = (int)(self.loc_y + 15.5) // 32 -1
        self.posses = {possess_trans: False,
                       possess_bomb:False,
                       possess_mine: False,
                       possess_conv:False,
                       possess_pass: False,
                       possess_trap:False
                       }
        self.pos= [possess_trans, possess_bomb, possess_mine, possess_conv, possess_pass, possess_trap]
        self.chance = 0

    def directMoveViaColRow(self, col, row):
        self.col = col
        self.row = row
        self.loc_x = (self.col +1) * 32 -15.5
        self.loc_y = (self.row +1) * 32 -15.5
    
    def directMoveViaLoc(self, loc_x, loc_y):
        self.col = (int)(loc_x + 15.5) // 32 -1
        self.row = (int)(loc_y + 15.5) // 32 -1
        self.loc_x = loc_x
        self.loc_y = loc_y

    def update(self, g, top, down, right, left):
        #  g 已经经过算法生成
        if top:
            if g.cell_at(self.row, self.col).north != None:
                if g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row-1, self.col)):
                    self.loc_y-=self.vv
                    self.row = (int)(self.loc_y + 15.5) // 32 -1
                    self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

        if down:
            if g.cell_at(self.row, self.col).south != None:
                if g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row +1, self.col)):
                    self.loc_y += self.vv
                    self.row = (int)(self.loc_y + 15.5) // 32 -1
                    self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

        if left:
            if g.cell_at(self.row, self.col).west != None:
                if g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row , self.col - 1 )):
                    self.loc_x -= self.hv
                    self.col = (int)(self.loc_x + 15.5) // 32 -1
                    self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

        if right:
            if g.cell_at(self.row, self.col).east != None:
                if g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row , self.col + 1)):
                    self.loc_x += self.hv
                    self.col = (int)(self.loc_x + 15.5) // 32 -1
                    self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))


    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def getGadget(self):
        if chance <= 3:
            a = random.randrange(6)
            self.pos[a] = True





    '''chances are that the randombox might contain nothing'''

class Randombox(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.gad_surf = pygame.image.load('sprites/道具/randombox.jpg').convert()
        self.image = pygame.Surface((40, 40))
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0] / 1.5), int(self.image.get_size()[1] / 1.5)))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.image.blit(self.gad_surf, (0, 0), (0, 0, self.gad_surf.get_rect().size[0], self.gad_surf.get_rect().size[1]))
        self.col = (int)(self.loc_x + 15.5) // 32 - 1
        self.row = (int)(self.loc_y + 15.5) // 32 - 1


    def directMoveViaLoc(self, loc_x, loc_y):
        self.col = (int)(loc_x + 15.5) // 32 - 1
        self.row = (int)(loc_y + 15.5) // 32 - 1
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

class Mine(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.gad_surf = pygame.image.load('sprites/道具/地雷.png').convert()
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey((255, 255, 255))
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 4167, 4167))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.col = (int)(self.loc_x + 15.5) // 32 - 1
        self.row = (int)(self.loc_y + 15.5) // 32 - 1

    def directMoveViaLoc(self, loc_x, loc_y):
        self.col = (int)(loc_x + 15.5) // 32 - 1
        self.row = (int)(loc_y + 15.5) // 32 - 1
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))




class Transporter(pygame.sprite.Sprite):
   
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.gad_surf = pygame.image.load('sprites/道具/传送.png').convert()
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey((255, 255, 255))
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 617, 655))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.col = (int)(self.loc_x + 15.5) // 32 - 1
        self.row = (int)(self.loc_y + 15.5) // 32 - 1

    def directMoveViaLoc(self, loc_x, loc_y):
        self.col = (int)(loc_x + 15.5) // 32 - 1
        self.row = (int)(loc_y + 15.5) // 32 - 1
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.gad_surf = pygame.image.load('sprites/道具/炸弹.png').convert()
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey((255, 255, 255))
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 500, 500))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.col = (int)(self.loc_x + 15.5) // 32 - 1
        self.row = (int)(self.loc_y + 15.5) // 32 - 1

    def directMoveViaLoc(self, loc_x, loc_y):
        self.col = (int)(loc_x + 15.5) // 32 - 1
        self.row = (int)(loc_y + 15.5) // 32 - 1
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

class Converse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.gad_surf = pygame.image.load('sprites/道具/反转.png').convert()
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey((255, 255, 255))
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 8000, 6747))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.col = (int)(self.loc_x + 15.5) // 32 - 1
        self.row = (int)(self.loc_y + 15.5) // 32 - 1

    def directMoveViaLoc(self, loc_x, loc_y):
        self.col = (int)(loc_x + 15.5) // 32 - 1
        self.row = (int)(loc_y + 15.5) // 32 - 1
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

class PassWall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.gad_surf = pygame.image.load('sprites/道具/墙.png').convert()
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey((255, 255, 255))
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 1600, 1600))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.col = (int)(self.loc_x + 15.5) // 32 - 1
        self.row = (int)(self.loc_y + 15.5) // 32 - 1

    def directMoveViaLoc(self, loc_x, loc_y):
        self.col = (int)(loc_x + 15.5) // 32 - 1
        self.row = (int)(loc_y + 15.5) // 32 - 1
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

class Trap(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.gad_surf = pygame.image.load('sprites/道具/炸弹.png').convert()
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey((255, 255, 255))
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 4167, 4167))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.col = (int)(self.loc_x + 15.5) // 32 - 1
        self.row = (int)(self.loc_y + 15.5) // 32 - 1

    def directMoveViaLoc(self, loc_x, loc_y):
        self.col = (int)(loc_x + 15.5) // 32 - 1
        self.row = (int)(loc_y + 15.5) // 32 - 1
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))


