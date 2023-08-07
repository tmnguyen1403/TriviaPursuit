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
from utils_local import Color
from question_display_screen import QuestionDisplayScreen
from trivial_compute_select_screen import TrivialComputeSelectScreen

'''
The below is used to generate
'''
# Define category_colors
class GamePlayScreen:
    def __init__(self, game_info: 'GamePlayInfo') -> None:
        self.init_board = True
        self.update_board = True
        self.nb_player = game_info.get_nb_player()
        self.categories = game_info.get_categories()

    def init_screen(self,screen):
        pass
    
    async def main_database(self, category_list):
        print(f"Main database: {category_list}")
        result = await create_with_online_database(categories=category_list)
        return result
    
    def render_efficient_reset(self):
        self.init_board = True
        self.update_board = True

    def render_screen(self, pygame, screen):

        # Player Dummy Generator
        
        players = []
        player_colors = {1: Color.BLUE.value, 2: Color.YELLOW.value, 3: Color.RED.value, 4: Color.GREEN.value}
        for i in range(self.nb_player):
            player_info = {"position": (0, 0), "name": f"P{i + 1}", "token": None, "score": [], "color": player_colors[i + 1]}
            players.append(Player(player_info))
        player_manager = PlayerManager(players=players)

        tile_matrix = [[-1, 1, 0, 3, 2, 1, 0, 3, -1],
                    [2, -10, -10, -10, 1, -10, -10, -10, 2],
                    [3, -10, -10, -10, 0, -10, -10, -10, 1],
                    [1, -10, -10, -10, 3, -10, -10, -10, 0],
                    [2, 0, 3, 2, -2, 0, 1, 2, 3],
                    [2, -10, -10, -10, 1, -10, -10, -10, 2],
                    [3, -10, -10, -10, 2, -10, -10, -10, 1],
                    [1, -10, -10, -10, 3, -10, -10, -10, 0],
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

        move_calculator = MoveCalculator(-10)
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

        '''
        Debug 
        '''
        DEBUG_WITH_DICE = True
        dice_debug_value = 0

        clock = pygame.time.Clock()

        while running:
            # Without doing pygame.event.get(), the game will not be rendered
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        current_state = game_manager.get_state()
                        mouse_pos = pygame.mouse.get_pos()
                        print("Mouse clicking ", current_state)
                        if current_state == GameState.WAIT_ROLL:
                            if dice_manager.can_roll(mouse_pos=mouse_pos):
                                dice_manager.animate(screen=screen, pygame=pygame, clock=clock,
                                                        debug_value=dice_debug_value)
                                dice_value = dice_manager.roll_value()

                                # First turn and roll 6(default special dice value)
                                if player_manager.is_first_turn() and dice_manager.is_special_value(dice_value=dice_value):
                                    possible_moves = gameboard.get_headquater_moves()
                                else:
                                    player_pos = player_manager.get_current_player_position()
                                    possible_moves = gameboard.get_possible_moves(player_pos=player_pos,
                                                                                    dice_value=dice_value)
                                game_manager.set_state(GameState.MOVE_SELECTION)

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

            current_state = game_manager.get_state()
            # DEBUG
            if DEBUG_WITH_DICE:
                dice_values = [pygame.K_0 + index for index in range(1, 10)]
                keys = pygame.key.get_pressed()
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

            if self.update_board:
                gameboard_renderer.render(tile_objects=tile_objects, engine=pygame, screen=screen)
                gameboard_renderer.render_player(gameboard=gameboard, engine=pygame, screen=screen,
                                                player_manager=player_manager)
                gameboard_renderer.render_player_score(engine=pygame, screen=screen, player_manager=player_manager)
                self.update_board = False

            current_state = game_manager.get_state()

            if current_state == GameState.END_GAME:
                print("Render end game state")
                
            if current_state == GameState.TRIVIA_COMPUTE_SELECTION:
                print('TRIVIAL COMPUTE')
                selected_category = trivial_compute_select_screen.render_screen(pygame=pygame, screen=screen, current_player=player_manager.get_current_player().get_name(),
                all_scored=player_manager.player_score_all_category())
                question_manager.set_question(selected_category)
                current_question = question_manager.get_current_question()
                print("Current question: ", current_question)
                question_display_screen.render_screen(pygame=pygame, screen=screen, game_manager=game_manager,
                                                    question=current_question)

            elif current_state == GameState.QUESTION_SELECTION:
                current_question = question_manager.get_current_question()
                print("Current question: ", current_question)
                question_display_screen.render_screen(pygame=pygame, screen=screen, game_manager=game_manager,
                                                    question=current_question)
            else:
                if current_state == GameState.ACCEPT_ANSWER:
                    print("Stay on the current player:")
                    player_manager.update_player_score()
                    game_manager.set_state(GameState.RESET_STATE)
                elif current_state == GameState.REJECT_ANSWER:
                    player_manager.next_player()
                    game_manager.set_state(GameState.RESET_STATE)
        

            current_state = game_manager.get_state()
            if current_state == GameState.RESET_STATE:
                game_manager.reset()
                self.render_efficient_reset()
                if player_manager.has_winner():
                    player_manager.next_player()
                    if player_manager.is_last_player_move():
                        print("We has a winner\n")
                        game_manager.set_state(GameState.END_GAME)
            pygame.display.flip()
            clock.tick(60)
