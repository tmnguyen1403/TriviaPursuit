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

class ButtonRenderer:
    def __init__(self,engine):
        self.engine = engine
    def draw(self, screen, button, font):
        button_rect = button.get_rect()
        self.engine.draw.rect(screen, button.color, button_rect)
        button_text = font.render(button.text, True, button.text_color)
        x,y,w,h = button_rect
        button_text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(button_text, button_text_rect)

class ButtonManager:
    def __init__(self, buttons = None):
        self.buttons = buttons
        if self.buttons is None:
          self.buttons = []
    def add_button(self, button):
        self.buttons.append(button)
    def is_point_inside_rect(self, point, rect):
      x, y = point
      rect_x, rect_y, rect_width, rect_height = rect
      return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height
    def on_click(self, mouse_pos):
        for button in self.buttons:
          if self.is_point_inside_rect(mouse_pos, button.get_rect()):
              button.on_click()
              print("Click on button")
              break