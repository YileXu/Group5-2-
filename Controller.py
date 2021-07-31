import pygame.gfxdraw
import Maze
import random
import sys
import Character
import pygame
from pygame.locals import *


def main():

    grid_row = 18
    grid_col = 24
    gadgets_num = 6

    pygame.init()
    WindowSize_x = 800
    WindowSize_y = 670
    surface = pygame.display.set_mode([WindowSize_x, WindowSize_y])
    pygame.display.set_caption('CATCH THE FLAG')
    background = pygame.image.load('背景图片/瓷砖.jpg').convert()
    background_zero = pygame.image.load('背景图片/menu.png').convert()
    background_final = pygame.image.load('gameover.png').convert()
    player_zero_sprite = pygame.image.load(
        'sprites/players/Pepper-Pete.png').convert()
    player_one_sprite = pygame.image.load(
        'sprites/players/Luigi.png').convert()
    player_zero_sprite = pygame.transform.scale(player_zero_sprite, (int(
        player_zero_sprite.get_size()[0]/4), int(player_zero_sprite.get_size()[1]/4)))
    player_one_sprite = pygame.transform.scale(player_one_sprite, (int(
        player_one_sprite.get_size()[0]/4), int(player_one_sprite.get_size()[1]/4)))
    background_zero = pygame.transform.scale(background_zero, (int(
        background_zero.get_size()[0]*2), int(background_zero.get_size()[1]*2.3)))
    background_final = pygame.transform.scale(background_final, (int(
        background_final.get_size()[0] * 2.2), int(background_final.get_size()[1] * 3)))
    surface.blit(background, (0, 0))

    '''drawing the background and players initially'''

    player_group = pygame.sprite.Group()
    player_zero = Character.Player(player_zero_sprite)
    player_one = Character.Player(player_one_sprite)
    player_group.add(player_zero, player_one)

    gadgets_group = pygame.sprite.Group()
    for i in range(gadgets_num):
        gadgets_group.add(Character.Randombox())

    '''initialize the players'''

    clock = pygame.time.Clock()
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
    g = Maze.Grid(grid_row, grid_col)
    Maze.wilson(g)
    markup = Maze.FlagAndPlayersMarkup(g)
    list = []
    for randombox in gadgets_group:
        list.append(randombox)
    print("len of list", len(list))
    land_group = pygame.sprite.Group()
    ice_count = 0
    water_count = 0
    for cell in markup.cost:
        cost = markup.cost[cell]
        if cost == 2:
            ice_count += 1
        elif cost == 3:
            water_count += 1
    ice_list = []
    for i in range(ice_count):
        ice = Character.Ice()
        ice_list.append(ice)
        land_group.add(ice)
    water_list = []
    for i in range(water_count):
        water = Character.Water()
        water_list.append(water)
        land_group.add(water)
    display_grid(g, markup, surface, player_zero,
                 player_one, list, ice_list, water_list)
    player_group.clear(surface, background)
    player_zero.rectChange()
    player_one.rectChange()
    for ice in ice_list:
        ice.rectChange()
    for water in water_list:
        water.rectChange()
    for randombox in gadgets_group:
        randombox.rectChange()
    '''distributed positions'''

    while running:
        clock.tick(60)
        left = False
        top = False
        right = False
        down = False
        prop_use = False
        left1 = False
        top1 = False
        right1 = False
        down1 = False
        prop_use1 = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == K_q:  # Quit
                    if player_one.prop != 0:
                        pass
                if event.key == K_UP:
                    top = True
                if event.key == K_LEFT:
                    left = True
                if event.key == K_DOWN:
                    down = True
                if event.key == K_RIGHT:
                    right = True
                if event.key == K_m:
                    prop_use = True
                if event.key == K_w:
                    top1 = True
                if event.key == K_a:
                    left1 = True
                if event.key == K_s:
                    down1 = True
                if event.key == K_d:
                    right1 = True
                if event.key == K_q:
                    prop_use1 = True

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
                if event.key == K_m:
                    prop_use = False
                if event.key == K_w:
                    top1 = False
                if event.key == K_a:
                    left1 = False
                if event.key == K_s:
                    down1 = False
                if event.key == K_d:
                    right1 = False
                if event.key == K_q:
                    prop_use1 = False

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
        pygame.sprite.groupcollide(
            player_group, land_group, False, False, collided=pygame.sprite.collide_rect)
        if len(gadgets_group) > 0:
            pygame.sprite.groupcollide(
                player_group, gadgets_group, False, True, collided=pygame.sprite.collide_circle)

        player_zero.update(g, top, down, right, left, prop_use, markup)
        player_one.update(g, top1, down1, right1, left1, prop_use1, markup)

        for player in player_group:
            if markup.get_item_at(player.row, player.col) == 'p':
                player.getGadget()
                markup.set_item_at(player.row, player.col, ' ')
            elif markup.get_item_at(player.row, player.col) == 'b':  # bomb detection
                print("meet bomb")
                cur_cell = g.grid[player.row][player.col]
                while True:
                    row_offset = random.randint(-1, 1)
                    col_offset = random.randint(-1, 1)
                    if row_offset == 0 and col_offset == 0:
                        continue
                    elif (row_offset == -1 and cur_cell.north == None) or (row_offset == 1 and cur_cell.south == None):
                        continue
                    elif (col_offset == -1 and cur_cell.west == None) or (col_offset == 1 and cur_cell.east == None):
                        continue
                    markup.set_item_at(player.row, player.col, ' ')
                    player.directMoveViaColRow(
                        player.col+col_offset, player.row+row_offset)
                    print("boom, I am at", player.row, player.col)
                    break

        if markup.get_item_at(player_one.row, player_one.col) == 'f' or markup.get_item_at(player_zero.row, player_zero.col) == 'f':
            running = False

        land_group.draw(surface)
        gadgets_group.draw(surface)
        player_group.draw(surface)
        pygame.display.flip()
        '''game loop'''

    while final:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                final = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    final = False
        surface.blit(background_final, (0, 0))
        pygame.display.flip()
        '''Game Over'''


