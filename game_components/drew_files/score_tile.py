class Score_Tile:
    def __init__(self, category_color, rect, player_score):
        self.category_color = category_color
        self.player_score = player_score
        self.rect = rect #contains (x,y,width,height)
    

    def activate(self):
        self.active = 1
    def draw(self, engine, screen):
        if self.player_score == 1:
            engine.draw.rect(screen, self.category_color, self.rect)

        else:
            engine.draw.rect(screen, (255,255,255), self.rect)