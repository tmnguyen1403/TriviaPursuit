from typing import List
from interface import TileSubscriber
from utils import Color
from .score_box import Score_Box
from gameboard import TileType
class PlayerManager(TileSubscriber):
    """Manage Player to communicate with other system about player position
    """    
    def __init__(self, players: List['Player']) -> None:
        self.test = 0
        self.players = players
        self.current_player = players[0]
        self.current_index = 0
        self.player_scores = [None for _ in range(len(self.players))]
        self.current_tile = None
        #This is used to apply special rule for first turn move
        self.first_turn = [True for _ in range(len(self.players))]

    def init_player_score(self, category_colors, rect_size):
        index = 0
        sx,sy,sw,sh = rect_size
        margin = 300
        for player_id in range(len(self.players)):
            x = sx + (margin * index)
            y = sy
            rect = (x,y,sw,sh)
            #print(player_id)
            self.player_scores[player_id] = Score_Box(rect, category_colors)
            index += 1

    def next_player(self):
        next_index = (self.current_index + 1)%len(self.players)
        self.current_player = self.players[next_index]
        self.current_index = next_index
        print(f"Next player index: {self.current_index}")

    def update(self, tile ,matrix_position):
        print("Update current player position")
        self.current_player.update(matrix_position)
        if self.is_first_turn():
            self.first_turn[self.current_index] = False
        self.current_tile = tile
    
    def is_first_turn(self):
        return self.first_turn[self.current_index]
    
    def update_all(self,new_position):
        for player in self.players:
            player.update(new_position)

    def get_current_player(self):
        return self.current_player
    
    def get_current_player_position(self):
        return self.current_player.get_position()
    
    def move(self, dice_manager: 'DiceManager'):
        dice_value = dice_manager.dice.get_value()
        print("inside player manager: ", dice_value)
        return None
    
    def get_players(self):
        return self.players
    
    def update_player_score(self):
        if self.current_tile.get_type() == TileType.HEADQUATER:
            category_color = self.current_tile.get_category_color()
            self.player_scores[self.current_index].update_score(category_color)

    def player_score_all_category(self):
        return self.player_scores[self.current_index].score_all_category()

    def draw_score(self, engine, screen):
        for index, score_box in enumerate(self.player_scores):
            score_box.draw(engine, screen)
        
            #draw player name next to score_box:
            x,y,w,h = score_box.get_rect()
            text = "Player " + str(self.players[index].name) + ":"
            font = engine.font.Font(None, 32)
           # surface_color = (125,125,125) #screen.get_at((x,y))
            text_surface = font.render(text, True, Color.BLACK.value)
            textbox_x = x - 120
            textbox_width = text_surface.get_width() + 10
            textbox_height = text_surface.get_height() + 10
            
            engine.draw.rect(screen, Color.DEFAULT_SCREEN.value, (textbox_x, y, textbox_width, textbox_height))
            screen.blit(text_surface, (textbox_x + 5, y + 5))

            #Draw playing token
            if self.current_index == index:
                token_x, token_y = x - 60,y + 50
                engine.draw.circle(screen, "red", (token_x,token_y), 20)

