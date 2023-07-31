import sys
import os
import subprocess

# Add Python path to help import 
current_dir = os.path.dirname(os.path.abspath(__file__))
parrent_dir = os.path.dirname(current_dir)
sys.path.append(parrent_dir)

from category_selection import *

game_categories = {}
get_game_categories(game_categories)

print("Selected categories with color information:")

print(game_categories)