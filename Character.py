import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.hv = 5
        self.vv = 5
        self.size_x = 20
        self.size_y = 30
        self.gadget = None

    def update(self):
        pass


class PlayerOne(Player):
    def __init__(self):
        super().__init__()

class PlayerTwo(Player):
    def __init__(self):
        super().__init__()


class Gadgets:
    def __init__(self):
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

