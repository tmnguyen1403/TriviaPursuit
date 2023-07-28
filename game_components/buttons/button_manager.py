from .button import Button
from typing import List, Dict
class ButtonManager:
    def __init__(self, buttons = List[Button]):
        self.buttons = buttons
        self.disable_buttons : Dict[int, bool] = {} #disable button indices 
        if self.buttons is None:
          self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)
     
    def is_point_inside_rect(self, point, rect):
        """this method is used to check if a mouse click action is inside 
        a button
        Args:
            point (x,y): mouse click position
            rect (x,y,width,height): the position of the button on screen

        Returns:
            bool: 
        """      
        x, y = point
        rect_x, rect_y, rect_width, rect_height = rect
        return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height
    
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
            if self.is_point_inside_rect(mouse_pos, button.get_rect()):
                button.on_click()
                print("Click on button")
                break