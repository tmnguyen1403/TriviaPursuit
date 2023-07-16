class GameBoardRenderer:
    def __init__(self):
        pass
    def render(self,tile_objects, engine: 'pygame', screen):
        for tile in tile_objects:
            tile.draw(engine, screen)
