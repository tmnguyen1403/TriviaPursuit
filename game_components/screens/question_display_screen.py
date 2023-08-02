from enum import Enum
from utils_local import Color
from buttons import Button, ButtonRenderer
from question import Question, QuestionManager, QuestionRenderer
from utils_local import is_point_inside_rect

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

class QuestionDisplayScreen:
    def __init__(self):
        self.state = InternalState.SHOW_QUESTION
        self.init_object = False
        self.buttons = {}
    def init_screen(self, screen):
        screen_width, screen_height = screen.get_size()
        self.question_position = (screen_width//4, screen_height//4)
        self.text_color = Color.BLACK.value
        q_w, q_h = self.question_position
        self.category_position = (screen_width//2, q_h - 50)
        self.answer_position = (q_w, 50 + q_h)

        #Button setting
        b_w, b_h = q_w//2, q_h//6
        self.show_answer_button_rect = (0, 50 + q_h, b_w, b_h)
        self.accept_button_rect = (0 + q_w, 100 + q_h, b_w, b_h)
        self.reject_button_rect = (0 + q_w*2, 100 + q_h, b_w, b_h)

    def create_button(self, rect, button_color, text:ButtonText,text_color=Color.WHITE.value, action = None):
        x,y,w,h = rect
        button = Button((x,y),(w,h), button_color, text.value, text_color, action)
        self.buttons[text] = button
        return button
        # self.button_renderer.add_button(button)

    def set_state(self, new_state: 'InternalState'):
        print(f"Current QuestionScreen state: {self.state}")
        self.state = new_state
        print(f"New QuestionScreen state: {self.state}")
        
    def render_screen(self, pygame, screen, game_manager, question):
        print("Render this question: ", question)
        if not self.init_object:
            self.init_screen(screen=screen)
            self.init_object = True
            self.button_renderer = ButtonRenderer(pygame)
            self.font = pygame.font.Font(None, 32)
        running = True
        self.game_manager = game_manager
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.state == InternalState.WAIT_ANSWER:
                            button = self.buttons[ButtonText.SHOW_ANSWER]
                            if is_point_inside_rect(mouse_pos, button.get_rect()):
                                button.on_click()
                        elif self.state == InternalState.VOTE:
                            buttons = [self.buttons[ButtonText.ACCEPT], self.buttons[ButtonText.REJECT]]
                            for button in buttons:
                                if is_point_inside_rect(mouse_pos,button.get_rect()):
                                    button.on_click()
                                    self.set_state(InternalState.SHOW_QUESTION)
                                    return
  
            if self.state == InternalState.SHOW_QUESTION:
                screen.fill(Color.WHITE.value)
                # Render Category
                category_text = question.get_category()
                category_source = self.font.render(category_text, True, self.text_color, None)
                screen.blit(category_source, self.category_position)
        
                # Render Question
                question_text = question.get_text()
                question_source = self.font.render(question_text, True, self.text_color, None)
                screen.blit(question_source, self.question_position)
                
                # Button render
                show_button = self.buttons.get(ButtonText.SHOW_ANSWER, None)
                if show_button is None:
                    show_button = self.create_button(self.show_answer_button_rect, button_color=Color.BLUE.value,text=ButtonText.SHOW_ANSWER, action=lambda:self.set_state(InternalState.SHOW_ANSWER))
                self.button_renderer.draw(screen=screen,button=show_button, font=self.font)

                self.set_state(InternalState.WAIT_ANSWER)
            elif self.state == InternalState.SHOW_ANSWER:
                #print("Show Answer State")
                 # Render Answer
                answer_text = question.get_answer()
                answer_source = self.font.render(answer_text, True, self.text_color, None)
                screen.blit(answer_source, self.answer_position)
                self.set_state(InternalState.VOTE)
            elif self.state == InternalState.VOTE:
                 # Button render
                accept_button = self.buttons.get(ButtonText.ACCEPT, None)
                if accept_button == None:
                    accept_button = self.create_button(self.accept_button_rect, button_color=(62,255,62),text=ButtonText.ACCEPT, action=lambda: self.game_manager.accept())
                reject_button = self.buttons.get(ButtonText.REJECT, None)
                if reject_button == None:
                    reject_button = self.create_button(self.reject_button_rect, button_color=Color.RED.value,text=ButtonText.REJECT, action=lambda: self.game_manager.reject())
                
                self.button_renderer.draw(screen=screen,button=accept_button, font=self.font)
                self.button_renderer.draw(screen=screen,button=reject_button, font=self.font)
            
            pygame.display.flip()