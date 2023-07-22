from .score_tile import Score_Tile

class Score_Box:
    def __init__(self, rect, cat_colors):
        self.rect = rect
        self.cat_colors = cat_colors
        self.score_tiles = dict()
        self.total_score = 0
        self.max_score = len(cat_colors) - 2
        self.generate_score_tiles()
    def generate_score_tiles(self):
        x,y,width,height = self.rect
        
        width = width//3
        height = height//3
        #create 4 smaller rectangles inside the larger rectangle
        k=1

        # Make this more dynamic??
        for i in range(2):
            for j in range(2):
                ix = (x + (width//3)) + (i * 4 *(width//3))
                iy = (y + (height//3)) + (j * 4 *(height//3))
                cat_color = self.cat_colors[k]
                score_tile = Score_Tile(self.cat_colors[k], (ix,iy,width,height))
                self.score_tiles[cat_color] = score_tile
                k +=1

    def get_rect(self):
        return self.rect
    
    def update_score(self, category_color):
        print("Update scorebox score")
        
        score_tile = self.score_tiles[category_color]
        if score_tile.is_scored():
            print(f"Player already scored this category: {category_color}")
        else:
            self.total_score += 1
            score_tile.activate()

    def get_total_score(self):
        return self.total_score >= self.max_score
    
    def score_all_category(self):
        return self.get_total_score()
    
    def draw(self, engine, screen):
        #draw initial black box
        engine.draw.rect(screen, (0,0,0), self.rect)

        #draw the score tiles
        for cat_color, tile in self.score_tiles.items(): 
            tile.draw(engine, screen)
    
