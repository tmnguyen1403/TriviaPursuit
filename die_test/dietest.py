# Import and initialize the pygame library
import pygame
from dice import Dice, DiceRenderer

pygame.init()

# Set screen size
screen_width = 1280
screen_height = 720

# Clock for setting frame rate
clock = pygame.time.Clock()

# Set up the drawing window
screen = pygame.display.set_mode([screen_width, screen_height])

# Die
die_width = 100
die_height = 100
die_x = (screen_width - die_width) // 4
die_y = (screen_width - die_height) // 4
die_color = (0, 0, 0)
die_text_color = (255, 255, 255)
die_font = pygame.font.Font(None, 64)

# Roll button
roll_button_width = 200
roll_button_height = 50
roll_button_x = (screen_width - roll_button_width) // 2
roll_button_y = (screen_height - roll_button_height) // 2
roll_button_color = (0, 255, 0)
hover_color = (0, 200, 0)
roll_button_text_color = (255, 255, 255)
button_font = pygame.font.Font(None, 32)


def is_point_inside_rect(point, rect):
    x, y = point
    rect_x, rect_y, rect_width, rect_height = rect
    return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height


dice = Dice((die_x, die_y), (die_width, die_height), die_color, die_text_color)
dice_renderer = DiceRenderer(pygame)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse
                mouse_pos = pygame.mouse.get_pos()
                if is_point_inside_rect(mouse_pos, (roll_button_x, roll_button_y, roll_button_width, roll_button_height)
                                        ):
                    print("Button is clicked. Rolling die")
                    dice.roll()
                    print("Number rolled is " + str(dice.get_value()) + ".")

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw roll die button
    pygame.draw.rect(screen, roll_button_color, (roll_button_x, roll_button_y, roll_button_width, roll_button_height))
    button_text = button_font.render("Roll Die", True, roll_button_text_color)
    button_text_rect = button_text.get_rect(center=(roll_button_x + roll_button_width // 2, roll_button_y +
                                                    roll_button_height // 2))
    screen.blit(button_text, button_text_rect)

    # Draw die
    dice_renderer.draw(screen, dice, die_font)

    # Render game
    pygame.display.flip()

    # set frame rate to 60
    dt = clock.tick(60) / 1000

# Done! Time to quit.
pygame.quit()
