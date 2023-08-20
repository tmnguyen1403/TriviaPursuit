from utils_local import Color
class GameBoardRenderer:
    def __init__(self):
        self.active_player_color = Color.WHITE.value
        self.inactive_player_color = Color.BLACK.value
        self.active_text_color = Color.BLACK.value

    def render(self,tile_objects, engine: 'pygame', screen):
        for tile in tile_objects:
            tile.draw(engine, screen)
    
    def render_player(self, gameboard, engine: 'pygame', screen, player_manager):
        players = player_manager.get_players()
        tile_map = gameboard.get_tile_map()
        player_tile = dict()
        
        for player in players:
            pos = player.get_position()
            if player_tile.get(pos, None) is None:
                player_tile[pos] = list()
            player_tile[pos].append(player)
            #print("player color: ", player.get_color())
        for pos, count in player_tile.items():
            tile = tile_map[pos]
            x,y,w,h = tile.get_rect()
            tile_players = player_tile[pos]
            nb_players = len(tile_players)
            arrangement_dict = dict()
            arrangement_dict[1] = [(0,0)]
            arrangement_dict[2] = [(0,-20),(0,20)]
            arrangement_dict[3] = [(-w//4,-h//4),(w//4,-h//4), (0,0)]
            arrangement_dict[4] = [(-w//4,-h//4),(w//4,-h//4), (-w//4,h//4),(w//4,h//4)]
            arrangements = arrangement_dict[nb_players]
            
            for index, player in enumerate(tile_players):
                name = player.get_name()
                color = player.get_color()
                padding_x, padding_y = arrangements[index]
                print("Player color: ", color)
                px,py = x+w//2 + padding_x, y + h//2 + padding_y
                font = engine.font.Font(None, 20)
                circle_color = self.active_player_color if player_manager.is_current_player(player) else self.inactive_player_color
                engine.draw.circle(screen, circle_color, (px, py),(w//4)-3)
                engine.draw.circle(screen, color, (px, py),(w//4)-6)
                text_color = self.active_text_color if player_manager.is_current_player(player) else self.inactive_player_color
                player_text = font.render(name,True,text_color, None)
                screen.blit(player_text,(px-8,py-6))
    
    def render_player_score(self, engine: 'pygame', screen, player_manager):
        player_manager.draw_score(engine, screen)
