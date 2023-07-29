import pygame
import webview

pygame.init()
clock = pygame.time.Clock()

video_url = "https://www.youtube.com/embed/XnbCSboujF4"
video_view = webview.create_window("Test webview", video_url)

screen = pygame.display.set_mode((1200, 800))

running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = false
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                webview.start()
    screen.fill((125,0,255))
    pygame.display.flip()
    clock.tick(60)
'''
For video question:
Question
    Watch video button:

No Question
    Watch video to hear the question


'''