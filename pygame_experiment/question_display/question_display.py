import pygame
import requests

#setup
pygame.init()
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

#Button test
button_width = 200
button_height = 50
button_color = (0, 255, 0)
hover_color = (0, 200, 0)

text_color = (255, 255, 255)
font = pygame.font.Font(None, 32)

#TODO:
'''
1. Get question
2. Determine question type (text, audio, video)
3. Display question based on approriate type
4. Display answer if it is multiple choice
'''

# Define button position
button_x = (screen_width - button_width) // 2
button_y = (screen_height - button_height) // 2
message = None

def is_point_inside_rect(point, rect):
    x, y = point
    rect_x, rect_y, rect_width, rect_height = rect
    return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height
button_text_rect = None 

#Question object
class Question:
    def __init__(self):
        self.text = "What is your name?"
        self.type = "text" #text, audio, video question
        self.source = None # Use for audio/video question
        self.answer = "My name is KK" # Store correct answer
        self.category = "Geology" #
'''
{
    question_id(object_id): "",
    question: "",
    type: "",
    answer: "",
    link: "link_to_audio/link_to_video" #Optional,
    category: "",
    user_id: dummy_userID
}

'''
'''
Game screens: [landing_screen, in_game]

Game screen: [in_game]
Game state: [player_movement, showing_question, answering, showing_answer, determine_correctness]

[game screen, game state] : [in_game, showing_question]
click on button --> 
  display question --> how? Which questions to display?
  QuestionManager:
     question objects?  
  QuestionRenderer:
    draw(question)
  
  new_question = question_manager.get_question()
  question_renderer.draw(new_question)


'''

class Button:
    def __init__(self, position, size, color, text, text_color, action):
        self.position = position
        self.size = size
        self.color = color
        self.text = text
        self.text_color = text_color
        self.action = action
    def get_rect(self):
        return self.position + self.size
    def on_click(self):
        self.action()

class ButtonRenderer:
    def __init__(self,engine):
        self.engine = engine
    def draw(self, screen, button, font):
        button_rect = button.get_rect()
        self.engine.draw.rect(screen, button.color, button_rect)
        button_text = font.render(button.text, True, button.text_color)
        x,y,w,h = button_rect
        button_text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(button_text, button_text_rect)

class ButtonManager:
    def __init__(self, buttons = None):
        self.buttons = buttons
        if self.buttons is None:
          self.buttons = []
    def add_button(self, button):
        self.buttons.append(button)
    def is_point_inside_rect(self, point, rect):
      x, y = point
      rect_x, rect_y, rect_width, rect_height = rect
      return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height
    def on_click(self, mouse_pos):
        for button in self.buttons:
          if self.is_point_inside_rect(mouse_pos, button.get_rect()):
              button.on_click()
              print("Click on button")
              break
    
      
show_question_button = Button((button_x, button_y),(button_width, button_height),(0, 255, 0), "show question",(255, 255, 255) ,lambda: print("Question"))
button_renderer = ButtonRenderer(pygame)
button_manager = ButtonManager([show_question_button])
# Question Renderer
  #Display question based on type (text, audio, video)
  #Display based on input type (textbox, multiple choice)
# Answer Renderer
  #Display answer based on type (text, audio, video)

question = Question()
question_position = {"x": screen_width//2, "y": screen_height//2}
#
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
              mouse_pos = pygame.mouse.get_pos()
              button_manager.on_click(mouse_pos)
    #screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
    screen.fill("purple")
    button_renderer.draw(screen, show_question_button, font)
    #message_text = font.render(question.text, True, text_color)
    #screen.blit(message_text, (question_position["x"],question_position["y"]))
    # Render game here
    pygame.display.flip()
    #clock tick is called at the end to maintain the desire frame rate (create delay if frame rate update is too)
    #the return value of clock tick is the elapsed time since clock tick is called (millisecond)
    clock.tick(60)
    #dt  = clock.tick(60) / 1000

pygame.quit()