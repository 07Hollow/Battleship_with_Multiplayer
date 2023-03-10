from import_and_color_size_setting import *
from create_ai_ship_and_buttons import computer
import random

def computer_shoots(set_to_shoot_from):
    """
    Randomly chooses a block from available to shoot from set
    """
    pygame.time.delay(500)
    computer_fired_block = random.choice(tuple(set_to_shoot_from))
    computer_available_to_fire_set.discard(computer_fired_block)
    return computer_fired_block


def check_hit_or_miss(fired_block, opponents_ships_list, computer_turn, opponents_ships_list_original_copy,
                      opponents_ships_set):
    """
    Checks whether the block that was shot at either by computer or by human is a hit or a miss.
    Updates sets with dots (in missed blocks or in diagonal blocks around hit block) and 'X's
    (in hit blocks).
    Removes destroyed ships from the list of ships.
    """
    for elem in opponents_ships_list:
        diagonal_only = True
        if fired_block in elem:
            # This is to put dots before and after a destroyed ship
            # and to draw computer's destroyed ships (which are hidden until destroyed)
            ind = opponents_ships_list.index(elem)
            if len(elem) == 1:
                diagonal_only = False
            update_dotted_and_hit_sets(
                fired_block, computer_turn, diagonal_only)
            elem.remove(fired_block)
            # This is to check who loses - if ships_set is empty
            opponents_ships_set.discard(fired_block)
            if computer_turn:
                last_hits_list.append(fired_block)
                update_around_last_computer_hit(fired_block, True)
            # If the ship is destroyed
            if not elem:
                update_destroyed_ships(
                    ind, computer_turn, opponents_ships_list_original_copy)
                if computer_turn:
                    last_hits_list.clear()
                    around_last_computer_hit_set.clear()
                else:
                    # Add computer's destroyed ship to the list to draw it (computer ships are hidden)
                    destroyed_computer_ships.append(computer.ships[ind])
            return True
    add_missed_block_to_dotted_set(fired_block)
    if computer_turn:
        update_around_last_computer_hit(fired_block, False)
    return False


def update_destroyed_ships(ind, computer_turn, opponents_ships_list_original_copy):
    """
    Adds blocks before and after a ship to dotted_set to draw dots on them.
    Adds all blocks in a ship to hit_blocks set to draw 'X's within a destroyed ship.
    """
    ship = sorted(opponents_ships_list_original_copy[ind])
    for i in range(-1, 1):
        update_dotted_and_hit_sets(ship[i], computer_turn, False)


def update_around_last_computer_hit(fired_block, computer_hits):
    """
    Updates around_last_computer_hit_set (which is used to choose for computer to fire from) if it
    hit the ship but not destroyed it). Adds to this set vertical or horizontal blocks around the
    block that was last hit. Then removes those block from that set which were shot at but missed.
    around_last_computer_hit_set makes computer choose the right blocks to quickly destroy the ship
    instead of just randomly shooting at completely random blocks.
    """
    global around_last_computer_hit_set, computer_available_to_fire_set
    if computer_hits and fired_block in around_last_computer_hit_set:
        around_last_computer_hit_set = computer_hits_twice()
    elif computer_hits and fired_block not in around_last_computer_hit_set:
        computer_first_hit(fired_block)
    elif not computer_hits:
        around_last_computer_hit_set.discard(fired_block)

    around_last_computer_hit_set -= dotted_set_for_computer_not_to_shoot
    around_last_computer_hit_set -= hit_blocks_for_computer_not_to_shoot
    computer_available_to_fire_set -= around_last_computer_hit_set
    computer_available_to_fire_set -= dotted_set_for_computer_not_to_shoot


def computer_first_hit(fired_block):
    """
    Adds blocks above, below, to the right and to the left from the block hit
    by computer to a temporary set for computer to choose its next shot from.
    Args:
        fired_block (tuple): coordinates of a block hit by computer
    """
    x_hit, y_hit = fired_block
    if x_hit > 16:
        around_last_computer_hit_set.add((x_hit - 1, y_hit))
    if x_hit < 25:
        around_last_computer_hit_set.add((x_hit + 1, y_hit))
    if y_hit > 1:
        around_last_computer_hit_set.add((x_hit, y_hit - 1))
    if y_hit < 10:
        around_last_computer_hit_set.add((x_hit, y_hit + 1))


def computer_hits_twice():
    """
    Adds blocks before and after two or more blocks of a ship to a temporary list
    for computer to finish the ship faster.
    Returns:
        set: temporary set of blocks where potentially a human ship should be
        for computer to shoot from
    """
    last_hits_list.sort()
    new_around_last_hit_set = set()
    for i in range(len(last_hits_list) - 1):
        x1 = last_hits_list[i][0]
        x2 = last_hits_list[i + 1][0]
        y1 = last_hits_list[i][1]
        y2 = last_hits_list[i + 1][1]
        if x1 == x2:
            if y1 > 1:
                new_around_last_hit_set.add((x1, y1 - 1))
            if y2 < 10:
                new_around_last_hit_set.add((x1, y2 + 1))
        elif y1 == y2:
            if x1 > 16:
                new_around_last_hit_set.add((x1 - 1, y1))
            if x2 < 25:
                new_around_last_hit_set.add((x2 + 1, y1))
    return new_around_last_hit_set


def update_dotted_and_hit_sets(fired_block, computer_turn, diagonal_only=True):
    """
    Puts dots in center of diagonal or all around a block that was hit (either by human or
    by computer). Adds all diagonal blocks or all-around chosen block to a separate set
    block: hit block (tuple)
    """
    global dotted_set
    x, y = fired_block
    a = 15 * computer_turn
    b = 11 + 15 * computer_turn
    # Adds a block hit by computer to the set of his hits to later remove
    # them from the set of blocks available for it to shoot from
    hit_blocks_for_computer_not_to_shoot.add(fired_block)
    # Adds hit blocks on either grid1 (x:1-10) or grid2 (x:16-25)
    hit_blocks.add(fired_block)
    # Adds blocks in diagonal or all-around a block to repsective sets
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (not diagonal_only or i != 0 and j != 0) and a < x + i < b and 0 < y + j < 11:
                add_missed_block_to_dotted_set((x + i, y + j))
    dotted_set -= hit_blocks


def add_missed_block_to_dotted_set(fired_block):
    """
    Adds a fired_block to the set of missed shots (if fired_block is a miss then) to then draw dots on them.
    Also needed for computer to remove these dotted blocks from the set of available blocks for it to shoot from.
    """
    dotted_set.add(fired_block)
    dotted_set_for_computer_not_to_shoot.add(fired_block)
