from enum import Enum
from utils import Color
from buttons import Button, ButtonRenderer
from utils import is_point_inside_rect

class InternalState(Enum):
    PROMPT_CATEGORY_SELECTION=0
    WAIT_CATEGORY_SELECTION=1
    CATEGORY_SELECTED=2

#class ButtonText(Enum):
    #SHOW_ANSWER = "Show Answer"
    #ACCEPT = "Accept"
    #REJECT = "Reject"

class TrivialComputeSelectScreen:
    def __init__(self):
        self.state = InternalState.PROMPT_CATEGORY_SELECTION
        self.init_object = False
        self.buttons = {}
        self.selected_category = ''
    def init_screen(self, screen):
        screen_width, screen_height = screen.get_size()
        self.category_position = (screen_width//4, screen_height//4)
        self.text_color = Color.BLACK.value
        q_w, q_h = self.category_position
        self.instruction_label_position = (screen_width//2, q_h - 50)
        c_w, c_h = self.category_position

        #Button setting
        b_w, b_h = c_w//2, c_h//6
        self.category_one_rect = (25, 100 + c_h, b_w, b_h)
        self.category_two_rect = (25 + c_w, 100 + c_h, b_w, b_h)
        self.category_three_rect = (25 + c_w*2, 100 + c_h, b_w, b_h)
        self.category_four_rect = (25 + c_w * 3, 100 + c_h, b_w, b_h)

    def create_button(self, rect, button_color, text,text_color=Color.WHITE.value, action = None):
        x,y,w,h = rect
        button = Button((x,y),(w,h), button_color, text, text_color, action)
        self.buttons[text] = button
        return button
        # self.button_renderer.add_button(button)

    def set_state(self, new_state: 'InternalState'):
        print(f"Current SelectScreen state: {self.state}")
        self.state = new_state
        print(f"New SelectScreen state: {self.state}")
        
    def render_screen(self, pygame, screen, game_manager, categories):
        print("Categories: ", categories)
        if not self.init_object:
            self.init_screen(screen=screen)
            self.init_object = True
            self.button_renderer = ButtonRenderer(pygame)
            self.font = pygame.font.Font(None, 32)
        running = True
        self.game_manager = game_manager
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.state == InternalState.WAIT_CATEGORY_SELECTION:
                            buttons = self.buttons
                            for button in buttons:
                                if is_point_inside_rect(mouse_pos, buttons[button].get_rect()):
                                    buttons[button].on_click()
                                    self.selected_category = button

  
            if self.state == InternalState.PROMPT_CATEGORY_SELECTION:
                screen.fill(Color.WHITE.value)

                # Render Instruction Label
                label_text = 'Select a category for the next question'
                label_source = self.font.render(label_text, True, self.text_color, None)
                screen.blit(label_source, self.category_position)
                
                # Button render
                show_buttons = self.buttons.get(0, None)
                if show_buttons is None:
                    show_buttons = [
                        self.create_button(self.category_one_rect, button_color=Color.BLUE.value, text=categories[0],
                                           action=lambda: self.set_state(InternalState.CATEGORY_SELECTED)),
                        self.create_button(self.category_two_rect, button_color=Color.BLUE.value,
                                           text=categories[1],
                                           action=lambda: self.set_state(InternalState.CATEGORY_SELECTED)),
                        self.create_button(self.category_three_rect, button_color=Color.BLUE.value,
                                           text=categories[2],
                                           action=lambda: self.set_state(InternalState.CATEGORY_SELECTED)),
                        self.create_button(self.category_four_rect, button_color=Color.BLUE.value,
                                           text=categories[3],
                                           action=lambda: self.set_state(InternalState.CATEGORY_SELECTED))]
                    for button in show_buttons:
                        self.button_renderer.draw(screen=screen, button=button, font=self.font)

                self.set_state(InternalState.WAIT_CATEGORY_SELECTION)
            elif self.state == InternalState.CATEGORY_SELECTED:
                print("Category: " + self.selected_category)
                self.set_state(InternalState.PROMPT_CATEGORY_SELECTION)
                return self.selected_category
            
            pygame.display.flip()