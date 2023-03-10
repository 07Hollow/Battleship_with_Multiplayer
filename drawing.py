from import_and_color_size_setting import *

def draw_ships(ships_coordinates_list):
    """
    Draws rectangles around the blocks that are occupied by a ship
    Args:
        ships_coordinates_list (list of tuples): a list of ships's coordinates
    """
    for elem in ships_coordinates_list:
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        # Horizontal and 1block ships
        ship_width = block_size * len(ship)
        ship_height = block_size
        # Vertical ships
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width, ship_height = ship_height, ship_width
        x = block_size * (x_start - 1) + left_margin
        y = block_size * (y_start - 1) + upper_margin
        pygame.draw.rect(
            screen, GREEN, ((x, y), (ship_width, ship_height)), width=block_size // 10)


def draw_from_dotted_set(dotted_set_to_draw_from):
    """
    Draws dots in the center of all blocks in the dotted_set
    """
    for elem in dotted_set_to_draw_from:
        pygame.draw.circle(screen, BLUE, (block_size * (
            elem[0] - 0.5) + left_margin, block_size * (elem[1] - 0.5) + upper_margin), block_size // 6)


def draw_hit_blocks(hit_blocks_to_draw_from):
    """
    Draws 'X' in the blocks that were successfully hit either by computer or by human
    """
    for block in hit_blocks_to_draw_from:
        x1 = block_size * (block[0] - 1) + left_margin
        y1 = block_size * (block[1] - 1) + upper_margin
        pygame.draw.line(screen, RED, (x1, y1),
                         (x1 + block_size, y1 + block_size), block_size // 6)
        pygame.draw.line(screen, RED, (x1, y1 + block_size),
                         (x1 + block_size, y1), block_size // 6)


def show_message_at_rect_center(message, rect, which_font=font, color=RED):
    """
    Prints message to screen at a given rect's center.
    Args:
        message (str): Message to print
        rect (tuple): rectangle in (x_start, y_start, width, height) format
        which_font (pygame font object, optional): What font to use to print message. Defaults to font.
        color (tuple, optional): Color of the message. Defaults to RED.
    """
    message_width, message_height = which_font.size(message)
    message_rect = pygame.Rect(rect)
    x_start = message_rect.centerx - message_width / 2
    y_start = message_rect.centery - message_height / 2
    background_rect = pygame.Rect(
        x_start - block_size / 2, y_start, message_width + block_size, message_height)
    message_to_blit = which_font.render(message, True, color)
    screen.fill(GREY, background_rect)
    screen.blit(message_to_blit, (x_start, y_start))


def ship_is_valid(ship_set, blocks_for_manual_drawing):
    """
    Checks if ship is not touching other ships
    Args:
        ship_set (set): Set with tuples of new ships' coordinates
        blocks_for_manual_drawing (set): Set with all used blocks for other ships, including all blocks around ships.

    Returns:
        Bool: True if ships are not touching, False otherwise.
    """
    return ship_set.isdisjoint(blocks_for_manual_drawing)


def check_ships_numbers(ship, num_ships_list):
    """
    Checks if a ship of particular length (1-4) does not exceed necessary quantity (4-1).

    Args:
        ship (list): List with new ships' coordinates
        num_ships_list (list): List with numbers of particular ships on respective indexes.

    Returns:
        Bool: True if the number of ships of particular length is not greater than needed, 
            False if there are enough of such ships.
    """
    return (5 - len(ship)) > num_ships_list[len(ship)-1]


def update_used_blocks(ship, method):
    for block in ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                method((block[0]+i, block[1]+j))
