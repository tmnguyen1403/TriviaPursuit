
class DiceRenderer:
    def __init__(self, engine: 'pygame', font):
        self.engine = engine
        self.font = font

    def draw(self, screen, dice: 'Dice'):
        dice_rect = dice.get_rect()
        self.engine.draw.rect(screen, dice.get_color(), dice_rect)
        dice_text = self.font.render(str(dice.get_value()), True, dice.get_text_color())
        x, y, w, h = dice_rect
        dice_text_rect = dice_text.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(dice_text, dice_text_rect)