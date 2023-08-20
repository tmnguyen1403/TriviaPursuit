class QuestionRenderer:
    def __init__(self, screen, position, text_color, background_color = None):
        self.screen = screen
        self.position = position
        self.text_color = text_color
        self.background_color = background_color
    def render(self, question, font):
        print("Hello question renderer")
        category_text = font.render(f"Category {question.category}", True, self.text_color, self.background_color)
        self.screen.blit(category_text, (self.position["x"],self.position["y"] - 100))

        message_text = font.render(question.get_text(), True, self.text_color, self.background_color)
        self.screen.blit(message_text, (self.position["x"],self.position["y"]))