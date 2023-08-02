from typing import List
from interface import TileSubscriber
from utils_local import Color
from .score_box import Score_Box
from gameboard import TileType
class PlayerManager(TileSubscriber):
    """Manage Player to communicate with other system about player position
    """    
    def __init__(self, players: List['Player'], start_player = 0) -> None:
        
        self.players = players
        self.start_player = start_player 
        self.current_player = players[0]
        self.current_index = start_player
        self.player_scores = [None for _ in range(len(self.players))]
        self.current_tile = None
        #This is used to apply special rule for first turn move
        self.first_turn = [True for _ in range(len(self.players))]
        self.winners = []
        self.last_player_move = False
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
        if next_index == self.start_player:
            self.last_player_move = True
        else:
            self.last_player_move = False

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

    def get_current_player_tile(self):
        return self.current_tile
    
    def get_players(self):
        return self.players

    def update_player_score(self):
        tile_type = self.current_tile.get_type()
        if tile_type == TileType.HEADQUATER:
            category_color = self.current_tile.get_category_color()
            self.player_scores[self.current_index].update_score(category_color)
        elif tile_type == TileType.TRIVIA_COMPUTE and self.player_score_all_category():
            self.winners.append(self.current_index)

    def has_winner(self):
        return len(self.winners) > 0
    
    def is_last_player_move(self):
        return self.last_player_move
    
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
            token_x, token_y = x - 60,y + 50
            if self.current_index == index:
                engine.draw.circle(screen, "red", (token_x,token_y), 20)
            
            # Draw Winner
            if self.is_last_player_move():
                if index in self.winners:
                    winner_text = "Winner"
                    winner_font = engine.font.Font(None, 30)
                    winner_surface = winner_font.render(winner_text, True, Color.RED.value)
                    w_x,w_y = token_x - 20, token_y + 20
                    w_width,w_height = textbox_width, textbox_height
                    # engine.draw.rect(screen, Color.DEFAULT_SCREEN.value, (w_x, w_y, w_width, w_height))
                    screen.blit(winner_surface, (w_x, w_y))




