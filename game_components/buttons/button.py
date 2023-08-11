from typing import Dict, List, Optional
class Button:
    def __init__(self, position, size, color, text, text_color, action):
        self.position = position
        self.size = size
        self.color = color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.is_hidden = False

    def get_rect(self):
        return self.position + self.size
    
    def get_position(self):
        return self.position
    
    def get_text(self):
        return self.text
    
    def get_color(self):
        return self.color
    
    def set_color(self, color):
        self.color = color
        
    def on_click(self):
        self.action()
    
    def hide(self):
        self.is_hidden = True
    
    def reveal(self):
        self.is_hidden = False

    def is_disable(self):
        return self.is_hidden
    