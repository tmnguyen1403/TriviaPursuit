from .tile_type import TileType
from utils_local import Color

class Tile:
    def __init__(self, category, color, rect, type):
        self.category = category
        self.origin_color = color
        self.color = color
        self.rect = rect #(x,y,width,height)
        self.type = type #Allows to perform certain action depending on tile
        self.border_info = (2,2, (0,0,0)) #margin_x,margin_y, color,
        self.move_candidate = False
        self.alpha = 255

        #Move animation
        self.animation_start_time_second = 0
        self.transition_duration_second = 0.5
        self.current_frame = -1
        self.shrink_width = 10
        self.shrink_height = 10
        self.animation_direction = 1

    def get_radiant_color(self):
        if self.alpha > 50 and self.animation_direction == 0:
            self.alpha -= 20
        else:
            #self.animation_direction = 1
            self.alpha += 20
            if self.alpha >= 255:
                #self.animation_direction =0
                self.alpha = 255
        r,g,b,_ = self.color
        return (r,g,b,self.alpha)
    
    def get_animate_rect(self):
        x,y,width,height = self.rect
        inner_rect = (x+self.shrink_width//2,y+self.shrink_height//2,width-self.shrink_width, height-self.shrink_height)
        if self.animation_direction == 0:
            self.shrink_width -= 10
            self.shrink_height -= 10
            if self.shrink_width < 30:
                self.animation_direction = 1
        else:
            self.shrink_width += 10
            self.shrink_height += 10
            if self.shrink_width >= width - 30:
                self.animation_direction =0

        
        return inner_rect

    def get_rect(self):
        return self.rect
    
    def get_category(self):
        return self.category
    
    def get_category_color(self):
        return self.origin_color
    
    def get_type(self):
        return self.type
    
    def set_type(self, tile_type):
        self.type = tile_type

    def draw(self, engine, screen):
        x,y,width,height = self.rect

        #this code to make borders should be obsolete
        #border_x, border_y, border_color = self.border_info
        #inner_x = x + border_x
        #inner_y = y + border_y
        #inner_width = width - border_x * 2
        #inner_height = height - border_y * 2

        if self.move_candidate:
            #draw highlighted border
            engine.draw.rect(screen, Color.HIGHLIGHT_COLOR.value, (x-5,y-5,width+10,height+10))
            engine.draw.rect(screen, Color.BLACK.value, (x-2,y-2,width+4,height+4))
            
            #draw the square
            high_rect = (x+5,y+5,width-10, height-10)
            radiant_color = self.get_radiant_color()
            engine.draw.rect(screen, radiant_color, high_rect)
        else:
            engine.draw.rect(screen, self.color, self.rect)

        # Draw headquater symbol
        if self.type == TileType.HEADQUARTER:
            font = engine.font.Font(None, 32)
            hq_text = font.render("HQ", True, Color.BLACK.value, None)
            screen.blit(hq_text, (x + width//3, y + height//3))

        # Draw trivial compute symbol
        if self.type == TileType.TRIVIA_COMPUTE:
            font = engine.font.Font(None, 32)
            hq_text = font.render("TC", True, Color.BLACK.value, None)
            screen.blit(hq_text, (x + width // 3, y + height // 3))

    def draw_move_candidate(self, engine, screen, animation_duration):
        if self.move_candidate:
            self.update_animation_time_second(animation_duration)
            if not self.should_transition():
                return
            self.current_frame += 1
            # Fill the screen            
            engine.draw.rect(screen, Color.BLACK.value,self.rect)
            #draw the square
            animate_rect = self.get_animate_rect()
            radiant_color = self.get_radiant_color()
            #print(f"draw_move: {radiant_color}")
            #print(f"draw_move rect: {animate_rect}")

            engine.draw.rect(screen, radiant_color, animate_rect)
            engine.display.flip()

    def clear_animation(self):
        self.animation_start_time_second = 0
        self.current_frame = -1
        self.alpha = 255
        self.shrink_width = 10
        self.shrink_height = 10

    def update_animation_time_second(self, duration):
        self.animation_start_time_second += duration

    def should_transition(self):
        next_frame = int(self.animation_start_time_second // self.transition_duration_second)
        return next_frame > self.current_frame
    
    def set_move_candidate(self):
        self.move_candidate = True

    def reset(self):
        self.move_candidate = False
        self.clear_animation()

        

    