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

#get the size for the tiles, and the border sizes
square_size = board_width // 10
border_size = square_size //10

#calculate the size of the qhite squares separating the spokes
w_square_size = (3*square_size)+ (2*border_size)

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

    #draw big black square to act as borders
    pygame.draw.rect(board_surface, BLACK, (350, 250, board_height, board_width))

    # draw 4 white squares to separate the spokes and outside borders
    for i in range(2):
        for j in range(2):
            w_square_x = 350 + (((2* border_size)+ square_size) * (i+1)) + (w_square_size*i)
            w_square_y = 250 + (((2* border_size)+ square_size) * (j+1)) + (w_square_size*j)

            pygame.draw.rect(board_surface, WHITE, (w_square_x, w_square_y, 
                                                    w_square_size, w_square_size))


    # Draw the game board
    for row in range(9):
        for col in range(9):
            # Calculate the coordinates of each square on the board

            x = 350 + ((col+1) * border_size) + (col * square_size)
            y = 250 + ((row+1) * border_size) + (row * square_size)

            #draw the game board rectangles
            if tile_matrix[row][col] == 1:
                #color the squares
                square_color = colors[color_matrix[row][col]]

                pygame.draw.rect(board_surface, square_color, (x, y, square_size, square_size))




    players = [Player(_) for _ in range(4)]
    cat_colors = (RED, GREEN, BLUE, YELLOW)
    score_boxes =[]


    #draw players onto the game board
    for index in range(len(players)):
        pygame.draw.circle(board_surface, BLACK, players[index].curr_pos, 14)
        pygame.draw.circle(board_surface, cat_colors[index], players[index].curr_pos, 12)


    #these two lines are to update the player scores, so there are some colored tiles in the example
    players[1].update_score(1)
    players[3].update_score(2)


    #create the scoreboard
    for n in range(len(players)):

        #calculate x and y coordinates
        x = 150 + (300 * n)
        y = 25


        score_boxes += [Score_Box(players[n], (x,y, 90,90), cat_colors)]


        #draw the player name next to their score box
        text = "Player " + str(players[n].name) + ":"
        font = pygame.font.Font(None, 32)
        text_surface = font.render(text, True, BLACK)
        textbox_x = x - 100
        textbox_width = text_surface.get_width() + 10
        textbox_height = text_surface.get_height() + 10

        pygame.draw.rect(board_surface, WHITE, (textbox_x, y, textbox_width, textbox_height))
        board_surface.blit(text_surface, (textbox_x + 5, y + 5))


    #draw the score boxes
    for sb in score_boxes: sb.draw(pygame, board_surface)



    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
