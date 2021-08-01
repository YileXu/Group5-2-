import pygame
import random
import threading
import time
import ctypes


class Player(pygame.sprite.Sprite):
    def __init__(self, name, cha_surf, loc_x=16.5, loc_y=16.5):
        pygame.sprite.Sprite.__init__(self)
        self.name = name

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

        self.trap = False
        self.auto_walk_dir = None

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
                if not self.teleporting and not self.trap and (self.cross_privilege or g.cell_at(self.row, self.col).is_linked(g.cell_at((int)(self.loc_y - self.vv + 15.5) // 32 - 1, self.col))):
                    self.auto_walk_dir = 'top'
                    self.prev_row = self.row
                    self.prev_col = self.col
                    self.loc_y -= self.vv
                    self.row = (int)(self.loc_y + 15.5) // 32 - 1
                    self.rect = self.image.get_rect(
                        center=(self.loc_x, self.loc_y))
                    self.cross_privilege = False
                    if markup.get_item_in(self.row, self.col) == 3:
                        self.trap = True
                elif self.teleporting and self.teleport_row > self.row-2:
                    self.teleport_row -= 1
                elif self.trap:
                    self.trap = False

        if down:
            if g.cell_at(self.row, self.col).south != None:
                if not self.teleporting and not self.trap and (self.cross_privilege or g.cell_at(self.row, self.col).is_linked(g.cell_at((int)(self.loc_y + self.vv + 15.5) // 32 - 1, self.col))):
                    self.auto_walk_dir = 'down'
                    self.prev_row = self.row
                    self.prev_col = self.col
                    self.loc_y += self.vv
                    self.row = (int)(self.loc_y + 15.5) // 32 - 1
                    self.rect = self.image.get_rect(
                        center=(self.loc_x, self.loc_y))
                    self.cross_privilege = False
                    if markup.get_item_in(self.row, self.col) == 3:
                        self.trap = True
                elif self.teleporting and self.teleport_row < self.row+2:
                    self.teleport_row += 1
                elif self.trap:
                    self.trap = False

        if left:
            if g.cell_at(self.row, self.col).west != None:
                if not self.teleporting and not self.trap and (self.cross_privilege or g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row, (int)(self.loc_x - self.hv + 15.5) // 32 - 1))):
                    self.auto_walk_dir = 'left'
                    self.prev_col = self.col
                    self.prev_row = self.row
                    self.loc_x -= self.hv
                    self.col = (int)(self.loc_x + 15.5) // 32 - 1
                    self.rect = self.image.get_rect(
                        center=(self.loc_x, self.loc_y))
                    self.cross_privilege = False
                    if markup.get_item_in(self.row, self.col) == 3:
                        self.trap = True
                elif self.teleporting and self.teleport_col > self.col-2:
                    self.teleport_col -= 1
                elif self.trap:
                    self.trap = False

        if right:
            if g.cell_at(self.row, self.col).east != None:
                if not self.teleporting and not self.trap and (self.cross_privilege or g.cell_at(self.row, self.col).is_linked(g.cell_at(self.row, (int)(self.loc_x + self.hv + 15.5) // 32 - 1))):
                    self.auto_walk_dir = 'right'
                    self.prev_col = self.col
                    self.prev_row = self.row
                    self.loc_x += self.hv
                    self.col = (int)(self.loc_x + 15.5) // 32 - 1
                    self.rect = self.image.get_rect(
                        center=(self.loc_x, self.loc_y))
                    self.cross_privilege = False
                    if markup.get_item_in(self.row, self.col) == 3:
                        self.trap = True
                elif self.teleporting and self.teleport_col < self.col+2:
                    self.teleport_col += 1
                elif self.trap:
                    self.trap = False

        if prop_use:
            self.useProp(markup)

    def auto_walk_dir_update(self, top, down, right, left):

        if top:
            self.auto_walk_dir = 'top'
            print("auto walk dir update", self.auto_walk_dir)
        if down:
            self.auto_walk_dir = 'down'
            print("auto walk dir update", self.auto_walk_dir)
        if left:
            self.auto_walk_dir = 'left'
            print("auto walk dir update", self.auto_walk_dir)
        if right:
            self.auto_walk_dir = 'right'
            print("auto walk dir update", self.auto_walk_dir)

    def rectChange(self):
        self.rect = self.image.get_rect(center=(self.loc_x, self.loc_y))

    def getGadget(self):
        self.prop = random.randint(1, 5)
        if self.prop == 1:
            self.hv *= -1
            self.vv *= -1
        print("get prop", self.prop)

    def useProp(self, markup):
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


exitFlag0 = False
exitFlag1 = False


class IceThread (threading.Thread):
    def __init__(self, threadID, name, player, g, prop_use, markup):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.player = player
        self.prop_use = prop_use
        self.markup = markup
        self.g = g

    def run(self):
        print("开始线程：" + self.name)
        ice_function(self, 1)
        print("退出线程：" + self.name)


def ice_function(self, delay):
    while True:
        if (self.player.name == 'player_zero' and exitFlag0) or (self.player.name == 'player_one' and exitFlag1):
            print("thread break")
            break
        time.sleep(delay)
        if self.player.auto_walk_dir == 'top':
            self.player.update(self.g, True, False, False,
                               False, self.prop_use, self.markup)
            print("auto walk ", self.player.auto_walk_dir)
        elif self.player.auto_walk_dir == 'down':
            self.player.update(self.g, False, True, False,
                               False, self.prop_use, self.markup)
            print("auto walk ", self.player.auto_walk_dir)
        elif self.player.auto_walk_dir == 'right':
            self.player.update(self.g, False, False, True,
                               False, self.prop_use, self.markup)
            print("auto walk ", self.player.auto_walk_dir)
        elif self.player.auto_walk_dir == 'left':
            self.player.update(self.g, False, False, False,
                               True, self.prop_use, self.markup)
            print("auto walk ", self.player.auto_walk_dir)
