import pygame
from tile_generator import TileGenerator
# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
RED =(255,0,0)
SPECIAL = (244,88,20)

# Set the screen size
screen_size = (1200, 800)

# Set the dimensions of the game board
board_x = 100
board_y = 100
board_width = 600
board_height = 600

#create matrix to represent where game board rectangles should be and their colors


# tile_matrix = [[1,1,1,1,1,1,1,1,1],
#                [1,0,0,0,1,0,0,0,1],
#                [1,0,0,0,1,0,0,0,1],
#                [1,0,0,0,1,0,0,0,1],
#                [1,1,1,1,1,1,1,1,1],
#                [1,0,0,0,1,0,0,0,1],
#                [1,0,0,0,1,0,0,0,1],
#                [1,0,0,0,1,0,0,0,1],
#                [1,1,1,1,1,1,1,1,1]]

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
tile_generator = TileGenerator(categories=categories, tile_matrix=tile_matrix,colors=colors, tile_types=action_types, board_rect=(board_x,board_y,board_width,board_height))
tile_objects = tile_generator.generate()

screen_surface = pygame.display.set_mode((screen_size[0], screen_size[1]))
# Create the game board surface
#board_surface = pygame.display.set_mode((board_width, board_height))
pygame.display.set_caption("Board Game Board")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the board surface with white color
    screen_surface.fill((125,125,125))
    pygame.draw.rect(screen_surface, WHITE, (board_x,board_y,board_width,board_height))
    #board_surface.fill(WHITE)

    # Draw the game board
    for tile in tile_objects:
        x,y,width,height = tile.rect
        pygame.draw.rect(screen_surface, BLACK, (x, y, width, height))
        
        border_size = 5
        inner_x = x + border_size
        inner_y = y + border_size
        inner_width = width - border_size * 2
        inner_height = height - border_size * 2
        pygame.draw.rect(screen_surface, tile.color, (inner_x, inner_y, inner_width, inner_height))
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
