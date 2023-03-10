from import_and_color_size_setting import *
from create_ai_ship_and_buttons import *
from grid import Grid
from drawing import *
from shooting import check_hit_or_miss
import json
import time
from client_conn_win import username
from client_conn_win import on_message
from client_conn_win import connect_to_server
from client_conn_win import on_close
from client_conn_win import window




def enemy_shot(ws,message):
    msg_json = json.loads(message)
    if msg_json["type"] == "PLAYER_CHANGED":
       if msg_json["data"]["name"] == "Player2":
           if msg_json["type"] == "SHOT_FIRED":
                draw_from_dotted_set(dotted_set)
                draw_hit_blocks(hit_blocks)
           
     


def multiplayer(ws, message):
    msg_json = json.loads(message)
    ships_creation_not_decided = True
    ships_not_created = True
    drawing = False
    game_over = False
    computer_turn = False
    start = (0, 0)
    ship_size = (0, 0)

    rect_for_grids = (0, 0, size[0], upper_margin + 12 * block_size)
    rect_for_messages_and_buttons = (
        0, upper_margin + 11 * block_size, size[0], 5 * block_size)
    message_rect_for_drawing_ships = (undo_button.rect_for_draw[0] + undo_button.rect_for_draw[2], upper_margin + 11 * block_size, size[0]-(
        undo_button.rect_for_draw[0] + undo_button.rect_for_draw[2]), 4 * block_size)
    message_rect_computer = (left_margin - 2 * block_size, upper_margin +
                             11 * block_size, 14 * block_size, 4 * block_size)
    message_rect_human = (left_margin + 15 * block_size, upper_margin +
                          11 * block_size, 10 * block_size, 4 * block_size)

    human_ships_to_draw = []
    human_ships_set = set()
    used_blocks_for_manual_drawing = set()
    num_ships_list = [0, 0, 0, 0]

    screen.fill(GREY)
    computer_grid = Grid("ENEMY", 0)
    human_grid = Grid(username, 15)

    

    while connect_to_server(ws, message):
        if msg_json["type"] == "GAME_PHASE_CHANGED":
            if msg_json["data"]["phase"] == "SETUP": 
                while ships_creation_not_decided:
                    auto_button.draw_button()
                    manual_button.draw_button()
                    auto_button.change_color_on_hover()
                    manual_button.change_color_on_hover()
                    auto_button.print_message_for_button()

                    mouse = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_over = True
                            ships_creation_not_decided = False
                            ships_not_created = False
                        # If AUTO button is pressed - create human ships automatically
                        elif event.type == pygame.MOUSEBUTTONDOWN and auto_button.rect.collidepoint(mouse):
                            human = AutoShips(15)
                            human_ships_to_draw = human.ships
                            human_ships_working = copy.deepcopy(human.ships)
                            human_ships_set = human.ships_set
                            ships_creation_not_decided = False
                            ships_not_created = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and manual_button.rect.collidepoint(mouse):
                            ships_creation_not_decided = False

                    pygame.display.update()
                    screen.fill(GREY, rect_for_messages_and_buttons)


                while ships_not_created:
                    screen.fill(GREY, rect_for_grids)
                    computer_grid = Grid("Enemy", 0)
                    human_grid = Grid(username, 15)
                    mouse = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if on_close():
                            ships_not_created = False
                            game_over = True
                            pygame.QUIT
                            ws.close()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            drawing = True
                            x_start, y_start = event.pos
                            start = x_start, y_start
                            ship_size = (0, 0)
                        if drawing and event.type == pygame.MOUSEMOTION:
                            x_end, y_end = event.pos
                            end = x_end, y_end
                            ship_size = x_end - x_start, y_end - y_start
                        elif drawing and event.type == pygame.MOUSEBUTTONUP:
                            x_end, y_end = event.pos
                            drawing = False
                            ship_size = (0, 0)
                            start_block = ((x_start - left_margin) // block_size + 1,
                                           (y_start - upper_margin) // block_size + 1)
                            end_block = ((x_end - left_margin) // block_size + 1,
                                         (y_end - upper_margin) // block_size + 1)
                            if start_block > end_block:
                                start_block, end_block = end_block, start_block
                            temp_ship = []
                            if 15 < start_block[0] < 26 and 0 < start_block[1] < 11 and 15 < end_block[0] < 26 and 0 < end_block[1] < 11:
                                screen.fill(GREY, message_rect_for_drawing_ships)
                                if start_block[0] == end_block[0] and (end_block[1] - start_block[1]) < 4:
                                    for block in range(start_block[1], end_block[1]+1):
                                        temp_ship.append((start_block[0], block))
                                elif start_block[1] == end_block[1] and (end_block[0] - start_block[0]) < 4:
                                    for block in range(start_block[0], end_block[0]+1):
                                        temp_ship.append((block, start_block[1]))
                                else:
                                    show_message_at_rect_center(
                                        "SHIP IS TOO LARGE", message_rect_for_drawing_ships)
                            else:
                                show_message_at_rect_center(
                                    "SHIP IS BEYOND YOUR GRID", message_rect_for_drawing_ships)
                            if temp_ship:
                                temp_ship_set = set(temp_ship)
                                if ship_is_valid(temp_ship_set, used_blocks_for_manual_drawing):
                                    if check_ships_numbers(temp_ship, num_ships_list):
                                        num_ships_list[len(temp_ship) - 1] += 1
                                        human_ships_to_draw.append(temp_ship)
                                        human_ships_set |= temp_ship_set
                                        update_used_blocks(
                                            temp_ship, used_blocks_for_manual_drawing.add)
                                        data = {
                                        "type": "PLACE_SHIP",
                                        "data": {
                                            "x": x_start,
                                            "y": y_start,
                                            "length": ship_size,
                                            "direction": ship_size
                                             }
                                         }
                                        ws.send(json.dumps(data))
                                        i += 1
                                    else:
                                        show_message_at_rect_center(
                                            f"There already are enough of {len(temp_ship)} ships!", message_rect_for_drawing_ships)
                                else:
                                    show_message_at_rect_center(
                                        "SHIPS ARE TOUCHING", message_rect_for_drawing_ships)
                        if len(human_ships_to_draw) == 10:
                            ships_not_created = False
                            human_ships_working = copy.deepcopy(human_ships_to_draw)
                            screen.fill(GREY, rect_for_messages_and_buttons)
                    pygame.draw.rect(screen, GREEN, (start, ship_size), 3)
                    draw_ships(human_ships_to_draw)
                    pygame.display.update()

                while not game_over:
                    if msg_json["type"] == "GAME_PHASE_CHANGED":
                        if msg_json["data"]["phase"] == "IN_PROGRESS":
                            draw_ships(human_ships_to_draw)
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    game_over = True
                                    on_close()
                                    ws.close()
                                if msg_json["type"] == "PLAYER_CHANGED":
                                    if msg_json["data"]["name"] == "Player1":
                                        while msg_json["data"]["name"] == "Player1":
                                            show_message_at_rect_center("GAME STARTED! YOUR MOVE!", message_rect_computer)
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                x, y = event.pos
                                    if (left_margin < x < left_margin + 10 * block_size) and (
                                        upper_margin < y < upper_margin + 10 * block_size):
                                        fired_block = ((x - left_margin) // block_size + 1,
                                                   (y - upper_margin) // block_size + 1)
                                        
                                        data = {
                                        "type": "FIRE_SHOT",
                                        "data": {
                                        "x": (x - left_margin) // block_size + 1,
                                        "y": (y - upper_margin) // block_size + 1,
                                            }
                                        }
                                        ws.send(json.dumps(data))
                                        time.sleep(2.5)
                                        
                                    if msg_json["data"] == "SHOT_FIRED":
                                        if msg_json["type"]["result"] == "MISS":
                                            draw_from_dotted_set(dotted_set)
                                            if msg_json["type"] == "PLAYER_CHANGED":
                                                if msg_json["data"]["name"] == "Player2":
                                                    enemy_shot()
                                    if msg_json["type"] == "SHOT_FIRED":
                                        if msg_json["data"]["result"] == "HIT":
                                            draw_hit_blocks(hit_blocks)
                                    screen.fill(GREY, message_rect_computer)
                                    show_message_at_rect_center(
                                        f"Your last shot: {LETTERS[fired_block[0]-1] + str(fired_block[1])}", message_rect_computer, color=BLACK)

                                else:
                                    show_message_at_rect_center("Your shot is outside of grid", message_rect_computer)

                            if not human_ships_set:
                                show_message_at_rect_center(
                                    "YOU LOST!", (0, 0, size[0], size[1]), game_over_font)
                                game_over = True
                            pygame.display.update()

                while on_close():

                    screen.fill(LIGHT_GRAY, rect_for_messages_and_buttons)
                    play_again_button.draw_button()
                    play_again_button.print_message_for_button()
                    play_again_button.change_color_on_hover()
                    quit_game_button.draw_button()
                    quit_game_button.change_color_on_hover()

                    mouse = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and play_again_button.rect.collidepoint(mouse):
                            window.mainloop()
                        elif event.type == pygame.MOUSEBUTTONDOWN and quit_game_button.rect.collidepoint(mouse):
                            ws.close()
                            pygame.quit()
                            sys.exit()
                    pygame.display.update()


multiplayer()