def display_grid(g, markup, screen, player_zero, player_one, gad_list, icelist, waterlist):
    for row in range(g.num_rows):
        for col in range(g.num_columns):
            c = g.cell_at(row, col)
            cell_x = col * 32+1
            cell_y = row * 32+1

            # Draw top row
            if markup:
                value = markup.get_item_at(row, col)
                cos = markup.get_item_in(row, col)
                if not value:
                    continue
                if cos == 2:    # Ice
                    pygame.draw.circle(screen,
                                       (135, 206, 235),
                                       (cell_x + 15, cell_y + 15),
                                       9,  # radius
                                       0)  # filled
                    icelist[0].directMoveViaLoc(cell_x + 16.5, cell_y + 16.5)
                    icelist.pop(0)
                if cos == 3:    # Water
                    pygame.draw.circle(screen,
                                       (65, 105, 225),
                                       (cell_x + 15, cell_y + 15),
                                       9,  # radius
                                       0)  # filled
                    waterlist[0].directMoveViaLoc(cell_x + 16.5, cell_y + 16.5)
                    waterlist.pop(0)
                if value == '*':  # Path marker
                    pygame.draw.circle(screen,
                                       (255, 255, 50),
                                       (cell_x + 15, cell_y + 15),
                                       7,  # radius
                                       0)  # filled
                if value == 'f':  # Flag
                    pygame.draw.circle(screen,
                                       (255, 50, 50),
                                       (cell_x+15, cell_y+15),
                                       7,  # radius
                                       0)  # filled
                if value == 'p0':  # Player
                    pygame.draw.circle(screen,
                                       (50, 255, 50),
                                       (cell_x+15, cell_y+15),
                                       7,  # radius
                                       0)  # filled
                    player_zero.directMoveViaLoc(cell_x+16.5, cell_y+16.5)
                if value == 'p1':  # Player
                    pygame.draw.circle(screen,
                                       (50, 50, 255),
                                       (cell_x+15, cell_y+15),
                                       7,  # radius
                                       0)  # filled
                    player_one.directMoveViaLoc(cell_x+16.5, cell_y+16.5)
                if value == 'p':  # Gadgets
                    pygame.draw.circle(screen,
                                       (255, 255, 255),
                                       (cell_x+15, cell_y+15),
                                       7,  # radius
                                       0)  # filled
                    print("draw circle")
                    print(len(gad_list), "before")
                    if len(gad_list) != 0:
                        gad_list[0].directMoveViaLoc(cell_x+16.5, cell_y+16.5)
                        gad_list.pop(0)
                        print(len(gad_list), "after")

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
