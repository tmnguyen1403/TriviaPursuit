
class Score_Tile:
    def __init__(self, category_color, rect, scored = 0):
        self.category_color = category_color
        self.rect = rect #contains (x,y,width,height)
        self.scored = scored

    def activate(self):
        print(f"Player score this category: {self.category_color}")
        self.scored = 1

    def is_scored(self):
        return self.scored == 1
    
    def draw(self, engine, screen):
        if self.scored == 1:
            #print("Draw tile when player scored")
            engine.draw.rect(screen, self.category_color, self.rect)
        else:
            engine.draw.rect(screen, (255,255,255), self.rect)
