import pygame.gfxdraw
import Maze
import random

def main():
    pygame.init()
    WindowSize_x = 1300
    WindowSize_y = 650
    surface = pygame.display.set_mode([WindowSize_x,WindowSize_y])
    pygame.display.set_caption('Catch FLAG')
    background = pygame.image.load(r'').convert()
