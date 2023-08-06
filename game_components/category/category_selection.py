import pygame
import sys
import os
from utils_local import create_button, is_point_inside_rect
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
from buttons import ButtonRenderer
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
        self.category_per_row = 2
        self.colors = [
            Color.GREEN,
            Color.BLUE,
            Color.YELLOW,
            Color.RED,
        ]

        self.selected_categories = []
        self.selected_colors = []
        self.category_list = []
        self.category_buttons = []
        
        # use to rotate color when selected
        self.current_category_index = 0
        self.max_nb_category = 4
        self.selected_buttons = [None] * self.max_nb_category
        self.redraw_buttons = False
        self.button_width, self.button_height, self.button_size, self.button_spacing = 100, 50, 50, 20
        self.button_default_color = Color.GRAY.value
    
    def create_category_buttons(self):
        row_x, col_y = self.screen.get_width()// 2 - self.button_width, (self.screen.get_height() - (len(self.categories) * (self.button_height + self.button_spacing))) // 2
        
        current_row = 0
        current_col = 0
        margin = self.button_width // 3
        for i, category in enumerate(self.categories):
            x = row_x + (self.button_width + margin) * current_col
            y = col_y + (self.button_height + margin) * current_row

            button_rect = pygame.Rect(x, y, self.button_width, self.button_height)
            button = create_button(rect=button_rect,button_color= self.button_default_color,
                                   text=category, text_color=Color.BLACK.value)
            #Move row and col
            current_col = (current_col + 1) % self.category_per_row
            if current_col == 0:
                current_row += 1
            
            self.category_buttons.append(button)

    def draw_category_buttons(self):
        font = pygame.font.Font(None, 24)
        for button in self.category_buttons:
            self.button_renderer.draw(screen=self.screen, button=button, font=font)
    
    def create_continue_button(self):
        #Draw it relative to the number of category buttons on the screen
        last_button = self.category_buttons[-1]
        last_x,last_y = last_button.get_position()
        button_width = self.button_width + 50
        x, y = self.screen.get_width()// 2 - button_width//2, last_y + self.button_spacing + 2*self.button_height
        button_rect = pygame.Rect(x, y, button_width, self.button_height)
        button = create_button(rect=button_rect,button_color= self.button_default_color,
                                text="Continue", text_color=Color.BLACK.value)    
        self.continue_button = button

    def draw_continue_button(self):
        font = pygame.font.Font(None, 24)
        self.button_renderer.draw(screen=self.screen, button=self.continue_button, font=font)

    def get_nb_selected(self):
        return len([button for button in self.selected_buttons if button != None])
    
    def update_continue_button(self):
        if self.get_nb_selected() == self.max_nb_category:
            self.continue_button.set_color(Color.GREEN.value)
        else:
            self.continue_button.set_color(self.button_default_color)
        self.draw_continue_button()

    def update_selected_index(self):
        self.current_category_index = (self.current_category_index + 1) % self.max_nb_category

    def handle_category_click(self, engine) -> bool:
        mouse_pos = engine.mouse.get_pos()
        for index, button in enumerate(self.category_buttons):
            button_rect = button.get_rect()
            if is_point_inside_rect(mouse_pos, button_rect):
                if button in self.selected_buttons:
                    print("You are selected already")
                    return True
                #
                current_button = self.selected_buttons[self.current_category_index]
                if current_button:
                    current_button.set_color(self.button_default_color)
                button.set_color(self.colors[self.current_category_index].value)
                self.selected_buttons[self.current_category_index] = button
                self.update_selected_index()
                print(f"I selected: {button.get_text()}")
                self.redraw_buttons = True
                return True
        return False


    def handle_continue_click(self, engine) -> bool:
        mouse_pos = engine.mouse.get_pos()
        button_rect = self.continue_button.get_rect()
        if is_point_inside_rect(mouse_pos, button_rect):
            return True
        return False


    def run(self,engine):
        running = True
        while running:
            for event in engine.event.get():
                if event.type == engine.QUIT:
                    engine.quit()
                    sys.exit()
                elif event.type == engine.MOUSEBUTTONDOWN:
                    handled = False
                    handled = self.handle_category_click(engine=engine)
                    if not handled:
                        print("handdled here")
                        if self.get_nb_selected() == self.max_nb_category:
                            can_continue = self.handle_continue_click(engine=engine)
                            if can_continue:
                                running = False

            #Init
            if len(self.category_buttons) == 0:
                self.screen.fill(Color.WHITE.value)

                #Display text
                text = f"Select {self.max_nb_category} Categories"
                text_x, text_y = self.screen.get_width()//2 - len(text)*4, 50

                title_font = engine.font.Font(None, 30)
                title_text = title_font.render(text, True, Color.BLACK.value)
                self.screen.blit(title_text, (text_x, text_y))

                #Display category buttons
                self.button_renderer = ButtonRenderer(engine=engine)
                self.create_category_buttons()
                self.draw_category_buttons()

                #Display continue button
                self.create_continue_button()
                self.draw_continue_button()
            elif self.redraw_buttons:
                self.draw_category_buttons()
                self.update_continue_button()
                self.redraw_buttons = False
                
            engine.display.flip()
        
        return self.get_selected_categories()
    
    def get_selected_categories(self):
        for index, button in enumerate(self.selected_buttons):
            category = button.get_text()
            color = button.get_color()
            self.category_list.append(CategoryInfo(category, color))
        return self.category_list

        



