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
    background = pygame.image.load('ground.jpg').convert()
    image_surf = pygame.image.load('mario_sprites.png').convert()
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == K_q:  # Quit
                    running = False
                elif event.key == K_n:  # New
                    g = Maze.Grid(19, 32)
                    markup = None
                elif event.key == K_a:  # Aldous-Broder random walk
                    Maze.aldous_broder(g)
                    markup = None
                elif event.key == K_LEFT:
                    player_zero= Character.Player(image_surf)
                    player_zero.move_left = True
                elif event.key == K_RIGHT:
                    player_zero = Character.Player(image_surf)
                    player_zero.move_right = True
                elif event.key == K_UP:
                    player_zero = Character.Player(image_surf)
                    player_zero.move_up = True
                elif event.key == K_DOWN:
                    player_zero = Character.Player(image_surf)
                    player_zero.move_down = True
        surface.blit(background, (0, 0))
        display_grid(g, markup, surface)

        player_group.draw(surface)  #draw rect
        player_group.update(WindowSize_x, WindowSize_y)
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
