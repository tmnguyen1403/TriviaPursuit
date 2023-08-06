import sys
import os
import subprocess
try:
    import pygame
except Exception as e:
    print("Attemp to install packages")
    subprocess.run(["python3 -m pip install $(cat requirements.txt)"], shell=True)
# Add Python path to help import
current_dir = os.path.dirname(os.path.abspath(__file__))
parrent_dir = os.path.dirname(current_dir)
sys.path.append(parrent_dir)


from category_selection import CategorySelectionScreen
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Category Selection")

cs = CategorySelectionScreen(screen=screen)

cs.run(engine=pygame)
pair = cs.get_selected_categories()
for i in range(0, len(pair)):
    print(f"Category: {pair[i].name}, Color: {pair[i].color}")