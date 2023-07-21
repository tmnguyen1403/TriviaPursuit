#Set up path to load other modules
import sys
import os
import subprocess

subprocess.run(["python3 -m pip install $(cat requirements.txt)"], shell=True)
current_dir = os.path.dirname(os.path.abspath(__file__))
parrent_dir = os.path.dirname(current_dir)
sys.path.append(parrent_dir)

import pygame
import asyncio
from database import dummy_database, create_with_online_database
from player import Player, PlayerManager
from gameboard import Tile, TileGenerator, Gameboard, MoveCalculator, GameBoardRenderer
from dice import Dice, DiceManager, DiceRenderer
from game_manager import GameManager, GameState
from question import Question, QuestionManager, QuestionRenderer, AnswerRenderer
from buttons import Button, ButtonManager,ButtonRenderer
from utils import Color
from question_display_screen import QuestionDisplayScreen
pygame.init()
clock = pygame.time.Clock()

# Set screen size
screen_width = 1200
screen_height = 800

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
# Define colors
tile_matrix = [[0,2,1,4,3,2,1,4,0],
                [3,-1,-1,-1,2,-1,-1,-1,3],
                [4,-1,-1,-1,1,-1,-1,-1,2],
                [1,-1,-1,-1,4,-1,-1,-1,1],
                [2,1,4,3,5,1,2,3,4],
                [3,-1,-1,-1,2,-1,-1,-1,3],
                [4,-1,-1,-1,3,-1,-1,-1,2],
                [1,-1,-1,-1,4,-1,-1,-1,1],
                [0,2,3,4,1,2,3,4,0]]
colors = {0: Color.WHITE.value, 1: Color.BLUE.value, 2: Color.YELLOW.value, 3: Color.RED.value, 4: Color.GREEN.value, 5: Color.SPECIAL.value}
categories = {0: "", 1: "Math", 2: "Sport", 3: "History", 4: "Movie", 5: "Random"}
action_types = {0: "", 1: "", 2: "", 3: "", 4: "", 5: "Special"}
board_x = 100
board_y = 100
board_width = 600
board_height = 600
board_rect = (board_x, board_y, board_width, board_height)
tile_generator = TileGenerator(categories=categories, tile_matrix=tile_matrix,colors=colors, tile_types=action_types, board_rect=board_rect)
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
tile_info = (tile_matrix, tile_map, tile_objects)
gameboard = Gameboard(question_database, tile_info, move_calculator)
gameboard_renderer = GameBoardRenderer()

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
#question_screen_display
question_display_screen = QuestionDisplayScreen()
#game_manager.set_state(GameState.QUESTION_SELECTION)
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
                if current_state == GameState.WAIT_ROLL:
                    if dice_manager.can_roll(mouse_pos=mouse_pos):
                        dice_manager.animate(screen=screen,pygame=pygame,clock=clock)
                        dice_value = dice_manager.roll_value()
                        player_pos = player_manager.get_current_player_position()
                        possible_moves = gameboard.get_possible_moves(player_pos=player_pos, dice_value=dice_value)
                        game_manager.next_state()
                        update_board = True
                elif current_state == GameState.MOVE_SELECTION:
                    move_success = gameboard.move(mouse_pos=mouse_pos)
                    if move_success:
                        game_manager.next_state()
                        update_board = True
                        print(f"Move success {move_success}")
                        print("Update the player position, reset tile state")
    
    if init_board:
        screen.fill((125,125,125))
        init_board = False
        dice_manager.draw(screen=screen)
        pygame.draw.rect(screen, Color.WHITE.value, (board_x,board_y,board_width,board_height))

    if update_board:
        gameboard_renderer.render(tile_objects=tile_objects, engine=pygame, screen=screen)
        gameboard_renderer.render_player(gameboard=gameboard, engine=pygame, screen=screen,player_manager=player_manager)
        current_player = player_manager.get_current_player()
        player_name = current_player.get_name()
        print(f"Current player name {player_name}")
        player_text = player_font.render(f"Player {player_name}", True, (0,0,0,0))
        screen.blit(player_text, (board_x + board_width + 50,board_y - 50))
        update_board = False
    
    current_state = game_manager.get_state()
    if current_state == GameState.QUESTION_SELECTION:
        current_question = question_manager.get_current_question()
        print("Current question: ", current_question)
        question_display_screen.render_screen(pygame=pygame, screen=screen, game_manager=game_manager, question=current_question)
    else:
        if current_state == GameState.ACCEPT_ANSWER:
            print("Stay on the current player:")
            game_manager.reset()
            render_efficient_reset()
        elif current_state == GameState.REJECT_ANSWER:
            player_manager.next_player()
            game_manager.reset()
            render_efficient_reset()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()