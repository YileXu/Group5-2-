import pygame

class Land(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loc_x = 16.5
        self.loc_y = 16.5
        self.image = pygame.Surface((28, 28))
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
        self.gad_surf = pygame.image.load('sprites/道具/water.png').convert()
        self.image.blit(self.gad_surf, (0, 0), (0, 0, self.gad_surf.get_rect(
        ).size[0], self.gad_surf.get_rect().size[1]))
