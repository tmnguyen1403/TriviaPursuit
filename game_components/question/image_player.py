class ImagePlayer:
    def __init__(self, engine, screen):
        self.engine = engine
        self.screen = screen

    def show_image(self, img_src, rect):
        question_image = self.engine.image.load(img_src)
        x,y,img_width,img_height = rect
        scaled_image = self.engine.transform.scale(question_image, (img_width, img_height))
        self.screen.blit(scaled_image, (x,y))
