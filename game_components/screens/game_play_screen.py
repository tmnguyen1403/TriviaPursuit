#Set up path to load other modules
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

#Import dependencies 
import pygame
import asyncio
from database import dummy_database, create_with_online_database
from player import Player, PlayerManager
from gameboard import Tile, TileType, TileGenerator, Gameboard, MoveCalculator, GameBoardRenderer
from dice import Dice, DiceManager, DiceRenderer
from game_manager import GameManager, GameState
from question import Question, QuestionManager, QuestionRenderer, AnswerRenderer
from buttons import Button, ButtonManager,ButtonRenderer
from utils import Color
from question_display_screen import QuestionDisplayScreen
from landing_screen import LandingScreen

pygame.init()
clock = pygame.time.Clock()

# Set screen size
screen_width = 1200
screen_height = 1000

# Player Dummy Generator
nb_player = 4
players = []
player_font  = pygame.font.Font(None, 32)
player_colors = {1: Color.BLUE.value, 2: Color.YELLOW.value, 3: Color.RED.value, 4: Color.GREEN.value}
for i in range(4):
    player_info = {"position": (0,0), "name": f"P{i+1}", "token": None, "score": [], "color": player_colors[i+1]}
    players.append(Player(player_info))
player_manager = PlayerManager(players=players)

'''
The below is used to generate
'''
# Define category_colors
tile_matrix = [[0,2,1,4,3,2,1,4,0],
                [3,-1,-1,-1,2,-1,-1,-1,3],
                [4,-1,-1,-1,1,-1,-1,-1,2],
                [1,-1,-1,-1,4,-1,-1,-1,1],
                [2,1,4,3,5,1,2,3,4],
                [3,-1,-1,-1,2,-1,-1,-1,3],
                [4,-1,-1,-1,3,-1,-1,-1,2],
                [1,-1,-1,-1,4,-1,-1,-1,1],
                [0,2,3,4,1,2,3,4,0]]
head_quater_map = [(0,4),(4,0),(4,8),(8,4)]
category_colors = {0: Color.WHITE.value, 1: Color.BLUE.value, 2: Color.YELLOW.value, 3: Color.RED.value, 4: Color.GREEN.value, 5: Color.SPECIAL.value}
categories = {0: "", 1: "Math", 2: "Sport", 3: "History", 4: "Movie", 5: "Random"}
action_types = {0: TileType.FREEROLL, 1: TileType.NORMAL, 2: TileType.NORMAL, 3: TileType.NORMAL, 4: TileType.NORMAL, 5: TileType.TRIVIA_COMPUTE}
board_x = 100
board_y = 200
board_width = 600
board_height = 600
board_rect = (board_x, board_y, board_width, board_height)
tile_generator = TileGenerator(categories=categories, tile_matrix=tile_matrix,colors=category_colors, tile_types=action_types, board_rect=board_rect,
head_quater_map=head_quater_map)
tile_objects, tile_map = tile_generator.generate()


category_list = []
for  key, category in categories.items():
    if category == "Random" or category == "":
        continue
    category_list.append(category)
async def main_database(category_list):
    print(f"Main database: {category_list}")
    result = await create_with_online_database(categories=category_list)
    return result
question_database = asyncio.run(main_database(category_list))

move_calculator = MoveCalculator(-1)
tile_info = (tile_matrix, head_quater_map, tile_map, tile_objects)
gameboard = Gameboard(tile_info, move_calculator)
gameboard_renderer = GameBoardRenderer()
score_board_rect = (150,25,90,90)
player_manager.init_player_score(category_colors=category_colors,rect_size=score_board_rect)
# Die
die_width = 100
die_height = 100
die_x = board_x + board_width +20
die_y = board_y + board_height // 2
die_color = (0, 0, 0)
die_text_color = (255, 255, 255)
die_font = pygame.font.Font(None, 64)
dice = Dice((die_x, die_y), (die_width, die_height), die_color, die_text_color)
dice_renderer = DiceRenderer(pygame, die_font)
dice_manager = DiceManager(dice=dice,dice_renderer=dice_renderer)


player_manager.update_all(gameboard.get_center())

#Can only have one screen, create another screen will overide existing screen
screen = pygame.display.set_mode((screen_width, screen_height))
# Create the game board surface
pygame.display.set_caption("Board Game Board")
running = True
roll = False
game_manager = GameManager()

# Init Question
question_position = {"x": board_x + board_width, "y": 150}
question_text_color = (0,0,0)
question_font = pygame.font.Font(None, 64)
question_renderer = QuestionRenderer(screen=screen, position=question_position, text_color=question_text_color)
question_manager = QuestionManager(database=question_database)

#Init Answer
answer_font  = pygame.font.Font(None, 50)
answer_position  = (question_position["x"], question_position["y"]+ 200)
answer_color = (0,0,255)
answer_renderer = AnswerRenderer(position=answer_position, text_color=answer_color)
# Button creator


