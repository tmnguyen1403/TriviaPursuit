from utils_local import Color

#
class IntermediateWinnerScreen:
    def __init__(self, screen, max_display_time_second):
        self.screen = screen
        self.max_display_time_second = max_display_time_second
        self.init = False

    def init_text(self, engine):
        msg = "You won! Please wait for other players to finish their turns!"
        screen_width, screen_height = self.screen.get_size()
        winner_font = engine.font.Font(None, 32)
        self.winner_text = winner_font.render(msg, True, Color.WHITE.value)
        self.winner_rect = (screen_width//2 - 6*len(msg),screen_height//2,100,100)

    def render_screen(self, engine):
        print("IntermediateWinnerScreen")
        if not self.init:
            self.init_text(engine)
            self.init = True
        
        running = True
        display = False
        time_pass = 0
        clock = engine.time.Clock()
        while running:
            for event in engine.event.get():
               if event.type == engine.QUIT:
                   running = False
                   break
            if not display:
                self.screen.fill(Color.RED.value)
                self.screen.blit(self.winner_text, self.winner_rect)
                engine.display.flip()
                display = True
            else:
                time_pass += clock.tick(60)/1000
                if time_pass > self.max_display_time_second:
                    running = False
                    display = False
                    break
