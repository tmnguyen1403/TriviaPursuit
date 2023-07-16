class AnswerRenderer:
    def __init__(self, position, text_color, background_color = None):
        self.position = position
        self.text_color = text_color
        self.background_color = background_color
    def render(self, screen, text, font):
        #print("Hello AnswerRenderer")
        message_text = font.render(text, True, self.text_color, self.background_color)
        screen.blit(message_text, self.position)