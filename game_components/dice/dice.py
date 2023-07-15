import random


class Dice:
    def __init__(self, position, size, color, text_color):
        self.position = position
        self.size = size
        self.color = color
        self.roll_number = random.randint(1, 6)
        self.text_color = text_color
        self.animation_start_time_second = 0
        self.animation_duration_second = 1
        self.transition_duration_second = 0.13
        self.current_frame = -1
    #Handle Animation
    def roll(self):
        self.roll_number = random.randint(1, 6)
        return self.roll_number
    def clear_animation(self):
        self.animation_start_time_second = 0
        self.current_frame = -1
    def update_animation_time_second(self, duration):
        self.animation_start_time_second += duration
    def should_transition(self):
        next_frame = int(self.animation_start_time_second // self.transition_duration_second)
        return next_frame > self.current_frame
    def should_stop_roll(self):
        return self.animation_start_time_second >= self.animation_duration_second
    
    def get_rect(self):
        return self.position + self.size

    def get_value(self):
        return self.roll_number

    def get_color(self):
        return self.color

    def get_text_color(self):
        return self.text_color
