import pygame
import asyncio
from database import create_with_online_database
from game_manager import GameManager, GameState
from question import QuestionManager, QuestionRenderer, AnswerRenderer
from buttons import Button, ButtonManager,ButtonRenderer
from utils import Color
pygame.init()
clock = pygame.time.Clock()

# Set screen size
screen_width = 1200
screen_height = 800


'''
The below is used to generate
'''
# Define colors
colors = {0: Color.WHITE.value, 1: Color.BLUE.value, 2: Color.YELLOW.value, 3: Color.RED.value, 4: Color.GREEN.value, 5: Color.SPECIAL.value}
categories = {0: "", 1: "Math", 2: "Sport", 3: "History", 4: "Movie", 5: "Random"}
action_types = {0: "", 1: "", 2: "", 3: "", 4: "", 5: "Special"}

category_list = []
for  key, category in categories.items():
    if category == "Random" or category == "":
        continue
    category_list.append(category)
async def main_database(category_list):
    print(f"Main database: {category_list}")
    result = await create_with_online_database(categories=category_list)
    return result
question_database = asyncio.run(main_database(category_list))

#Can only have one screen, create another screen will overide existing screen
screen = pygame.display.set_mode((screen_width, screen_height))
# Create the game board surface
pygame.display.set_caption("Board Game Board")
running = True
roll = False
game_manager = GameManager()

# Init Question
question_position = {"x": screen_width//4 , "y": screen_height // 4}
question_text_color = (0,0,0)
question_font = pygame.font.Font(None, 32)
question_renderer = QuestionRenderer(screen=screen, position=question_position, text_color=question_text_color)
question_manager = QuestionManager(database=question_database)

#Init Answer
answer_font  = pygame.font.Font(None, 32)
answer_position  = (question_position["x"], screen_height//3)
answer_color = (0,0,255)
answer_renderer = AnswerRenderer(position=answer_position, text_color=answer_color)
# Button creator
def toggle_answer():
    global game_manager
    game_manager.next_state()
def accept_answer():
    global game_manager
    if game_manager.current_state == GameState.PLAYER_VOTE:
        game_manager.set_state(GameState.ACCEPT_ANSWER)
def reject_answer():
    global game_manager
    if game_manager.current_state == GameState.PLAYER_VOTE:
        game_manager.set_state(GameState.REJECT_ANSWER)

button_x = 0 + screen_width//2
button_y = screen_height//3
button_width = 200
button_height = 50
button_color = (0, 255, 0)
hover_color = (0, 200, 0)
button_font = pygame.font.Font(None, 32)

show_answer_button = Button((0, button_y),(button_width, button_height),(0, 255, 255), "Show Answer",(255, 255, 255) , toggle_answer)
accept_answer_button = Button((button_x-200, button_y+100),(button_width, button_height),(80, 120, 255), "Accept Answer",(0, 0, 255) , accept_answer)

reject_answer_button = Button((button_x+100, button_y+100),(button_width, button_height),(80, 120, 255), "Reject Answer",(255, 0, 0) , reject_answer)


button_renderer = ButtonRenderer(pygame)
button_manager = ButtonManager([show_answer_button])
button_manager.add_button(accept_answer_button)
button_manager.add_button(reject_answer_button)

game_manager.set_state(GameState.QUESTION_SELECTION)
question_manager.set_question(category="Sport")
while running:
    #Without doing pygame.event.get(), the game will not be rendered
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                current_state = game_manager.get_state()
                mouse_pos = pygame.mouse.get_pos()
                if current_state == GameState.WAIT_ROLL:
                    continue
                elif current_state == GameState.MOVE_SELECTION:
                    continue
                elif current_state == GameState.WAIT_PLAYER_ANSWER:
                    button_manager.on_click(mouse_pos=mouse_pos)
                elif current_state == GameState.PLAYER_VOTE:
                    button_manager.on_click(mouse_pos=mouse_pos)
    #Handle question
    current_state = game_manager.get_state()
    if current_state == GameState.QUESTION_SELECTION:
        screen.fill((255,255,255))
        current_question = question_manager.get_current_question()
        print("current_question in QUESTION_SELECTION: ", current_question)
        question_renderer.render(question=current_question, font=question_font)
        button_renderer.draw(screen=screen, button=show_answer_button, font=button_font)
        # for button in button_manager.buttons:
        #     button_renderer.draw(screen=screen, button=button, font=button_font)
        game_manager.next_state()
    elif current_state == GameState.ANSWER_REVEAL:
        current_question = question_manager.get_current_question()
        answer_renderer.render(screen=screen, text=current_question.answer, font=answer_font)
        button_renderer.draw(screen=screen, button=accept_answer_button, font=button_font)
        button_renderer.draw(screen=screen, button=reject_answer_button, font=button_font)

        game_manager.next_state()
    elif current_state == GameState.ACCEPT_ANSWER:
        print("Stay on the current player:")
        already_shown = False
        update_board = True
        game_manager.reset()
    elif current_state == GameState.REJECT_ANSWER:
        print("Move to the next player")
        #player_manager.next_player()
        already_shown = False
        update_board = True
        game_manager.reset()
    elif current_state == GameState.PLAYER_SELECTION:
        already_shown = False
        update_board = True
        game_manager.reset()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()