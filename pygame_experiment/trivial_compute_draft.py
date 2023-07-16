import pygame
from score_tile import Score_Tile
from score_box import Score_Box
from player import Player


# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
RED =(255,0,0)

# Set the dimensions of the game board
board_width = 600
board_height = 600

#create matrix to represent where game board rectangles should be and their colors

tile_matrix = [[1,1,1,1,1,1,1,1,1],
               [1,0,0,0,1,0,0,0,1],
               [1,0,0,0,1,0,0,0,1],
               [1,0,0,0,1,0,0,0,1],
               [1,1,1,1,1,1,1,1,1],
               [1,0,0,0,1,0,0,0,1],
               [1,0,0,0,1,0,0,0,1],
               [1,0,0,0,1,0,0,0,1],
               [1,1,1,1,1,1,1,1,1]]

colors = [WHITE, BLUE, YELLOW, RED, GREEN]
color_matrix = [[0,2,1,4,3,2,1,4,0],
                [3,-1,-1,-1,2,-1,-1,-1,3],
                [4,-1,-1,-1,1,-1,-1,-1,2],
                [1,-1,-1,-1,4,-1,-1,-1,1],
                [2,1,4,3,0,1,2,3,4],
                [3,-1,-1,-1,2,-1,-1,-1,3],
                [4,-1,-1,-1,3,-1,-1,-1,2],
                [1,-1,-1,-1,4,-1,-1,-1,1],
                [0,2,3,4,1,2,3,4,0]]

# Create the game board surface
board_surface = pygame.display.set_mode((1300, 900))
pygame.display.set_caption("Trivial Compute")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the board surface with white color
    board_surface.fill(WHITE)

    # Draw the game board
    for row in range(9):
        for col in range(9):
            # Calculate the coordinates of each square on the board
            square_size = board_width // 9
            x = 350 + (col * square_size)
            y = 250 + (row * square_size)

            border_size = 5
            inner_x = x + border_size
            inner_y = y + border_size
            inner_size = square_size - border_size * 2

            #draw the game board rectangles
            if tile_matrix[row][col] == 1:
                #color the squares
                square_color = colors[color_matrix[row][col]]
                

                # Draw initial black square on the board


                pygame.draw.rect(board_surface, BLACK, (x, y, square_size, square_size))
                #draw smaller colored square inside of black square 
                pygame.draw.rect(board_surface, square_color, (inner_x, inner_y, inner_size, inner_size))




    players = [Player() for _ in range(4)]
    cat_colors = (RED, GREEN, BLUE, YELLOW)
    score_boxes =[]


    #these two lines are to update the player scores, so there are some colored tiles in the example
    players[1].update_score(1)
    players[3].update_score(2)


    #draw in the scoreboard
    for n in range(len(players)):

        #calculate x and y coordinates
        x = 100 + (300 * n)
        y = 25


        score_boxes += [Score_Box(players[n], (x,y, 90,90), cat_colors)]

    for sb in score_boxes: sb.draw(pygame, board_surface)



    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
