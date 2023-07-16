from .button import Button
from typing import List, Dict
from utils import is_point_inside_rect
class ButtonManager:
    def __init__(self, buttons = List[Button]):
        self.buttons = buttons
        self.disable_buttons : Dict[int, bool] = {} #disable button indices 
        if self.buttons is None:
          self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)
    
    def disable(self, button: Button):
        if self.buttons.count(button) == 0:
            return False
        index = self.buttons.index(button)
        self.disable_buttons[index] = True
        return True
    def is_disable(self, button: Button):
        if self.buttons.count(button) == 0:
            return False
        index = self.buttons.index(button)
        return self.disable_buttons.get(index, False)
    def enable(self, button: Button):
        if self.buttons.count(button) == 0:
            return False
        index = self.buttons.index(button)
        self.disable_buttons[index] = False
        return True
    
    def on_click(self, mouse_pos):
        for index, button in enumerate(self.buttons):
          if self.disable_buttons.get(index, False) == False:
            if is_point_inside_rect(mouse_pos, button.get_rect()):
                button.on_click()
                print("Click on button")
                break