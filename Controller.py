import pygame.gfxdraw
import Maze
import random
import Character
import pygame
from pygame.locals import *

def main():
    pygame.init()
    WindowSize_x = 1000
    WindowSize_y = 600
    surface = pygame.display.set_mode([WindowSize_x,WindowSize_y])
    pygame.display.set_caption('Catch FLAG')
    background = pygame.image.load('ground.jpg').convert()
    image_surf = pygame.image.load('mario_sprites.png').convert()
    surface.blit(background,(0,0))


    player_group = pygame.sprite.Group()
    player_zero = Character.Player(image_surf)
    player_one = Character.Player(image_surf)
    player_group.add(player_zero)
    player_group.add(player_one)


    clock= pygame.time.Clock()
    running = True
    markup = None
    g = Maze.Grid(19, 24)
    Maze.wilson(g)
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

        surface.blit(background, (0, 0))
        display_grid(g, markup, surface)
        player_zero.update(g, top, down, right, left)
        player_one.update(g, top1, down1, right1, left1)
        player_group.draw(surface)
        pygame.display.flip()




def display_grid(g, markup, screen):
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
