import pygame
import pygame.gfxdraw
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
                                     (0, 0, 0))
            if not c.south or not c.is_linked(c.south):
                pygame.gfxdraw.hline(screen,
                                     cell_x, cell_x + 31, cell_y + 31,
                                     (0, 0, 0))
            if not c.east or not c.is_linked(c.east):
                pygame.gfxdraw.vline(screen,
                                     cell_x + 31, cell_y, cell_y + 31,
                                     (0, 0, 0))
            if not c.west or not c.is_linked(c.west):
                pygame.gfxdraw.vline(screen,
                                     cell_x, cell_y, cell_y + 31,
                                     (0, 0, 0))


def put_bomb(g, markup, screen):
    for row in range(g.num_rows):
        for col in range(g.num_columns):
            if markup:
                value = markup.get_item_at(row, col)
                if value == 'b':
                    pygame.draw.circle(screen, (112, 128, 105),(col*32+16, row*32+16),7, 0)


def bomb_effect(surface, player):
    cell_x = player.col * 32 + 1
    cell_y = player.row * 32 + 1
    pygame.gfxdraw.hline(surface,
                         cell_x, cell_x + 31, cell_y - 31,
                         (255, 97, 0))
    pygame.gfxdraw.hline(surface,
                         cell_x, cell_x + 31, cell_y + 62,
                         (255, 97, 0))
    pygame.gfxdraw.hline(surface,
                         cell_x - 31, cell_x, cell_y - 31,
                         (255, 97, 0))
    pygame.gfxdraw.hline(surface,
                         cell_x - 31, cell_x, cell_y + 62,
                         (255, 97, 0))
    pygame.gfxdraw.hline(surface,
                         cell_x + 31, cell_x + 62, cell_y + 62,
                         (255, 97, 0))
    pygame.gfxdraw.hline(surface,
                         cell_x + 31, cell_x + 62, cell_y - 31,
                         (255, 97, 0))

    pygame.gfxdraw.vline(surface,
                         cell_x - 31, cell_y + 31, cell_y +62,
                         (255, 97, 0))
    pygame.gfxdraw.vline(surface,
                         cell_x - 31, cell_y, cell_y + 31,
                         (255, 97, 0))
    pygame.gfxdraw.vline(surface,
                         cell_x - 31, cell_y - 31, cell_y,
                         (255, 97, 0))
    pygame.gfxdraw.vline(surface,
                         cell_x + 62, cell_y, cell_y + 31,
                         (255, 97, 0))
    pygame.gfxdraw.vline(surface,
                         cell_x, cell_y - 31, cell_y,
                         (255, 97, 0))
    pygame.gfxdraw.vline(surface,
                         cell_x, cell_y + 31, cell_y + 62,
                         (255, 97, 0))

def set_tp(surface, player):
    cell_x = player.col * 32 + 1
    cell_y = player.row * 32 + 1
    pygame.gfxdraw.hline(surface,
                         cell_x - 62, cell_x - 31, cell_y - 62,
                         (3, 168, 158))
    pygame.gfxdraw.hline(surface,
                         cell_x - 31, cell_x, cell_y - 62,
                         (3, 168, 158))
    pygame.gfxdraw.hline(surface,
                         cell_x, cell_x + 31, cell_y - 62,
                         (3, 168, 158))
    pygame.gfxdraw.hline(surface,
                         cell_x + 31, cell_x +62, cell_y - 62,
                         (3, 168, 158))
    pygame.gfxdraw.hline(surface,
                         cell_x + 62, cell_x + 93, cell_y - 62,
                         (3, 168, 158))

    pygame.gfxdraw.hline(surface,
                         cell_x - 62, cell_x - 31, cell_y + 93,
                         (3, 168, 158))
    pygame.gfxdraw.hline(surface,
                         cell_x - 31, cell_x, cell_y + 93,
                         (3, 168, 158))
    pygame.gfxdraw.hline(surface,
                         cell_x, cell_x + 31, cell_y + 93,
                         (3, 168, 158))
    pygame.gfxdraw.hline(surface,
                         cell_x + 31, cell_x + 62, cell_y + 93,
                         (3, 168, 158))
    pygame.gfxdraw.hline(surface,
                         cell_x + 62, cell_x + 93, cell_y + 93,
                         (3, 168, 158))


    pygame.gfxdraw.vline(surface,
                         cell_x - 62, cell_y - 62, cell_y - 31,
                         (3, 168, 158))
    pygame.gfxdraw.vline(surface,
                         cell_x - 62, cell_y - 31, cell_y,
                         (3, 168, 158))
    pygame.gfxdraw.vline(surface,
                         cell_x - 62, cell_y, cell_y + 31,
                         (3, 168, 158))
    pygame.gfxdraw.vline(surface,
                         cell_x - 62, cell_y + 31, cell_y + 62,
                         (3, 168, 158))
    pygame.gfxdraw.vline(surface,
                         cell_x - 62, cell_y + 62, cell_y + 93,
                         (3, 168, 158))

    pygame.gfxdraw.vline(surface,
                         cell_x + 93, cell_y - 62, cell_y - 31,
                         (3, 168, 158))
    pygame.gfxdraw.vline(surface,
                         cell_x + 93, cell_y - 31, cell_y,
                         (3, 168, 158))
    pygame.gfxdraw.vline(surface,
                         cell_x + 93, cell_y, cell_y + 31,
                         (3, 168, 158))
    pygame.gfxdraw.vline(surface,
                         cell_x + 93, cell_y + 31, cell_y + 62,
                         (3, 168, 158))
    pygame.gfxdraw.vline(surface,
                         cell_x + 93, cell_y + 62, cell_y + 93,
                         (3, 168, 158))
















