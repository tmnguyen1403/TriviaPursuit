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

from landing_screen import LandingScreen

pygame.font.init()
screen = pygame.display.set_mode((1200, 800))
landing = LandingScreen()
landing.render_screen(pygame, screen, None, None)


