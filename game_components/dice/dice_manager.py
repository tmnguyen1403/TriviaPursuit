import random
class DiceManager:
    def __init__(self, dice: 'Dice', dice_renderer: 'DiceRenderer'):
        self.dice = dice
        self.dice_renderer = dice_renderer
    #Handle Animation
    def animate(self, screen, pygame, clock):
        dice = self.dice
        while not dice.should_stop_roll():
            if dice.should_transition():
                dice.roll()
                self.draw(screen)
                pygame.display.flip()
                dice.current_frame += 1
            dt = clock.tick(60) / 1000
            dice.update_animation_time_second(dt)
        
        dice.clear_animation()
        print("Number rolled is " + str(dice.get_value()) + ".")
    def roll_value(self):
        return self.dice.get_value()
    
    def draw(self, screen):
        self.dice_renderer.draw(screen, self.dice)
        