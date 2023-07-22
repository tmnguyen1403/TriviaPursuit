class Score_Tile:
    def __init__(self, category_color, rect, score = 0):
        self.category_color = category_color
        self.rect = rect #contains (x,y,width,height)
        self.score = score

    def activate(self):
        self.score = 1
        
    def draw(self, engine, screen):
        if self.score == 1:
            engine.draw.rect(screen, self.category_color, self.rect)

        else:
            engine.draw.rect(screen, (255,255,255), self.rect)

'''
gameboard
player_manager
player_score[]: map players to their scorebox
whenever player answer correct on a headquater, player_manager
update the scorebox based on the player

score_tile[color]

''''

