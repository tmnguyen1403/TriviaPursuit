import random
from utils import is_point_inside_rect
class DiceManager:
    def __init__(self, dice: 'Dice', dice_renderer: 'DiceRenderer', special_dice_value=6):
        self.dice = dice
        self.dice_renderer = dice_renderer
        self.special_dice_value = special_dice_value
    
    def can_roll(self, mouse_pos):
        return is_point_inside_rect(mouse_pos, self.dice.get_rect())
    #Handle Animation
    def animate(self, screen, pygame, clock, debug_value=0):
        dice = self.dice
        while not dice.should_stop_roll():
            if dice.should_transition():
                dice.roll(debug_value=debug_value)
                self.draw(screen)
                pygame.display.flip()
                dice.current_frame += 1
            dt = clock.tick(60) / 1000
            dice.update_animation_time_second(dt)
        
        dice.clear_animation()
        print("Number rolled is " + str(dice.get_value()) + ".")
    
    def roll_value(self):
        return self.dice.get_value()

    def is_special_value(self, dice_value):
        return self.special_dice_value == dice_value
    
    def draw(self, screen):
        self.dice_renderer.draw(screen, self.dice)
        