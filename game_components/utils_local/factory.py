from buttons import Button
from .color import Color

def create_button(rect, button_color, text:str,text_color=Color.WHITE.value, action = None):
    x,y,w,h = rect
    button = Button((x,y),(w,h), button_color, text, text_color, action)
    return button
    # self.button_renderer.add_button(button)