import pygame.gfxdraw
import Maze
import random
import  sys
import Character
import pygame
from pygame.locals import *

def main():
    pygame.init()
    WindowSize_x = 1000
    WindowSize_y = 600
    surface = pygame.display.set_mode([WindowSize_x,WindowSize_y])
    pygame.display.set_caption('CATCH THE FLAG')
    background = pygame.image.load('背景图片/瓷砖.jpg').convert()
    background_zero = pygame.image.load('背景图片/menu.png').convert()
    background_final = pygame.image.load('mario_background.png').convert()
    player_zero_sprite = pygame.image.load('sprites/players/Mario.png').convert()
    player_one_sprite = pygame.image.load('sprites/players/Luigi.png').convert()
    player_zero_sprite = pygame.transform.scale(player_zero_sprite, (int(player_zero_sprite.get_size()[0]/4), int(player_zero_sprite.get_size()[1]/4)))
    player_one_sprite = pygame.transform.scale(player_one_sprite, (int(player_one_sprite.get_size()[0]/4), int(player_one_sprite.get_size()[1]/4)))
    background_zero = pygame.transform.scale(background_zero,(int(background_zero.get_size()[0]*3), int(background_zero.get_size()[1]*2)) )
    surface.blit(background,(0,0))

    '''drawing the background and players initially'''

    player_group = pygame.sprite.Group()
    player_zero = Character.Player(player_zero_sprite)
    player_one = Character.Player(player_one_sprite)
    player_group.add(player_zero)
    player_group.add(player_one)
    '''initialize the players'''

    clock= pygame.time.Clock()
    running = True
    state = 0
    final = True
    '''loop things'''

    while True:
        surface.blit(background_zero, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_b:
                    state += 1
                    break
        if state == 1:
            break
        pygame.display.flip()
    '''initial interface'''

    surface.blit(background, (0, 0))
    g = Maze.Grid(18, 24)
    Maze.ABWilson(g)
    markup = Maze.FlagAndPlayersMarkup(g)
    display_grid(g, markup, surface, player_zero, player_one)
    player_group.clear(surface, background)
    player_zero.rectChange()
    player_one.rectChange()
    '''game interface'''
    while running:
        clock.tick(60)
        left = False
        top = False
        right = False
        down = False
        left1 = False
        top1 = False
        right1 = False
        down1 = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == K_q:  # Quit
                    running = False
                if event.key == K_UP:
                    top = True
                if event.key == K_LEFT:
                    left = True
                if event.key == K_DOWN:
                    down = True
                if event.key == K_RIGHT:
                    right = True
                if event.key == K_w:
                    top1 = True
                if event.key == K_a:
                    left1 = True
                if event.key == K_s:
                    down1 = True
                if event.key == K_d:
                    right1 = True

            if event.type == pygame.KEYUP:
                if event.key == K_l:  # longest path
                    markup = Maze.LongestPathMarkup(g)
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP:
                    top = False
                if event.key == pygame.K_DOWN:
                    down = False
                if event.key == K_w:
                    top1 = False
                if event.key == K_a:
                    left1 = False
                if event.key == K_s:
                    down1 = False
                if event.key == K_d:
                    right1 = False
        if left and right:
            left = False
            right = False
        if left1 and right1:
            left1 = False
            right1 = False
        if top and down:
            top = False
            down = False
        if top1 and down1:
            top1 = False
            down1 = False

        player_group.clear(surface, background)
        player_zero.update(g, top, down, right, left)
        player_one.update(g, top1, down1, right1, left1)
        if markup.get_item_at(player_one.row, player_one.col) == 'f' or markup.get_item_at(player_zero.row, player_zero.col) == 'f':
            running = False

        player_group.draw(surface)
        pygame.display.flip()
    while final :
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                final = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    final = False
        surface.blit(background_final, (0, 0))
        pygame.display.flip()





def display_grid(g, markup, screen, player_zero, player_one):
    for row in range(g.num_rows):
        for col in range(g.num_columns):
            c = g.cell_at(row, col)
            cell_x = col * 32+1
            cell_y = row * 32+1

            # Draw top row
            if markup:
                value = markup.get_item_at(row, col)
                if not value:
                    continue
                if value == '*':  # Path marker
                    pygame.draw.circle(screen,
                                       (255, 255, 50),
                                       (cell_x + 15, cell_y + 15),
                                       7,  # radius
                                       0)  # filled
                if value == 'f':  # Flag
                    pygame.draw.circle(screen,
                                       (255,50,50),
                                       (cell_x+15,cell_y+15),
                                       7,  #radius
                                       0)  #filled
                if value == 'p0':  # Player
                    pygame.draw.circle(screen,
                                       (50,255,50),
                                       (cell_x+15,cell_y+15),
                                       7,  #radius
                                       0)  #filled
                    player_zero.directMoveViaLoc(cell_x+16.5, cell_y+16.5)
                if value == 'p1':  # Player
                    pygame.draw.circle(screen,
                                       (50,50,255),
                                       (cell_x+15,cell_y+15),
                                       7,  #radius
                                       0)  #filled
                    player_one.directMoveViaLoc(cell_x+16.5, cell_y+16.5)
                if isinstance(value, list) and len(value) == 3:
                    pygame.draw.rect(screen,
                                     value,  # color
                                     (cell_x, cell_y, 32, 32))

            if not c.north or not c.is_linked(c.north):
                pygame.gfxdraw.hline(screen,
                                     cell_x, cell_x + 31, cell_y,
                                     (255, 255, 255))
            if not c.south or not c.is_linked(c.south):
                pygame.gfxdraw.hline(screen,
                                     cell_x, cell_x + 31, cell_y + 31,
                                     (255, 255, 255))
            if not c.east or not c.is_linked(c.east):
                pygame.gfxdraw.vline(screen,
                                     cell_x + 31, cell_y, cell_y + 31,
                                     (255, 255, 255))
            if not c.west or not c.is_linked(c.west):
                pygame.gfxdraw.vline(screen,
                                     cell_x, cell_y, cell_y + 31,
                                     (255, 255, 255))





if __name__ == "__main__":
    main()
