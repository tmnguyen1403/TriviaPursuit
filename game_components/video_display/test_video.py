import pygame
import webbrowser

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame with YouTube Video")

    # Replace "your_video_id" with the actual YouTube video ID you want to display.
    youtube_video_id = "XnbCSboujF4"

    youtube_url = f"https://www.youtube.com/embed/{youtube_video_id}"

    # Open the YouTube video in the user's default web browser.
    webbrowser.open(youtube_url)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
