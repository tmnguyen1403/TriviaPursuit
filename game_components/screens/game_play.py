import pygame

from database import dummy_database
from player import Player, PlayerManager
from gameboard import Tile, TileGenerator, GameBoard, MoveCalculator, GameBoardRenderer
from dice import Dice, DiceManager, DiceRenderer

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
colors = {0: WHITE, 1: BLUE, 2: YELLOW, 3: RED, 4: GREEN, 5: SPECIAL}
categories = {0: "", 1: "Math", 2: "Science", 3: "Sport", 4: "Movie", 5: "Random"}
action_types = {0: "", 1: "", 2: "", 3: "", 4: "", 5: "Special"}
board_x = 100
board_y = 100
board_width = 600
board_height = 600
board_rect = (board_x, board_y, board_width, board_height)
tile_generator = TileGenerator(categories=categories, tile_matrix=tile_matrix,colors=colors, tile_types=action_types, board_rect=board_rect)
tile_objects = tile_generator.generate()

question_database = dummy_database()
move_calculator = MoveCalculator(-1)
gameboard = GameBoard(question_database, tile_matrix, move_calculator)
gameboard_renderer = GameBoardRenderer()

# Die
die_width = 100
die_height = 100
die_x = (screen_width - die_width) // 4
die_y = (screen_width - die_height) // 4
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
player_pos = player_manager.get_player_position()
possible_moves = gameboard.get_moves(player_pos=player_pos, dice_value=dice_value)
print("Player position: ", player_pos)
print("Possible moves:", possible_moves)
#

#Can only have one screen, create another screen will overide existing screen
screen = pygame.display.set_mode((screen_width, screen_height))
# Create the game board surface
pygame.display.set_caption("Board Game Board")
running = True
while running:
    #Without doing pygame.event.get(), the game will not be rendered
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((125,125,125))
    # # Draw the game board
    pygame.draw.rect(screen, WHITE, (board_x,board_y,board_width,board_height))
    gameboard_renderer.render(tile_objects=tile_objects, engine=pygame, screen=screen)
    # for tile in tile_objects:
    #     x,y,width,height = tile.rect
    #     border_size = 5
    #     inner_x = x + border_size
    #     inner_y = y + border_size
    #     inner_width = width - border_size * 2
    #     inner_height = height - border_size * 2
    #     pygame.draw.rect(screen, BLACK, (x, y, width, height))
    #     pygame.draw.rect(screen, tile.color, (inner_x, inner_y, inner_width, inner_height))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()