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