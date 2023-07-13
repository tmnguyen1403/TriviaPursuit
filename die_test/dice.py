import random


class Dice:
    def __init__(self, position, size, color, text_color):
        self.position = position
        self.size = size
        self.color = color
        self.roll_number = random.randint(1, 6)
        self.text_color = text_color

    def roll(self):
        self.roll_number = random.randint(1, 6)
        return self.roll_number

    def get_rect(self):
        return self.position + self.size

    def get_value(self):
        return self.roll_number

    def get_color(self):
        return self.color

    def get_text_color(self):
        return self.text_color


class DiceRenderer:
    def __init__(self, engine):
        self.engine = engine

    def draw(self, screen, dice, font):
        dice_rect = dice.get_rect()
        self.engine.draw.rect(screen, dice.get_color(), dice_rect)
        dice_text = font.render(str(dice.get_value()), True, dice.get_text_color())
        x, y, w, h = dice_rect
        dice_text_rect = dice_text.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(dice_text, dice_text_rect)
