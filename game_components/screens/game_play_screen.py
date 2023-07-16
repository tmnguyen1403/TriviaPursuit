import pygame

from database import dummy_database
from player import Player, PlayerManager
from gameboard import Tile, TileGenerator, Gameboard, MoveCalculator, GameBoardRenderer
from dice import Dice, DiceManager, DiceRenderer
from game_manager import GameManager, GameState
from question import Question, QuestionManager, QuestionRenderer, AnswerRenderer
from buttons import Button, ButtonManager,ButtonRenderer
from utils import Color
pygame.init()
clock = pygame.time.Clock()

# Set screen size
screen_width = 1200
screen_height = 800

player_info = {"position": (0,0), "name": "P1", "token": None, "score": []}
player1 = Player(player_info)
player_manager = PlayerManager([player1])

'''
The below is used to generate
'''
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
RED =(255,0,0)
SPECIAL = (244,88,20)
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
categories = {0: "", 1: "Math", 2: "Science", 3: "Chemistry", 4: "Movie", 5: "Random"}
action_types = {0: "", 1: "", 2: "", 3: "", 4: "", 5: "Special"}
board_x = 100
board_y = 100
board_width = 600
board_height = 600
board_rect = (board_x, board_y, board_width, board_height)
tile_generator = TileGenerator(categories=categories, tile_matrix=tile_matrix,colors=colors, tile_types=action_types, board_rect=board_rect)
tile_objects, tile_map = tile_generator.generate()

question_database = dummy_database()
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
#dice_manager.animate()

'''
_Current Player Roll Dice
_Obtain dice value
_Gameboard take in player position and dice value 
-->calculate next possible moves
'''
print("Dice value: ", dice_manager.roll_value())
dice_value = dice_manager.roll_value()
player_manager.update_all(gameboard.get_center())
player_pos = player_manager.get_current_player_position()
#possible_moves = gameboard.get_possible_moves(player_pos=player_pos, dice_value=dice_value)
#print("Player position: ", player_pos)
#print("Possible moves:", possible_moves)
#

#Can only have one screen, create another screen will overide existing screen
screen = pygame.display.set_mode((screen_width, screen_height))
# Create the game board surface
pygame.display.set_caption("Board Game Board")
running = True
roll = False
game_manager = GameManager()

database = dummy_database()

# Init Question
question_position = {"x": board_x + board_width, "y": 150}
question_text_color = (0,0,0)
question_font = pygame.font.Font(None, 64)
question_renderer = QuestionRenderer(screen=screen, position=question_position, text_color=question_text_color)
question_manager = QuestionManager(database=database)

#Init Answer
answer_font  = pygame.font.Font(None, 50)
answer_position  = (question_position["x"], question_position["y"]+ 200)
answer_color = (0,0,255)
answer_renderer = AnswerRenderer(position=answer_position, text_color=answer_color)
# Button creator
def toggle_answer():
    print("Reveal answer")
    global game_manager
    game_manager.next_state()
def accept_answer():
    global game_manager
    game_manager.next_state()

button_x = board_x + board_width
button_y = screen_height//3
button_width = 200
button_height = 50
button_color = (0, 255, 0)
hover_color = (0, 200, 0)
button_font = pygame.font.Font(None, 32)

show_answer_button = Button((button_x, button_y),(button_width, button_height),(0, 255, 255), "Show Answer",(255, 255, 255) , toggle_answer)
accept_answer_button = Button((button_x-200, button_y+100),(button_width, button_height),(80, 120, 255), "Accept Answer",(255, 255, 255) , accept_answer)

button_renderer = ButtonRenderer(pygame)
button_manager = ButtonManager([show_answer_button])
button_manager.add_button(accept_answer_button)

gameboard.subscribe(question_manager)
gameboard.subscribe(player_manager)
displaying_question = False
already_shown = False
update_board = True
while running:
    #Without doing pygame.event.get(), the game will not be rendered
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                current_state = game_manager.get_state()
                mouse_pos = pygame.mouse.get_pos()
                if current_state == GameState.WAIT_ROLL:
                    if dice_manager.can_roll(mouse_pos=mouse_pos):
                        dice_manager.animate(screen=screen,pygame=pygame,clock=clock)
                        dice_value = dice_manager.roll_value()
                        player_pos = player_manager.get_current_player_position()
                        possible_moves = gameboard.get_possible_moves(player_pos=player_pos, dice_value=dice_value)
                        print(possible_moves)
                        game_manager.next_state()
                        update_board = True
                elif current_state == GameState.MOVE_SELECTION:
                    move_success = gameboard.move(mouse_pos=mouse_pos)
                    game_manager.next_state()
                    update_board = True
                    print(f"Move success {move_success}")
                    print("Update the player position, reset tile state")
                elif current_state == GameState.WAIT_PLAYER_ANSWER:
                    button_manager.on_click(mouse_pos=mouse_pos)
                elif current_state == GameState.PLAYER_VOTE:
                    button_manager.on_click(mouse_pos=mouse_pos)

    if not already_shown:
        screen.fill((125,125,125))
        already_shown = True
        dice_manager.draw(screen=screen)
        pygame.draw.rect(screen, WHITE, (board_x,board_y,board_width,board_height))
    if update_board:
        gameboard_renderer.render(tile_objects=tile_objects, engine=pygame, screen=screen)
        update_board = False
    #Handle question
    current_state = game_manager.get_state()
    if current_state == GameState.QUESTION_SELECTION:
        current_question = question_manager.get_current_question()
        print("current_question: ", current_question)
        question_renderer.render(question=current_question, font=question_font)
        for button in button_manager.buttons:
            button_renderer.draw(screen=screen, button=button, font=button_font)
        game_manager.next_state()
    elif current_state == GameState.ANSWER_REVEAL:
        current_question = question_manager.get_current_question()
        answer_renderer.render(screen=screen, text=current_question.answer, font=answer_font)
        game_manager.next_state()
    elif current_state == GameState.PLAYER_SELECTION:
        already_shown = False
        update_board = True
        game_manager.reset()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()