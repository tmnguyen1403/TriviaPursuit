import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parrent_dir = os.path.dirname(current_dir)
sys.path.append(parrent_dir)

from enum import Enum
from utils_local import Color
from buttons import Button, ButtonRenderer
from question import Question, MediaPlayer, QuestionType, ImagePlayer
from utils_local import is_point_inside_rect, is_mac
from games import GameState
class InternalState(Enum):
    PROMPT_CATEGORY_SELECTION=0
    SHOW_QUESTION = 1
    WAIT_ANSWER = 2
    SHOW_ANSWER = 3
    VOTE = 4

class ButtonText(Enum):
    SHOW_ANSWER = "Show Answer"
    ACCEPT = "Accept"
    REJECT = "Reject"
    PLAY_MEDIA = "Play Media"
    SHOW_IMAGE = "Show Image"
class QuestionDisplayScreen:
    def __init__(self):
        self.state = InternalState.SHOW_QUESTION
        self.init_object = False
        self.buttons = {}
        if is_mac():
            self.video_player = MediaPlayer()
        else:
            self.video_player = None
        
    def init_screen(self, screen):
        screen_width, screen_height = screen.get_size()
        self.q_x, self.q_y = (screen_width//4, screen_height//4)
        self.mid_x = screen_width//2
        self.text_color = Color.BLACK.value

    def create_button(self, rect, button_color, text:ButtonText,text_color=Color.WHITE.value, action = None):
        x,y,w,h = rect
        button = Button((x,y),(w,h), button_color, text.value, text_color, action)
        self.buttons[text] = button
        return button

    def set_state(self, new_state: 'InternalState'):
        print(f"Current QuestionScreen state: {self.state}")
        self.state = new_state
        print(f"New QuestionScreen state: {self.state}")
    
    def set_external_state(self, external_state: 'GameState'):
        self.external_state = external_state


    def calc_a_y(self, question):
        if question.get_type() in [QuestionType.AUDIO, QuestionType.VIDEO, QuestionType.IMAGE]:
            print("Image question")
            a_y = self.q_y + 500

        else:
            question_text = question.get_text()
            #code to wrap text around if question is too long
            #break question into words
            words = question_text.split( )
            question_lines = []
            desired_length = 500
            #loop through words, building individual lines to be displayed
            while len(words) > 0:
                line_words = []
                while len(words) > 0:
                    line_words += [words[0]]
                    words.remove(words[0])
                    #see if the next word would exceed the desired length
                    fw,fh = self.font.size(' '.join(line_words + words[:1])) 
                    if fw > desired_length:
                        break
                question_lines += [' '.join(line_words)]
                #calculate a_y by caclulating the offset that would be produced by the question text
                y_offset = 0
                for line in question_lines:
                    fw, fh = self.font.size(line)
                    y_offset += fh
                a_y = self.q_y + y_offset
        return a_y

    def render_question(self, screen, pygame, question):
        screen.fill(Color.DEFAULT_SCREEN.value)
        self.a_y = self.calc_a_y(question)
        #draw question box
        print(f"Question a_y:{self.a_y} q_y: {self.q_y}")
        q_box_dim = ((self.mid_x - 350),(self.q_y -100),(700), (self.a_y + 100))
        qb_x,qb_y,qb_w,qb_h = q_box_dim
        pygame.draw.rect(screen,Color.BLACK.value,q_box_dim)

        #draw white box interior to larger box
        pygame.draw.rect(screen,Color.WHITE.value,(qb_x+5,qb_y+5,qb_w-10,qb_h-10))
        
        # Render Category
        category_text = question.get_category()
        category_source = self.font.render(category_text, True, self.text_color, None)
        cw,ch = self.font.size(category_text)
        category_position = (self.mid_x - (cw//2), self.q_y - 50)
        screen.blit(category_source, category_position)
        
        # Render Question
        question_text = question.get_text()
        #code to wrap text around if question is too long
        #break question into words
        words = question_text.split()
        question_lines = []
        desired_length = 500
        #loop through words, building individual lines to be displayed
        while len(words) > 0:
            line_words = []
            while len(words) > 0:
                line_words += [words[0]]
                words.remove(words[0])
                #see if the next word would exceed the desired length
                fw,fh = self.font.size(' '.join(line_words + words[:1])) 
                if fw > desired_length:
                    break
            question_lines += [' '.join(line_words)]
            #render the question line by line
            y_offset = 0
            for line in question_lines:
                fw, fh = self.font.size(line)

                # (tx, ty) is the top-left of the font surface
                tx = self.mid_x - fw / 2
                ty = self.q_y + y_offset

                font_surface = self.font.render(line, True, self.text_color, None)
                screen.blit(font_surface, (tx, ty))

                y_offset += fh

    def init_rects(self):
        #Button setting
        b_w, b_h = self.q_x//2, self.q_y//6 #button size

        #button positions
        self.show_answer_button_rect = (self.mid_x - (b_w//2), 50+ self.a_y, b_w, b_h)
        #Can play both video/audio sound track?
        self.play_media_button_rect = (self.mid_x - (b_w//2), 50 + self.a_y + 1.5*b_h, b_w, b_h)
        self.accept_button_rect = (self.mid_x - 3*(b_w//2), 100 + self.a_y, b_w, b_h)
        self.reject_button_rect = (self.mid_x + (b_w//2), 100 + self.a_y, b_w, b_h)

        # Image position on screen
        self.image_rect = (self.mid_x -100,  self.q_y, 200, 200)
        
    def render_screen(self, pygame, screen, question):
        print("Render question")
        self.set_state(InternalState.SHOW_QUESTION)
        if not self.init_object:
            self.image_player = ImagePlayer(engine=pygame, screen=screen)
            self.init_screen(screen=screen)
            self.font = pygame.font.Font(None, 32)
            self.a_y = self.calc_a_y(question)
            self.init_object = True
            self.button_renderer = ButtonRenderer(pygame)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.state == InternalState.WAIT_ANSWER:
                            buttons = [self.buttons[ButtonText.SHOW_ANSWER]]
                            for button in buttons:
                                if button is None or button.is_disable():
                                    continue
                                if is_point_inside_rect(mouse_pos, button.get_rect()):
                                    button.on_click()
                                
                        elif self.state == InternalState.VOTE:
                            buttons = [self.buttons[ButtonText.ACCEPT], self.buttons[ButtonText.REJECT]]
                            for button in buttons:
                                if is_point_inside_rect(mouse_pos,button.get_rect()):
                                    button.on_click()
                                    if self.video_player:
                                        self.video_player.reset_view()
                                    return self.external_state
                                
                        #Check to play media
                        media_button = self.buttons.get(ButtonText.PLAY_MEDIA, None)
                        if media_button and not media_button.is_disable():
                            if is_point_inside_rect(mouse_pos, media_button.get_rect()):
                                media_button.on_click()
  
            if self.state == InternalState.SHOW_QUESTION:
                self.render_question(screen, pygame, question)
                self.init_rects()
                
                # Button render
                show_button = self.buttons.get(ButtonText.SHOW_ANSWER, None)
                if show_button is None:
                    show_button = self.create_button(self.show_answer_button_rect, button_color=Color.BLUE.value,text=ButtonText.SHOW_ANSWER, action=lambda:self.set_state(InternalState.SHOW_ANSWER))
                self.button_renderer.draw(screen=screen,button=show_button, font=self.font)

                #Media Button
                media_button = self.buttons.get(ButtonText.PLAY_MEDIA, None)
                question_type =  question.get_type()
                if question_type in [QuestionType.AUDIO, QuestionType.VIDEO, QuestionType.IMAGE] and self.video_player:
                    video_url = question.get_link()
                    media_action = lambda url=video_url:self.video_player.play_video(url)
                    if question_type == QuestionType.IMAGE:
                        media_action = lambda url=video_url:self.video_player.play_image(url)

                    if media_button is None:
                        media_button = self.create_button(self.play_media_button_rect, button_color=Color.RED.value,text=ButtonText.PLAY_MEDIA, action=media_action)
                    else:
                        media_button.action = media_action
                        media_button.reveal()
                    media_button.update_text(ButtonText.SHOW_IMAGE.value if question_type == QuestionType.IMAGE else ButtonText.PLAY_MEDIA.value)

                    self.button_renderer.draw(screen=screen,button=media_button, font=self.font)
                else:
                    if media_button:
                        media_button.hide()

                self.set_state(InternalState.WAIT_ANSWER)
            elif self.state == InternalState.SHOW_ANSWER:
                #print("Show Answer State")

                self.render_question(screen, pygame, question)
                 # Render Answer
                answer_text = question.get_answer()
                answer_source = self.font.render(answer_text, True, self.text_color, None)
                aw,ah = self.font.size(answer_text)
                answer_position = (self.mid_x - (aw//2), self.a_y+ 50)
                screen.blit(answer_source, answer_position)

                self.set_state(InternalState.VOTE)
            elif self.state == InternalState.VOTE:
                 # Button render
                accept_button = self.buttons.get(ButtonText.ACCEPT, None)
                if accept_button == None:
                    accept_button = self.create_button(self.accept_button_rect, button_color=(62,255,62),text=ButtonText.ACCEPT, action=lambda: self.set_external_state(GameState.ACCEPT_ANSWER))
                reject_button = self.buttons.get(ButtonText.REJECT, None)
                if reject_button == None:
                    reject_button = self.create_button(self.reject_button_rect, button_color=Color.RED.value,text=ButtonText.REJECT, action=lambda: self.set_external_state(GameState.REJECT_ANSWER))
                
                self.button_renderer.draw(screen=screen,button=accept_button, font=self.font)
                self.button_renderer.draw(screen=screen,button=reject_button, font=self.font)

            pygame.display.flip()

if __name__ == "__main__":
    import pygame
    from utils_local import Color, is_mac, is_windows
    if not is_mac():
        print("Webgame is not supported on none Mac OS")
        exit(1)
    
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((1200, 800))
    qscreen = QuestionDisplayScreen()
    question_data = ("Test media player?",QuestionType.VIDEO.value, "https://www.youtube.com/embed/XnbCSboujF4", "You are always wrong!!",  "Music")
    question = Question(data=question_data)
    qscreen.render_screen(pygame=pygame, screen=screen,question=question)

    # Test Image
    question.link = "https://www.splashlearn.com/math-vocabulary/wp-content/uploads/2022/05/isosceles_triangles-6-01.png"
    question.mime_type = QuestionType.IMAGE
    qscreen.render_screen(pygame=pygame, screen=screen,question=question)

    #Test Video
    qscreen.render_screen(pygame=pygame, screen=screen,question=question)
    question.link = "https://www.youtube.com/embed/NzjF1pdlK7Y"
    #question.mime_type = QuestionType.TEXT
    #qscreen.render_screen(pygame=pygame, screen=screen,question=question)
    
    #Test Audio
    question.mime_type = QuestionType.AUDIO
    qscreen.render_screen(pygame=pygame, screen=screen,question=question)
