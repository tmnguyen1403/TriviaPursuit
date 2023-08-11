
from utils_local import Color

class Legend:
    def __init__(self, categories, rect):
        self.categories = categories
        self.rect = rect

    def draw(self, engine, screen):
        x,y,width,height = self.rect


        #draw large black rectangle to act as borders
        engine.draw.rect(screen,Color.BLACK.value, self.rect)

        #calculate size of inner rectangle
        ix = x + 5
        iy = y + 5
        iw = width - 10
        ih = height - 10

        engine.draw.rect(screen, Color.WHITE.value, (ix,iy,iw,ih))

        increment = ih //len(self.categories)
        for index, category_info in enumerate(self.categories):
            
            #calculate rectangle 
            cy = iy + (increment * (index)) + 10
            cx = ix + 10
            cw = 30
            ch = 30
            
            cat_name = category_info.get_name()
            color = category_info.get_color()

            #draw colored square
            engine.draw.rect(screen, Color.BLACK.value, (cx,cy,cw,ch))
            engine.draw.rect(screen, color, (cx+5, cy+5, cw-10, ch-10))

            #draw category name 
            font = engine.font.Font(None, 32)
            text_surface = font.render(cat_name, True, Color.BLACK.value)
            screen.blit(text_surface, ((cx + cw + 10), (cy + 5 )))


