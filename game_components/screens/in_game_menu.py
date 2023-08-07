
from utils_local import Color, create_button, is_point_inside_rect
from buttons import Button, ButtonRenderer
'''
The below is used to generate
'''
# Define category_colors
class InGameMenu:
    def __init__(self, screen) -> None:
        self.init = False
        self.screen = screen
        screen_width,screen_height = self.screen.get_size() 
        self.continue_button_rect = (screen_width // 2 - 150, screen_height//8, 150, 50)
        self.quit_button_rect = (screen_width // 2 + 50, screen_height//8, 150, 50)
        self.hide_area = ((screen_width // 2 - 150, screen_height//8, 2*150+50, 50))
        self.disable_buttons = True
        self.quit_game = False

    def draw(self,engine):
        if not self.init:
            self.button_renderer = ButtonRenderer(engine)
            self.continue_button = create_button(self.continue_button_rect, Color.GREEN.value, "Continue", Color.BLACK.value)
            self.quit_button = create_button(self.quit_button_rect, Color.RED.value, "Quit", Color.BLACK.value)
            self.buttons = [self.continue_button, self.quit_button]
            self.font = engine.font.SysFont(None, 24)
            self.init = True

        for button in self.buttons:
            self.button_renderer.draw(self.screen, button=button, font=self.font)
        self.disable_buttons = False
    
    def hide_buttons(self, engine):
        engine.draw.rect(self.screen, Color.DEFAULT_SCREEN.value ,self.hide_area)
        self.disable_buttons = True
        engine.display.flip()

    def is_active(self):
        return not self.disable_buttons
    
    def handle_click(self,engine) -> bool:
        if self.disable_buttons:
            return False
        
        mouse_pos = engine.mouse.get_pos()
        if is_point_inside_rect(mouse_pos, self.continue_button_rect):
            self.hide_buttons(engine=engine)
        elif is_point_inside_rect(mouse_pos, self.quit_button_rect):
            self.hide_buttons(engine=engine)
            self.quit_game = True

        return True
    
    def is_quit_game(self) -> bool:
        return self.quit_game
        

