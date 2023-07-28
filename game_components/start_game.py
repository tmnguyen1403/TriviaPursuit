import pygame
import requests

#setup
pygame.init()
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

#Button test
button_width = 200
button_height = 50
button_color = (0, 255, 0)
hover_color = (0, 200, 0)
text_color = (255, 255, 255)
font = pygame.font.Font(None, 32)


# Define button position
button_x = (screen_width - button_width) // 2
button_y = (screen_height - button_height) // 2
message = None
def is_point_inside_rect(point, rect):
    x, y = point
    rect_x, rect_y, rect_width, rect_height = rect
    return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height
button_text_rect = None 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #Left mouse
                mouse_pos = pygame.mouse.get_pos()
                if is_point_inside_rect(mouse_pos, (button_x, button_y, button_width, button_height)):
                    print("Button is clicked. Request question")
                    response =  requests.get("http://localhost:8000")
                    message = response.text
                  
    screen.fill("purple")
    
    if message:
        message_text = font.render(message, True, text_color)
        screen.blit(message_text, (0,0))
    #draw a red circle at the player position
    pygame.draw.circle(screen, "red", player_pos, 40)
    pygame.draw.circle(screen, "red", player_pos, 40)

    #render button
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    button_text = font.render("Click Me!", True, text_color)
    button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(button_text, button_text_rect)
    # Action based on key press
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:#up
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:#down
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:#left
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]: 
        player_pos.x += 300 * dt
    if keys[pygame.K_o]:
        response = requests.get("http://localhost:8000")
        print(response.text)
    if keys[pygame.K_x]:
        print("Update screen resolution")
        screen_width += 50
        screen_height += 25
        screen = pygame.display.set_mode((screen_width, screen_height))

    # Render game here
    pygame.display.flip()
    #clock tick is called at the end to maintain the desire frame rate (create delay if frame rate update is too)
    #the return value of clock tick is the elapsed time since clock tick is called (millisecond)
    dt  = clock.tick(60) / 1000

pygame.quit()