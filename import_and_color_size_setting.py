import pygame
import sys
import random
import copy

#COLORS
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN_BLUE = (0, 153, 153)
LIGHT_GRAY = (160, 160, 160)
RED = (255, 0, 0)

GREY = (35, 45, 55)
GREEN = (50, 200, 150)
BLUE = (50, 150, 200)	
RED = (250, 50, 100)

block_size = 40
left_margin = 4 * block_size
upper_margin = 2 * block_size
# 30 = 2x10 blocks width in two grids + hard-coded 5*blocks gap after each grid!
size = (left_margin + 28 * block_size, upper_margin + 15 * block_size)
LETTERS = "ABCDEFGHIJ"

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("C A R S T E N ` S    P  I  E  P  E  R  S  H  I  P  S")
# This ratio is purely for scaling the font according to the block size
font_size = int(block_size / 1.5)
font = pygame.font.SysFont('notosans', font_size)
game_over_font_size = 3 * block_size
game_over_font = pygame.font.SysFont('notosans', game_over_font_size)

### COMPUTER DATA ###
computer_available_to_fire_set = {(x, y)
                                for x in range(16, 26) for y in range(1, 11)}
around_last_computer_hit_set = set()
dotted_set_for_computer_not_to_shoot = set()
hit_blocks_for_computer_not_to_shoot = set()
last_hits_list = []
###################

hit_blocks = set()
dotted_set = set()
destroyed_computer_ships = []
