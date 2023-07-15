import pygame
import requests

from buttons import Button, ButtonRenderer, ButtonManager
from database import dummy_database
from question_manager import QuestionManager
from gameboard import GameBoard

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


    

'''
Gameround:
1. active player roll the dice
2. 
2. active player moves according to the number of dice roll (player choose the direction to move)

'''
show_question = False
def toggle_question():
    print("Toggle question")
    global show_question
    show_question = not show_question

show_answer = False
def toggle_answer():
    print("Reveal answer")
    global show_answer
    show_answer = not show_answer 

def accept_answer():
    print("Reveal answer")
    global show_question
    global show_answer
    show_answer = False
    show_question = False

show_question_button = Button((button_x, button_y),(button_width, button_height),(0, 255, 0), "show question",(255, 255, 255) ,toggle_question)
show_answer_button = Button((button_x, button_y+100),(button_width, button_height),(0, 255, 255), "Show Answer",(255, 255, 255) , toggle_answer)
accept_answer_button = Button((button_x-200, button_y+100),(button_width, button_height),(80, 120, 255), "Accept Answer",(255, 255, 255) , accept_answer)

button_renderer = ButtonRenderer(pygame)
button_manager = ButtonManager([show_question_button, show_answer_button])
button_manager.add_button(accept_answer_button)

print("show in: ", show_question_button in button_manager.buttons)
print("show in: ", show_answer_button in button_manager.buttons)
print("position: ", button_manager.buttons.index(show_question_button))
print("position: ", button_manager.buttons.index(show_answer_button))

# Question Manager - manage the question database, get next question based on category
'''
category: [question]
get_question(category)

'''
# Question Renderer
  #Display question based on type (text, audio, video)
  #Display based on input type (textbox, multiple choice)
# Answer Renderer
  #Display answer based on type (text, audio, video)
class QuestionRenderer:
    def __init__(self, screen, position, text_color, background_color = None):
        self.screen = screen
        self.position = position
        self.text_color = text_color
        self.background_color = background_color
    def render(self, question):
        print("Hello question rendere")
        message_text = font.render(question.question_text, True, self.text_color, self.background_color)
        screen.blit(message_text, (self.position["x"],self.position["y"] - 100))

from question import Question
question = Question(("1+1=?","text",None,"2","Math"))
question_position = {"x": screen_width//2, "y": screen_height//2}


database = dummy_database()
board = GameBoard(database=database)
question_renderer = QuestionRenderer(screen=screen, position=question_position, text_color=text_color)
question_manager = QuestionManager(database=database)
board.subscribe(question_manager)

# Quick state transition
states = ["player_move","show_question"]
state = states[0]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("State: ", state)
                state = states[1]
                mouse_pos = pygame.mouse.get_pos()
                #board.move()
                #button_manager.on_click(mouse_pos)
    #screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
    screen.fill("purple")
    if state == states[1]:
        print("in state: ", state)
        print("current question: ", question_manager.current_question)
        if question_manager.current_question is None:
            print("moving board")
            board.move()
            current_question = question_manager.get_current_question()
            question_renderer.render(current_question)
        else:
            current_question = question_manager.get_current_question()
            question_renderer.render(current_question)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_n]:#up
        print("Getting next question")
        state = states[0]
        question_manager.clear_question()
    if not show_question:
        if button_manager.is_disable(show_question_button):
            button_manager.enable(show_question_button)
        button_renderer.draw(screen, show_question_button, font)
    if show_question:
        button_manager.disable(show_question_button)
        message_text = font.render(question.question_text, True, text_color)
        screen.blit(message_text, (question_position["x"],question_position["y"] - 100))
        button_renderer.draw(screen, show_answer_button, font)
        if show_answer:
            answer_text = font.render(question.answer, True, text_color)
            screen.blit(answer_text, (question_position["x"],question_position["y"] - 50))
            button_renderer.draw(screen, accept_answer_button, font)

    # Render game here
    pygame.display.flip()
    #clock tick is called at the end to maintain the desire frame rate (create delay if frame rate update is too)
    #the return value of clock tick is the elapsed time since clock tick is called (millisecond)
    clock.tick(60)
    #dt  = clock.tick(60) / 1000

pygame.quit()