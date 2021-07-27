import pygame.gfxdraw
import Maze
import random
import Character

def main():
    pygame.init()
    WindowSize_x = 1300
    WindowSize_y = 650
    surface = pygame.display.set_mode([WindowSize_x,WindowSize_y])
    pygame.display.set_caption('Catch FLAG')
    background = pygame.image.load(r'F:\cis\3\mario_background.png').convert()
    image_surf = pygame.image.load(r'F:\cis\4\code\mario_sprites.png').convert()
    surface.blit(background,(0,0))


    player_group = pygame.sprite.Group
    player_zero = Character.Player(image_surf)
    player_group.add(player_zero)


    clock= pygame.time.Clock()
    running = True
    markup = None
    g = Maze.Grid(24, 32)
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
                    g = mazes.Grid(24, 32)
                    markup = None
                elif event.key == K_a:  # Aldous-Broder random walk
                    mazes.aldous_broder(g)
                    markup = None
                elif event.key == pygame.K_LEFT:
                    player1.move_left = True
                elif event.key == pygame.K_RIGHT:
                    player1.move_right = True
                elif event.key == pygame.K_UP:
                    player1.move_uo = True
                elif event.key == pygame.K_DOWN:
                    player1.move_down = True
        surface.blit(background, (0, 0))
        display_grid(g, markup, surface)

        player_group.draw(surface)
        player_group.update(WindowSize_x, WindowSize_y)
        pygame.display.flip()


def display_grid(g, markup, screen):
    screen.fill((0, 0, 0))
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
                                       (150, 80, 50),
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
                                     (100, 100, 100))
            if not c.south or not c.is_linked(c.south):
                pygame.gfxdraw.hline(screen,
                                     cell_x, cell_x + 31, cell_y + 31,
                                     (100, 100, 100))
            if not c.east or not c.is_linked(c.east):
                pygame.gfxdraw.vline(screen,
                                     cell_x + 31, cell_y, cell_y + 31,
                                     (100, 100, 100))
            if not c.west or not c.is_linked(c.west):
                pygame.gfxdraw.vline(screen,
                                     cell_x, cell_y, cell_y + 31,
                                     (100, 100, 100))





if __name__ == "__main__":
    main()
