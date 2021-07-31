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
        self.col = (int)(self.loc_x + 15.5) // 32 - 1
        self.row = (int)(self.loc_y + 15.5) // 32 - 1

        self.prop = 0
        self.prev_col = self.col
        self.prev_row = self.row
        self.cross_privilege = False
        self.teleporting = False
        self.teleport_col = self.col
        self.teleport_row = self.row

    def directMoveViaColRow(self, col, row):
        self.col = col
        self.row = row
        self.loc_x = (self.col + 1) * 32 - 15.5
        self.loc_y = (self.row + 1) * 32 - 15.5
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def directMoveViaLoc(self, loc_x, loc_y):
        self.col = (int)(loc_x + 15.5) // 32 - 1
        self.row = (int)(loc_y + 15.5) // 32 - 1
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def update(self, g, top, down, right, left, prop_use, markup):
        #  g 已经经过算法生成
        if top:
            if g.cell_at(self.row, self.col).north != None:
                if not self.teleporting and (self.cross_privilege or g.cell_at(self.row, self.col).is_linked(g.cell_at((int)(self.loc_y - self.vv + 15.5) // 32 - 1, self.col))):
                    self.prev_row = self.row
                    self.prev_col = self.col
                    self.loc_y -= self.vv
                    self.row = (int)(self.loc_y + 15.5) // 32 - 1
                    self.rect = self.image.get_rect(
                        center=(self.loc_x, self.loc_y))
                    self.cross_privilege = False
                elif self.teleporting and self.teleport_row > self.row-2:
                    self.teleport_row -= 1

        if down:
            if g.cell_at(self.row, self.col).south != None:
                if not self.teleporting and (self.cross_privilege or g.cell_at(self.row, self.col).is_linked(g.cell_at((int)(self.loc_y + self.vv + 15.5) // 32 - 1, self.col))):
                    self.prev_row = self.row
                    self.prev_col = self.col
                    self.loc_y += self.vv
                    self.row = (int)(self.loc_y + 15.5) // 32 - 1
                    self.rect = self.image.get_rect(
                        center=(self.loc_x, self.loc_y))
                    self.cross_privilege = False
                elif self.teleporting and self.teleport_row < self.row+2:
                    self.teleport_row += 1

        if left:
            if g.cell_at(self.row, self.col).west != None:
                if not self.teleporting and (self.cross_privilege or g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row, (int)(self.loc_x - self.hv + 15.5) // 32 - 1))):
                    self.prev_col = self.col
                    self.prev_row = self.row
                    self.loc_x -= self.hv
                    self.col = (int)(self.loc_x + 15.5) // 32 - 1
                    self.rect = self.image.get_rect(
                        center=(self.loc_x, self.loc_y))
                    self.cross_privilege = False
                elif self.teleporting and self.teleport_col > self.col-2:
                    self.teleport_col -= 1

        if right:
            if g.cell_at(self.row, self.col).east != None:
                if not self.teleporting and (self.cross_privilege or g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row, (int)(self.loc_x + self.hv + 15.5) // 32 - 1))):
                    self.prev_col = self.col
                    self.prev_row = self.row
                    self.loc_x += self.hv
                    self.col = (int)(self.loc_x + 15.5) // 32 - 1
                    self.rect = self.image.get_rect(
                        center=(self.loc_x, self.loc_y))
                    self.cross_privilege = False
                elif self.teleporting and self.teleport_col < self.col+2:
                    self.teleport_col += 1

        if prop_use:

            if self.prop == 1:
                # converse
                self.hv *= -1
                self.vv *= -1
                self.prop = 0
            elif self.prop == 2:
                # bomb
                markup.set_item_at(self.prev_row, self.prev_col, 'b')
                print("put bomb at", self.prev_row, self.prev_col)
                print("I am at", self.row, self.col)
                self.prop = 0
            elif self.prop == 3:
                # cross
                self.cross_privilege = True
                self.prop = 0
            elif self.prop == 4:
                # teleport
                if not self.teleporting:
                    self.teleporting = True
                    self.teleport_col = self.col
                    self.teleport_row = self.row
                    print("teleporting")
                else:
                    self.directMoveViaColRow(
                        self.teleport_col, self.teleport_row)
                    self.teleporting = False
                    print("teleport done")
                    self.prop = 0
            elif self.prop == 5:
                # long dist bomb
                if not self.teleporting:
                    self.teleporting = True
                    self.teleport_col = self.col
                    self.teleport_row = self.row
                    print("teleporting bomb")
                else:
                    markup.set_item_at(self.teleport_row,
                                       self.teleport_col, 'b')
                    self.teleporting = False
                    print("teleport bomb done")
                    self.prop = 0

    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def getGadget(self):
        self.prop = random.randint(1, 5)
        print("get prop", self.prop)


class Randombox(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.gad_surf = pygame.image.load('sprites/道具/randombox.jpg').convert()
        self.image = pygame.Surface((40, 40))
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (int(
            self.image.get_size()[0] / 1.5), int(self.image.get_size()[1] / 1.5)))
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))
        self.image.blit(self.gad_surf, (0, 0), (0, 0, self.gad_surf.get_rect(
        ).size[0], self.gad_surf.get_rect().size[1]))
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


class Prop(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey((255, 255, 255))
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


class Mine(Prop):
    def __init__(self):
        super().__init__()
        self.gad_surf = pygame.image.load('sprites/道具/地雷.png').convert()
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 4167, 4167))


class Transporter(Prop):
    def __init__(self):
        super().__init__()
        self.gad_surf = pygame.image.load('sprites/道具/传送.png').convert()
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 617, 655))


class Bomb(Prop):
    def __init__(self):
        super().__init__()
        self.gad_surf = pygame.image.load('sprites/道具/炸弹.png').convert()
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 500, 500))


class Converse(Prop):
    def __init__(self):
        super().__init__()
        self.gad_surf = pygame.image.load('sprites/道具/反转.png').convert()
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 8000, 6747))


class PassWall(Prop):
    def __init__(self):
        super().__init__()
        self.gad_surf = pygame.image.load('sprites/道具/墙.png').convert()
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 1600, 1600))


class Trap(Prop):
    def __init__(self):
        super().__init__()
        self.gad_surf = pygame.image.load('sprites/道具/炸弹.png').convert()
        self.image.blit(self.gad_surf, (0, 0), (0, 0, 4167, 4167))


class Land(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.image = pygame.Surface((20, 20))
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


class Ice(Land):

    def __init__(self):
        super().__init__()
        self.gad_surf = pygame.image.load('sprites/道具/冰.png').convert()
        self.image.blit(self.gad_surf, (0, 0), (0, 0, self.gad_surf.get_rect(
        ).size[0], self.gad_surf.get_rect().size[1]))


class Water(Land):

    def __init__(self):
        super().__init__()
        self.gad_surf = pygame.image.load('sprites/道具/水.jpg').convert()
        self.image.blit(self.gad_surf, (0, 0), (0, 0, self.gad_surf.get_rect(
        ).size[0], self.gad_surf.get_rect().size[1]))