gameboard.subscribe(question_manager)
gameboard.subscribe(player_manager)
init_board = True
update_board = True
def render_efficient_reset():
    global init_board
    global update_board
    init_board = True
    update_board = True

'''
Screens Init 
'''
landing_screen = LandingScreen()
question_display_screen = QuestionDisplayScreen()

'''
Debug 
'''
#game_manager.set_state(GameState.QUESTION_SELECTION)
DEBUG = False
DEBUG_WITH_DICE = True
dice_debug_value = 0

while running:
    #Without doing pygame.event.get(), the game will not be rendered
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                current_state = game_manager.get_state()
                mouse_pos = pygame.mouse.get_pos()
                print("Mouse clicking ", current_state)
                if DEBUG == True:
                    print("Debugging, bypass everything")
                    gameboard.move_debug()
                    move_success = gameboard.move(mouse_pos=mouse_pos)
                    if player_manager.player_score_all_category() == True:
                        print("Player score all, move to next player")
                        player_manager.next_player()
                        render_efficient_reset()
                        continue
                    if move_success:
                        selected_tile = gameboard.get_selected_tile()
                        tile_type = selected_tile.get_type()
                        if tile_type == TileType.FREEROLL:
                            print(f"Land on freeroll tile, player roll again")
                        elif tile_type == TileType.TRIVIA_COMPUTE:
                            print(f"Land on Trivia Compute")
                        else:
                            game_manager.next_state()
                        update_board = True
                        print(f"Move success {move_success}")
                        print("Update the player position, reset tile state")
                        game_manager.set_state(GameState.ACCEPT_ANSWER)
                else:
                    if current_state == GameState.WAIT_ROLL:
                        if dice_manager.can_roll(mouse_pos=mouse_pos):
                            dice_manager.animate(screen=screen,pygame=pygame,clock=clock, debug_value=dice_debug_value)
                            dice_value = dice_manager.roll_value()

                            # First turn and roll 6(default special dice value)
                            if player_manager.is_first_turn() and dice_manager.is_special_value(dice_value=dice_value):
                                possible_moves = gameboard.get_headquarter_moves()
                            else:
                                player_pos = player_manager.get_current_player_position()
                                possible_moves = gameboard.get_possible_moves(player_pos=player_pos, dice_value=dice_value)
                            game_manager.set_state(GameState.MOVE_SELECTION)

                            update_board = True
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
                            update_board = True
                            print(f"Move success {move_success}")
                            print("Update the player position, reset tile state")
    
    current_state = game_manager.get_state()
    if current_state == GameState.LANDING_SCREEN:
        landing_screen.render_screen(pygame=pygame,screen=screen,game_manager=game_manager,question=None)
    
    # DEBUG
    if DEBUG_WITH_DICE:
        dice_values = [pygame.K_0 + index for index in range(1,10)]
        keys = pygame.key.get_pressed()
        for key_code in dice_values:
            if keys[key_code]:
                dice_debug_value = key_code - pygame.K_0
                print(f"Key {dice_debug_value} is pressed")
    # End Debug

    if init_board:
        screen.fill(Color.DEFAULT_SCREEN.value)
        init_board = False
        dice_manager.draw(screen=screen)
        pygame.draw.rect(screen, Color.WHITE.value, (board_x,board_y,board_width,board_height))

    if update_board:
        gameboard_renderer.render(tile_objects=tile_objects, engine=pygame, screen=screen)
        gameboard_renderer.render_player(gameboard=gameboard, engine=pygame, screen=screen,player_manager=player_manager)
        gameboard_renderer.render_player_score(engine=pygame, screen=screen,player_manager=player_manager)
        update_board = False
    
    current_state = game_manager.get_state()
    
    if current_state == GameState.END_GAME:

        #player_manager.current_index
        #print(f"Current State after mouse event check: {current_state}")
        print("Render end game state")
        #continue
    if current_state == GameState.TRIVIA_COMPUTE_SELECTION:
        print("Trivia Compute - waiting to select category")
        if player_manager.player_score_all_category():
            print("Player wait for other player to select category")
            game_manager.set_state(GameState.QUESTION_SELECTION)
        else:
            print("Player can choose your own category")
            game_manager.set_state(GameState.QUESTION_SELECTION)
        update_board = True

    elif current_state == GameState.QUESTION_SELECTION:
        current_question = question_manager.get_current_question()
        print("Current question: ", current_question)
        question_display_screen.render_screen(pygame=pygame, screen=screen, game_manager=game_manager, question=current_question)
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
        render_efficient_reset()
        if player_manager.has_winner() and player_manager.is_last_player_move():
            print("We has a winner\n")
            game_manager.set_state(GameState.END_GAME)    

    pygame.display.flip()
    clock.tick(60)
pygame.quit()