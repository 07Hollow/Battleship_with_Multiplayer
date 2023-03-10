from autoships import AutoShips
from import_and_color_size_setting import block_size, left_margin
from button import Button
import copy


# Create computer ships
computer = AutoShips(0)
computer_ships_working = copy.deepcopy(computer.ships)

# Create AUTO and MANUAL buttons and explanatory message for them
auto_button_place = left_margin + 17 * block_size
manual_button_place = left_margin + 20 * block_size
how_to_create_ships_message = "How do you want to create your ships? Click the button"
auto_button = Button(auto_button_place, "AUTO", how_to_create_ships_message)
manual_button = Button(manual_button_place, "MANUAL",
                       how_to_create_ships_message)

# Create UNDO message and button
undo_message = "To undo the last ship click the button"
undo_button_place = left_margin + 10 * block_size
undo_button = Button(undo_button_place, "UNDO LAST SHIP", undo_message)

# Create PLAY AGAIN and QUIT buttons and message for them
play_again_message = "Do you want to play again or quit?"
play_again_button = Button(
    left_margin + 15 * block_size, "PLAY AGAIN", play_again_message)
quit_game_button = Button(manual_button_place, "QUIT", play_again_message)
