from utils_local import Color

#
class IntermediateWinnerScreen:
    def __init__(self, screen, max_display_time_second):
        self.screen = screen
        self.init = False
        self.max_display_time_second = max_display_time_second
    def render_screen(self, engine):
        print("IntermediateWinnerScreen")
        if not self.init:
            self.clock = engine.time.Clock()
            self.init = True
        running = True
        display = False
        time_pass = 0
        while running:
            for event in engine.event.get():
               if event.type == engine.QUIT:
                   running = False
                   break
            if not display:
                msg = "You won! Please wait for other players to finish their turns!"
                self.screen.fill(Color.DEFAULT_SCREEN.value)
                screen_width, screen_height = self.screen.get_size()
                winner_font = engine.font.Font(None, 32)
                winner_text = winner_font.render(msg, True, Color.RED.value)
                winner_rect = (screen_width//2 - 6*len(msg),screen_height//2,100,100)
                display = True 
                self.screen.blit(winner_text, winner_rect)
                engine.display.flip()
            else:
                time_pass += self.clock.tick(60)/1000
                if time_pass > self.max_display_time_second:
                    running = False
                    display = False
                    break
