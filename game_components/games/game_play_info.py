class GamePlayInfo:
    def __init__(self):
        self.nb_player = 4
        self.categories = {}

    def set_nb_player(self, nb_player):
        self.nb_player = nb_player
    
    def set_categories(self, categories):
        self.categories = categories
    
    def get_nb_player(self):
        return self.nb_player
    
    def get_categories(self):
        return self.categories
    