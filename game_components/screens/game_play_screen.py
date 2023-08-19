# Set up path to load other modules
# Set up PYTHONPATH
import sys
import os
import subprocess

try:
    import pygame
except Exception as e:
    print("Attemp to install packages")
    subprocess.run(["python3 -m pip install $(cat requirements.txt)"], shell=True)
# Add Python path to help import
current_dir = os.path.dirname(os.path.abspath(__file__))
parrent_dir = os.path.dirname(current_dir)
sys.path.append(parrent_dir)

# Import dependencies
import asyncio
from database import create_with_online_database
from player import Player, PlayerManager
from gameboard import TileType, TileInfo, TileGenerator, Gameboard, MoveCalculator, GameBoardRenderer, Legend
from dice import Dice, DiceManager, DiceRenderer
from games import GameManager, GameState
from question import QuestionManager
from utils_local import Color, is_point_inside_rect
from question_display_screen import QuestionDisplayScreen
from trivial_compute_select_screen import TrivialComputeSelectScreen
from intermediate_winner_screen import IntermediateWinnerScreen
from in_game_menu import InGameMenu
from sounds import Sound, SoundType
from games import GamePlayInfo
from buttons import Button, ButtonRenderer
from option_screen import OptionScreen

'''
The below is used to generate
'''
# Define category_colors
class GamePlayScreen:
    def __init__(self, game_info: 'GamePlayInfo', music_handler: 'Sound') -> None:
        self.init_board = True
        self.update_board = True
        self.nb_player = game_info.get_nb_player()
        self.categories = game_info.get_categories()
        self.player_names = game_info.get_player_names()
        self.button_renderer = ButtonRenderer(pygame)
        self.music_handler = music_handler

    def init_screen(self, screen):
        pass
    
    async def main_database(self, category_list):
        print(f"Main database: {category_list}")
        result = await create_with_online_database(categories=category_list)
        return result
    
    def render_efficient_reset(self):
        self.init_board = True
        self.update_board = True

    def render_screen(self, pygame, screen):

        screen_width, screen_height = screen.get_size()

        # Player Dummy Generator
        
        players = []
        player_colors = {1: Color.BLUE.value, 2: Color.YELLOW.value, 3: Color.RED.value, 4: Color.GREEN.value}
        for i in range(self.nb_player):
            player_info = {"position": (0, 0), "name": self.player_names[i], "token": None, "score": [], "color": player_colors[i + 1]}
            players.append(Player(player_info))
        player_manager = PlayerManager(players=players)

        tile_matrix = [[-1, 1, 0, 3, 1, 2, 0, 1, -1],
                    [2, -9, -9, -9, 2, -9, -9, -9, 2],
                    [3, -9, -9, -9, 0, -9, -9, -9, 1],
                    [1, -9, -9, -9, 3, -9, -9, -9, 0],
                    [2, 0, 3, 2, -2, 0, 1, 2, 3],
                    [0, -9, -9, -9, 1, -9, -9, -9, 2],
                    [3, -9, -9, -9, 2, -9, -9, -9, 1],
                    [1, -9, -9, -9, 3, -9, -9, -9, 0],
                    [-1, 1, 2, 3, 0, 1, 2, 3, -1]]
        head_quater_map = [(0, 4), (4, 0), (4, 8), (8, 4)]
        trivial_compute_map = [(4, 4)]

        special_tile_infos = {
            -1: TileInfo(Color.WHITE.value, TileType.FREEROLL),
            -2: TileInfo(Color.SPECIAL.value, TileType.TRIVIA_COMPUTE),
        }
       
        # for category in self.categories.items
        normal_tile_infos = {}
        for index, category in enumerate(self.categories):
            color = category.get_color()
            normal_tile_infos[index] = TileInfo(color=color, tile_type=TileType.NORMAL)

        board_x = 250
        board_y = 200
        board_width = 700
        board_height = 700
        board_rect = (board_x, board_y, board_width, board_height)
        tile_generator = TileGenerator(categories=self.categories, tile_matrix=tile_matrix, normal_info=normal_tile_infos,
                                    special_info=special_tile_infos, board_rect=board_rect,
                                    head_quater_map=head_quater_map, trivial_compute_map=trivial_compute_map)
        tile_objects, tile_map = tile_generator.generate()

        #Create category list to use in database
        # category_list = []
        # for key, category in self.categories.items():
        #     if category == "Random" or category == "":
        #         continue
        #     category_list.append(category)

        question_database = asyncio.run(self.main_database(self.categories))

        move_calculator = MoveCalculator(cant_move=-9)
        tile_info = (tile_matrix, head_quater_map, tile_map, tile_objects)
        gameboard = Gameboard(tile_info, move_calculator)
        gameboard_renderer = GameBoardRenderer()
        score_board_rect = (150, 25, 90, 90)
       
        category_colors = [tile_info.get_color() for tile_info in normal_tile_infos.values()]
        player_manager.init_player_score(category_colors=category_colors, rect_size=score_board_rect)
        
        # Die
        die_width = 100
        die_height = 100
        die_x = board_x + board_width + 20
        die_y = board_y + board_height // 2
        die_color = (0, 0, 0)
        die_text_color = (255, 255, 255)
        die_font = pygame.font.Font(None, 64)
        dice = Dice((die_x, die_y), (die_width, die_height), die_color, die_text_color)
        dice_renderer = DiceRenderer(pygame, die_font)
        dice_manager = DiceManager(dice=dice, dice_renderer=dice_renderer)

        # Music
        # music_handler = Sound(screen)
        self.music_handler.play(SoundType.GAME_MUSIC)

        # Options
        option_screen = OptionScreen(self.music_handler)
        options_button = Button(position=(0, screen_height - 50), size=(100, 50), color=Color.BLACK.value, text='Options', text_color=Color.WHITE.value, action=None)

        player_manager.update_all(gameboard.get_center())

        # Create the game board surface
        pygame.display.set_caption("Trivial Compute Game Board")
        running = True
        game_manager = GameManager()

        question_manager = QuestionManager(database=question_database)

        gameboard.subscribe(question_manager)
        gameboard.subscribe(player_manager)


        question_display_screen = QuestionDisplayScreen()
        category_names = [category_info.get_name() for category_info in self.categories]
        trivial_compute_select_screen = TrivialComputeSelectScreen(categories=category_names)
        intermediate_winner_screen = IntermediateWinnerScreen(screen=screen, max_display_time_second=3)
        '''
        Debug 
        '''
        DEBUG_WITH_DICE = True
        dice_debug_value = 0

        clock = pygame.time.Clock()

        in_game_menu = InGameMenu(screen=screen)
        tile_animation_clock = None
        animation_update_time = 0.5
        animation_time_pass = 0
        while running:
            # Without doing pygame.event.get(), the game will not be rendered
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print(f"Showing exit menu")
                        in_game_menu.draw(pygame)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        current_state = game_manager.get_state()
                        mouse_pos = pygame.mouse.get_pos()
                        print("Mouse clicking ", current_state)
                        if current_state == GameState.WAIT_ROLL:
                            if is_point_inside_rect(mouse_pos, options_button.get_rect()):
                                game_manager.set_state(GameState.OPTIONS)
                            if dice_manager.can_roll(mouse_pos=mouse_pos):
                                dice_manager.animate(screen=screen, pygame=pygame, clock=clock,
                                                        debug_value=dice_debug_value)
                                dice_value = dice_manager.roll_value()
                                dice_debug_value = 0
                                # First turn and roll 6(default special dice value)
                                if player_manager.is_first_turn() and dice_manager.is_special_value(dice_value=dice_value):
                                    possible_moves = gameboard.get_headquarter_moves()
                                else:
                                    player_pos = player_manager.get_current_player_position()
                                    possible_moves = gameboard.get_possible_moves(player_pos=player_pos,
                                                                                    dice_value=dice_value)
                                game_manager.set_state(GameState.MOVE_SELECTION)

                                tile_animation_clock = pygame.time.Clock()
                                self.update_board = True
                        elif current_state == GameState.MOVE_SELECTION:
                            move_success = gameboard.move(mouse_pos=mouse_pos)
                            if move_success:
                                selected_tile = gameboard.get_selected_tile()
                                tile_type = selected_tile.get_type()
                                if tile_type == TileType.FREEROLL:
                                    print(f"Land on freeroll tile, player roll again")
                                    game_manager.set_state(GameState.RESET_STATE)
                                elif tile_type == TileType.TRIVIA_COMPUTE:
                                    print(f"Land on Trivia Compute")
                                    game_manager.set_state(GameState.TRIVIA_COMPUTE_SELECTION)
                                else:
                                    game_manager.set_state(GameState.QUESTION_SELECTION)
                                self.update_board = True
                                print(f"Move success {move_success}")
                                print("Update the player position, reset tile state")
                        if in_game_menu.is_active():
                            print("Check Ingame Menu")
                            is_handled = in_game_menu.handle_click(pygame)
                            if is_handled and in_game_menu.is_quit_game():
                                running = False
                                self.music_handler.stop()
                                return

            # DEBUG
            keys = pygame.key.get_pressed()
            if DEBUG_WITH_DICE:
                dice_values = [pygame.K_0 + index for index in range(1, 10)]
                for key_code in dice_values:
                    if keys[key_code]:
                        dice_debug_value = key_code - pygame.K_0
                        print(f"Key {dice_debug_value} is pressed")
            # End Debug

            if self.init_board:
                screen.fill(Color.DEFAULT_SCREEN.value)
                self.init_board = False
                dice_manager.draw(screen=screen)

                #draw the legend
                legend_rect = (25, 250, 200, 500)
                legend = Legend(self.categories, legend_rect)
                legend.draw(engine=pygame, screen=screen)

                # # Draw the big black box to be the game board
                pygame.draw.rect(screen, Color.BLACK.value, (board_x,board_y,board_width,board_height))

                #draw four white squares to separate spokes
                w_square_size = (0.32 * board_width)
                for i in range(2):
                    for j in range(2):
                        w_square_x = board_x + ((0.12 * board_width) * (i+1)) + (w_square_size*i)
                        w_square_y = board_y + ((0.12 * board_width) * (j+1)) + (w_square_size*j)

                        pygame.draw.rect(screen, Color.WHITE.value, (w_square_x, w_square_y, 
                                                            w_square_size, w_square_size))

                self.button_renderer.draw(screen=screen, button=options_button, font=pygame.font.Font(None, 32))

            if self.update_board:
                gameboard_renderer.render(tile_objects=tile_objects, engine=pygame, screen=screen)
                gameboard_renderer.render_player(gameboard=gameboard, engine=pygame, screen=screen,
                                                player_manager=player_manager)
                gameboard_renderer.render_player_score(engine=pygame, screen=screen, player_manager=player_manager)
                self.update_board = False
            
            if tile_animation_clock and game_manager.get_state() == GameState.MOVE_SELECTION:
                dt = tile_animation_clock.tick(60)/1000
                #print(f"dt passed: {dt}")
                for tile in tile_objects:
                    tile.draw_move_candidate(pygame, screen, dt)

            current_state = game_manager.get_state()

            if current_state == GameState.END_GAME:
                #continue
                in_game_menu.draw(pygame)
                #print("Render end game state")
                
            if current_state == GameState.TRIVIA_COMPUTE_SELECTION:
                print('TRIVIAL COMPUTE')
                selected_category = trivial_compute_select_screen.render_screen(pygame=pygame, screen=screen, current_player=player_manager.get_current_player().get_name(),
                all_scored=player_manager.player_score_all_category())
                question_manager.set_question(selected_category)
                #current_question = question_manager.get_current_question()
                # print("Current question: ", current_question)
                # question_display_screen.render_screen(pygame=pygame, screen=screen, game_manager=game_manager,
                #                                     question=current_question)
                game_manager.set_state(GameState.QUESTION_SELECTION)

            if current_state == GameState.QUESTION_SELECTION:
                current_question = question_manager.get_current_question()
                print("Current question: ", current_question)
                new_game_state = question_display_screen.render_screen(pygame=pygame, screen=screen,
                                                    question=current_question)
                game_manager.set_state(new_game_state)
            else:
                if current_state == GameState.ACCEPT_ANSWER:
                    print("Stay on the current player:")
                    player_manager.update_player_score()
                    game_manager.set_state(GameState.RESET_STATE)
                    if player_manager.is_current_player_win():
                        if player_manager.is_last_player_move():
                            game_manager.set_state(GameState.END_GAME)      
                        else:
                            intermediate_winner_screen.render_screen(pygame, screen)
                        player_manager.next_player()
                            
                elif current_state == GameState.REJECT_ANSWER:
                    if player_manager.has_winner() and player_manager.is_last_player_move():
                        game_manager.set_state(GameState.END_GAME)
                        player_manager.next_player()
                    else:
                        game_manager.set_state(GameState.RESET_STATE)
                    player_manager.next_player()

            current_state = game_manager.get_state()
            if current_state == GameState.RESET_STATE:
                game_manager.reset()
                self.render_efficient_reset()
            elif current_state == GameState.END_GAME:
                player_manager.set_game_end(True)
                self.render_efficient_reset()

            if current_state == GameState.OPTIONS:
                print(game_manager.get_state())
                option_screen.render_screen(pygame, screen=screen)
                game_manager.reset()
                self.render_efficient_reset()

            pygame.display.flip()
            clock.tick(60)
