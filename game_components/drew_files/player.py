class Player:
    def __init__(self, name):
        self.score = [0,0,0,0]
        self.name = name + 1
        self.curr_pos = self.calc_start_pos()

        
    def calc_start_pos(self):
        #for testing purposes this method will assume a game board size of 600 x 600, hopefully this can be changed later
        mdpt_x = 650
        mdpt_y = 550
        if self.name == 1:
            mdpt_x -= 15
            mdpt_y -= 15
        elif self.name == 2:
            mdpt_x += 15
            mdpt_y -= 15
        elif self.name == 3:
            mdpt_x -= 15
            mdpt_y += 15
        elif self.name == 4:
            mdpt_x += 15
            mdpt_y += 15
        
        return (mdpt_x, mdpt_y)



    def update_score(self, cat_index):
        self.score[cat_index] = 1