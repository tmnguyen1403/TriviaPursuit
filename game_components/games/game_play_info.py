class GamePlayInfo:
    def __init__(self):
        self.nb_player = 4
        self.categories = []

    def set_nb_player(self, nb_player):
        self.nb_player = nb_player
    
    def set_categories(self, categories):
        self.categories = categories
    
    def get_nb_player(self):
        return self.nb_player
    
    def get_categories(self):
        return self.categories
    
    def set_debug(self):
        from category import CategoryInfo
        from utils_local import Color
        colors = [
            Color.GREEN,
            Color.BLUE,
            Color.YELLOW,
            Color.RED,
        ]
        categories = ["Sport", "History", "Math", "Movie", "Geography", "Biology"]
        self.categories = []
        for index, color in enumerate(colors):
            self.categories.append(CategoryInfo(name=categories[index], color=color.value))
        
    