import pygame.gfxdraw
import Maze
import random
import Character
import pygame
from pygame.locals import *

def main():
    pygame.init()
    WindowSize_x = 1034
    WindowSize_y = 620
    surface = pygame.display.set_mode([WindowSize_x,WindowSize_y])
    pygame.display.set_caption('Catch FLAG')
    background = pygame.image.load(r'F:\cis\3\ground.jpg').convert()
    image_surf = pygame.image.load(r'F:\cis\3\mario_sprites.png').convert()
    surface.blit(background,(0,0))


    player_group = pygame.sprite.Group()
    player_zero = Character.Player(image_surf)
    player_group.add(player_zero)


    clock= pygame.time.Clock()
    running = True
    markup = None
    g = Maze.Grid(19, 32)
    while running:
        clock.tick(60)
        left = False
        top = False
        right = False
        down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == K_q:  # Quit
                    running = False
                if event.key == K_n:  # New
                    g = Maze.Grid(19, 32)
                    markup = None
                if event.key == K_w:
                    Maze.wilson(g)
                    markup = None
                if event.key == K_UP:
                    top = True
                if event.key == K_LEFT:
                    left = True
                if event.key == K_DOWN:
                    down = True
                if event.key == K_RIGHT:
                    right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_UP:
                    top = False
                if event.key == pygame.K_DOWN:
                    down = False
        if left and right:
            left = False
            right = False

        if top and down:
            top = False
            down = False
        surface.blit(background, (0, 0))
        display_grid(g, markup, surface)
        player_group.update(WindowSize_x, WindowSize_y, top, down, right, left)
        player_group.draw(surface)
        pygame.display.flip()




def display_grid(g, markup, screen):
    for row in range(g.num_rows):
        for col in range(g.num_columns):
            c = g.cell_at(row, col)
            cell_x = col * 32 + 5
            cell_y = row * 32 + 5
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
