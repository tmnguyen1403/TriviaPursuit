class Player:
    def __init__(self):
        self.score = [0,0,0,0]
        self.start_pos = 0 #this will be set to the center tile on the game board by default

        


    def update_score(self, cat_index):
        self.score[cat_index] = 1