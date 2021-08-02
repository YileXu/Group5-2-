import pygame.gfxdraw
import Maze
import random
import sys
import Character
import pygame
import show_maze
import Randombox
import Land
from pygame.locals import *


def main():

    grid_row = 20
    grid_col = 25
    gadgets_num = 6
    player_one_auto_walk = False
    player_zero_auto_walk = False

    pygame.init()

    WindowSize_x = 800
    WindowSize_y = 730

    WindowSize_x = 802
    WindowSize_y = 802

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
    player_zero = Character.Player('player_zero', player_zero_sprite)
    player_one = Character.Player('player_one', player_one_sprite)
    player_group.add(player_zero, player_one)

    gadgets_group = pygame.sprite.Group()
    randombox1 = Randombox.Randombox()
    randombox2 = Randombox.Randombox()
    randombox3 = Randombox.Randombox()
    randombox4 = Randombox.Randombox()
    randombox5 = Randombox.Randombox()
    randombox6 = Randombox.Randombox()

    land_group = pygame.sprite.Group()
    ice_list = []
    for i in range(20):
        ice = Land.Ice()
        ice_list.append(ice)
        land_group.add(ice)
    water_list = []
    for i in range(40):
        water = Land.Water()
        water_list.append(water)
        land_group.add(water)
    '''mine = Character.Mine()
    transporter = Character.Transporter()
    bomb = Character.Bomb()
    converse = Character.Converse()
    passwall = Character.PassWall()
    trap = Character.Trap()'''

    gadgets_group.add(randombox1, randombox2, randombox3, randombox4, randombox5, randombox6)
    '''gadgets_group.add(mine)
    gadgets_group.add(transporter)
    gadgets_group.add(bomb)
    gadgets_group.add(converse)
    gadgets_group.add(passwall)
    gadgets_group.add(trap)'''
    for i in range(gadgets_num):
        gadgets_group.add(Randombox.Randombox())


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

    list1 = []
    for randombox in gadgets_group:
        list1.append(randombox)
    print("len of list", len(list1))

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
        ice = Land.Ice()
        ice_list.append(ice)
        land_group.add(ice)
    water_list = []
    for i in range(water_count):
        water = Land.Water()
        water_list.append(water)
        land_group.add(water)
    show_maze.display_grid(g, markup, surface, player_zero,
                           player_one, list1, ice_list, water_list)
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

        if not player_zero_auto_walk:
            player_zero.update(g, top, down, right, left, prop_use, markup)
        else:
            player_zero.auto_walk_dir_update(top, down, right, left)
        if not player_one_auto_walk:
            player_one.update(g, top1, down1, right1, left1, prop_use1, markup)
        else:
            player_one.auto_walk_dir_update(top1, down1, right1, left1)
        '''ice walk and normal walk'''

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

        if player_zero_auto_walk and markup.get_item_in(player_zero.row, player_zero.col) != 2:
            player_zero_auto_walk = False
            Character.exitFlag0 = True
        if player_one_auto_walk and markup.get_item_in(player_one.row, player_one.col) != 2:
            player_one_auto_walk = False
            Character.exitFlag1 = True

        if not player_zero_auto_walk and markup.get_item_in(player_zero.row, player_zero.col) == 2:
            player_zero_auto_walk = True
            Character.exitFlag0 = False
            thread0 = Character.IceThread(
                0, "Thread-0", player_zero, g, prop_use, markup)
            thread0.start()
        if not player_one_auto_walk and markup.get_item_in(player_one.row, player_one.col) == 2:
            player_one_auto_walk = True
            Character.exitFlag1 = False
            thread1 = Character.IceThread(
                1, "Thread-1", player_one, g, prop_use, markup)
            thread1.start()
        '''ice walk'''

        if markup.get_item_at(player_one.row, player_one.col) == 'f' or markup.get_item_at(player_zero.row, player_zero.col) == 'f':
            player_zero_auto_walk = False
            Character.exitFlag0 = True
            player_one_auto_walk = False
            Character.exitFlag1 = True
            running = False

        land_group.draw(surface)
        gadgets_group.draw(surface)
        player_group.draw(surface)
        pygame.display.flip()
        '''game loop'''
    player_zero_auto_walk = False
    Character.exitFlag0 = True
    player_one_auto_walk = False
    Character.exitFlag1 = True

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


if __name__ == "__main__":
    main()
