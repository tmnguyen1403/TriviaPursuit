from typing import Dict, List, Optional
class Button:
    def __init__(self, position, size, color, text, text_color, action):
        self.position = position
        self.size = size
        self.color = color
        self.text = text
        self.text_color = text_color
        self.action = action
    def get_rect(self):
        return self.position + self.size
    def on_click(self):
        self.action()