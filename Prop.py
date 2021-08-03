import pygame

class Prop(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.image = pygame.Surface((70, 70))
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