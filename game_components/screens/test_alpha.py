import pygame
import sys

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Alpha Color Example")

# Define a color with alpha value
alpha_color = (255, 0, 0, 255)  # Red color with alpha of 128

# Fill the screen with a color
screen.fill((0, 0, 0))  # Fill with black

# Create a surface with alpha
surface = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.rect(surface, alpha_color, (0, 0, 100, 100))

# Blit the surface onto the screen
screen.blit(surface, (width // 2 - 50, height // 2 - 50))

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
