import pygame

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