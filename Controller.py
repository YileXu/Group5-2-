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

START = 0
GAMELOOP = 1
ENDING = 2


def main():

    state = START
    winner = None

    grid_row = 20
    grid_col = 25
    gadgets_num = 6
    player_one_auto_walk = False
    player_zero_auto_walk = False

    pygame.init()
    WindowSize_x = 800
    WindowSize_y = 730
    surface = pygame.display.set_mode([WindowSize_x, WindowSize_y])
    pygame.display.set_caption('CATCH THE FLAG')
    background = pygame.image.load('背景图片/瓷砖.png').convert()
    background_zero = pygame.image.load('背景图片/menu.png').convert()
    background_final = pygame.image.load('gameover.png').convert()
    player_zero_sprite = pygame.image.load(
        'sprites/players/Pepper-Pete.png').convert()
    player_one_sprite = pygame.image.load(
        'sprites/players/Luigi.png').convert()
    background = pygame.transform.scale(background, (int(
        background.get_size()[0] * 2), int(background.get_size()[1] * 2.7)))
    player_zero_sprite = pygame.transform.scale(player_zero_sprite, (int(
        player_zero_sprite.get_size()[0]/4), int(player_zero_sprite.get_size()[1]/4)))
    player_one_sprite = pygame.transform.scale(player_one_sprite, (int(
        player_one_sprite.get_size()[0]/4), int(player_one_sprite.get_size()[1]/4)))
    background_zero = pygame.transform.scale(background_zero, (int(
        background_zero.get_size()[0]*2), int(background_zero.get_size()[1]*2.315)))
    background_final = pygame.transform.scale(background_final, (int(
        background_final.get_size()[0] * 2.2), int(background_final.get_size()[1] * 3)))
    surface.blit(background, (0, 0))
    '''drawing the background and players initially'''

    player_group = pygame.sprite.Group()
    player_zero = Character.Player('player_zero', player_zero_sprite)
    player_one = Character.Player('player_one', player_one_sprite)
    player_group.add(player_zero, player_one)
    '''initialize the players'''

    gadgets_group = pygame.sprite.Group()
    for i in range(gadgets_num):
        gadgets_group.add(Randombox.Randombox())
    '''initialize the gadgets'''

    clock = pygame.time.Clock()
    '''loop things'''

    generate_g = Maze.Grid(grid_row, grid_col)
    Maze.wilson(generate_g)
    generate_markup = Maze.FlagAndPlayersMarkup(generate_g)

    while True:
        if state == START:
            surface.blit(background_zero, (2, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    if event.key == K_b:
                        surface.blit(background, (0, 0))
                        g = generate_g
                        markup = generate_markup

                        list1 = []
                        font = pygame.font.SysFont('Courier New', 38)
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
                        lemon = (50, 205, 50)
                        clay = (138, 54, 15)
                        '''distributed positions'''
                        Playerone_font = font.render('Player One', True, lemon, None)
                        surface.blit(Playerone_font, (40, 674), Playerone_font.get_rect())
                        Playertwo_font = font.render('Player Two', True, clay, None)
                        surface.blit(Playertwo_font, (540, 674), Playertwo_font.get_rect())

                        non_prop = pygame.image.load('sprites/道具/水.jpg').convert()
                        non_prop = pygame.transform.scale(non_prop, (non_prop.get_rect().width//4, non_prop.get_rect().height//4))

                        conv_surf = pygame.image.load('sprites/道具/反转.png').convert()
                        conv_surf = pygame.transform.scale(conv_surf, (conv_surf.get_rect().width//6, conv_surf.get_rect().height//6))
                        mine_surf = pygame.image.load('sprites/道具/地雷.png').convert()
                        mine_surf = pygame.transform.scale(mine_surf, (mine_surf.get_rect().width//6, mine_surf.get_rect().height//6))

                        pass_surf = pygame.image.load('sprites/道具/墙.png').convert()
                        pass_surf = pygame.transform.scale(pass_surf, (pass_surf.get_rect().width//6, pass_surf.get_rect().height//6))

                        tran_surf = pygame.image.load('sprites/道具/传送.png').convert()
                        tran_surf = pygame.transform.scale(tran_surf, (tran_surf.get_rect().width//6, tran_surf.get_rect().height//6))

                        bomb_surf = pygame.image.load('sprites/道具/炸弹.png').convert()
                        bomb_surf = pygame.transform.scale(bomb_surf, (bomb_surf.get_rect().width//6, bomb_surf.get_rect().height//6))

                        prop_img_list = [conv_surf, mine_surf, pass_surf, tran_surf, bomb_surf]
                        prop_size_list = [(0, 0, 8000, 6467), (0, 0, 4167, 4167), (0, 0, 1600, 1600), (0, 0, 617, 655), (0, 0, 500, 500)]
                        state = GAMELOOP
                        break
            pygame.display.flip()
        '''Game Start'''

        if state == GAMELOOP:
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
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
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


            for i in range(5):
                if player_one.prop == i+1:
                    area = pygame.Surface((50, 50))
                    area.blit(prop_img_list[i], (-20, -20), prop_size_list[i])
                    area.set_colorkey((0,0,0))
                    surface.blit(area, (290, 670), area.get_rect())
                if player_one.prop == 0:
                    pygame.draw.rect(surface, (0, 0, 0), (290, 670, 50, 50))
                if player_zero.prop == i+1:
                    area0 = pygame.Surface((50, 50))
                    area0.blit(prop_img_list[i], (-20, -20), prop_size_list[i])
                    area0.set_colorkey((0,0,0))
                    surface.blit(area0, (480, 670), area0.get_rect())
                if player_zero.prop == 0:
                    pygame.draw.rect(surface, (0, 0, 0), (480, 670, 50, 50))

            for player in player_group:
                if markup.get_item_at(player.row, player.col) == 'p':
                    player.getGadget()   #抽个数
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
                        show_maze.bomb_effect(surface, player)

                        markup.set_item_at(player.row, player.col, ' ')
                        player.directMoveViaColRow(
                            player.col+col_offset, player.row+row_offset)
                        print("boom, I am at", player.row, player.col)
                        break
            show_maze.put_bomb(g, markup, surface)

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
                player_zero_auto_walk = False
                Character.exitFlag0 = True
                player_one_auto_walk = False
                Character.exitFlag1 = True
                if markup.get_item_at(player_one.row, player_one.col) == 'f':
                    winner = 1
                else:
                    winner = 0
                state = ENDING

            land_group.draw(surface)
            gadgets_group.draw(surface)
            player_group.draw(surface)
            pygame.display.flip()
        '''Game Loop'''

        if state == ENDING:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if (event.key == pygame.K_q and winner == 0) or (event.key == pygame.K_m and winner == 1):
                        player_group = pygame.sprite.Group()
                        player_zero = Character.Player('player_zero', player_zero_sprite)
                        player_one = Character.Player('player_one', player_one_sprite)
                        player_group.add(player_zero, player_one)
                        state = START
            surface.blit(background_final, (0, 0))
            pygame.display.flip()
        '''Game Over'''

if __name__ == "__main__":
    main()

