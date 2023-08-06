import pygame
import sys
import os

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

from utils_local import Color

class CategoryInfo:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def get_name(self):
        return self.name
    
    def get_name(self):
        return self.name 
    
    def set_name(self, name):
        self.name = name
    
    def set_color(self, color):
        self.color = color

class CategorySelectionScreen:

    def __init__(self, screen):
        # pygame.init()
        # screen_width, screen_height = 800, 600
        # self.screen = pygame.display.set_mode((screen_width, screen_height))
        # pygame.display.set_caption("Category Selection")
        self.screen = screen

        self.categories = ["Sport", "History", "Math", "Movie", "Geography", "Biology"]

        self.colors = [
            {"color_name": "Green", "color_code": Color.GREEN.value},
            {"color_name": "Blue", "color_code": Color.BLUE.value},
            {"color_name": "Yellow", "color_code": Color.YELLOW.value},
            {"color_name": "Red", "color_code": Color.RED.value},
        ]

        self.selected_categories = []
        self.selected_colors = []
        self.category_list = []

        self.button_width, self.button_height, self.button_size, self.button_spacing = 100, 50, 50, 20


    def draw_categories(self):
        x, y = self.screen.get_width() - 400 - self.button_width, (self.screen.get_height() - (len(self.categories) * (self.button_height + self.button_spacing))) // 2

        for i, category in enumerate(self.categories):
            button_rect = pygame.Rect(x, y, self.button_width, self.button_height)

            if category in self.selected_categories:
                pygame.draw.rect(self.screen, Color.WHITE.value, button_rect)
                pygame.draw.rect(self.screen, Color.BLACK.value, button_rect, 3)
            else:
                pygame.draw.rect(self.screen, Color.WHITE.value, button_rect)

            font = pygame.font.Font(None, 24)
            text = font.render(category, True, Color.BLACK.value)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

            y += self.button_height + self.button_spacing

    def draw_colors(self):
        x, y = 100, (self.screen.get_height() - (len(self.colors) * (self.button_size + self.button_spacing))) // 2

        for i, color in enumerate(self.colors):
            button_rect = pygame.Rect(x, y, self.button_size, self.button_size)

            if color in self.selected_colors:
                pygame.draw.rect(self.screen, color["color_code"], button_rect)
                pygame.draw.rect(self.screen, Color.BLACK.value, button_rect, 3)
            else:
                pygame.draw.rect(self.screen, color["color_code"], button_rect)

            y += self.button_size + self.button_spacing

    def handle_click(self):

        mouse_pos = pygame.mouse.get_pos()

        for i, category in enumerate(self.categories):
            button_rect = pygame.Rect(self.screen.get_width() - 400 - self.button_width, (self.screen.get_height() - (len(self.categories) * (self.button_height + 20))) // 2 + (i * (self.button_height + 20)), self.button_width, self.button_height)
            if button_rect.collidepoint(mouse_pos):
                if category not in self.selected_categories and len(self.selected_categories) < 4:
                    self.selected_categories.append(category)
                elif category in self.selected_categories:
                    self.selected_categories.remove(category)

        for i, color in enumerate(self.colors):
            button_rect = pygame.Rect(100, (self.screen.get_height() - (len(self.colors) * (self.button_size + 20))) // 2 + (i * (self.button_size + 20)), self.button_size, self.button_size)
            if button_rect.collidepoint(mouse_pos):
                if color not in self.selected_colors and len(self.selected_colors) < 4:
                    self.selected_colors.append(color)
                elif color in self.selected_colors:
                    self.selected_colors.remove(color)

    def run(self):
        while (len(self.selected_categories)) < 4:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click()

            self.screen.fill(Color.WHITE.value)
            self.draw_categories()
            self.draw_colors()

            font = pygame.font.Font(None, 24)
            x = self.screen.get_width() - 2.5 * self.button_width
            y = (self.screen.get_height() + 100 - (len(self.colors) * (self.button_size + self.button_spacing))) // 2
            pair_rect = pygame.Rect(x-20, y-20, 2*self.button_width, 3*self.button_height)
            pygame.draw.rect(self.screen, Color.BLACK.value, pair_rect, 1)

            title_font = pygame.font.Font(None, 30)
            title_text = title_font.render("Select 4 Categories", True, Color.BLACK.value)
            self.screen.blit(title_text, (x-self.button_spacing, y-3*self.button_spacing))

            for i, category in enumerate(self.selected_categories):
                text = font.render(f"{self.selected_colors[i]['color_name']}: {category}", True, Color.BLACK.value)
                self.screen.blit(text, (x, y))
                y += 30

            pygame.display.flip()
        
        return self.get_selected_categories()
    
    def get_selected_categories(self):
        for i in range(0, len(self.selected_categories)):
            self.category_list.append(CategoryInfo(self.selected_categories[i], self.selected_colors[i]['color_name']))
        return self.category_list

        



