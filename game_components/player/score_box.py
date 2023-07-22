from .score_tile import Score_Tile

class Score_Box:
    def __init__(self, rect, cat_colors):
        self.rect = rect
        self.cat_colors = cat_colors
        self.generate_score_tiles()

    def generate_score_tiles(self):
        x,y,width,height = self.rect
        
        width = width//3
        height = height//3
        #create 4 smaller rectangles inside the larger rectangle
        self.score_tiles = []
        k=0

        for i in range(2):
            for j in range(2):
                ix = (x + (width//3)) + (i * 4 *(width//3))
                iy = (y + (height//3)) + (j * 4 *(height//3))
                self.score_tiles += [Score_Tile(self.cat_colors[k], (ix,iy,width,height))]
                k +=1

    def get_rect(self):
        return self.rect
    
    def draw(self, engine, screen):
        #draw initial black box
        engine.draw.rect(screen, (0,0,0), self.rect)

        #draw the score tiles
        for tile in self.score_tiles: tile.draw(engine, screen)