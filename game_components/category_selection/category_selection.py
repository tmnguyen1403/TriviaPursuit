import pygame
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Trivial Pursuit")

category_data = [
        {"category": "Sport", "color_name": "Red", "color_code": (255, 0, 0)},
        {"category": "History", "color_name": "Green", "color_code": (0, 255, 0)},
        {"category": "Math", "color_name": "Blue", "color_code": (0, 0, 255)},
        {"category": "Movie", "color_name": "Orange", "color_code": (255, 165, 0)},
        {"category": "Geography", "color_name": "Magenta", "color_code": (255, 0, 255)},
        {"category": "Biology", "color_name": "Cyan", "color_code": (0, 255, 255)},
]

def show_category_selection(selected_categories, category_data):
    screen.fill((255, 255, 255))

    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 38)

    spacing = 50
    y_offset = 200
    category_buttons = []

    # Render the title
    title_text = title_font.render("Select 4 Categories", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(screen_width // 2, 125))
    screen.blit(title_text, title_rect)

    # Draw the underline for the title
    underline_start = (title_rect.left, title_rect.bottom)
    underline_end = (title_rect.right, title_rect.bottom)
    pygame.draw.line(screen, (30, 30, 30), underline_start, underline_end, 2)

    for index, category_info in enumerate(category_data):
        category = category_info["category"]
        color_code = category_info["color_code"]

        # Create the text surface
        text = font.render(f"{category}", True, color_code)

        # Create the button rectangle and center the text within it
        button_rect = pygame.Rect(0, 0, 200, text.get_height() + 20)
        button_rect.center = (screen_width // 2, y_offset + index * spacing)

        category_buttons.append(button_rect)

        if category in selected_categories:
            pygame.draw.rect(screen, color_code, button_rect, 4)

        # Center the text within the button rectangle
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    pygame.display.update()
    return category_buttons

def category_selection():
    selected_categories = set()

    category_buttons = show_category_selection(selected_categories, category_data)

    while len(selected_categories) < 4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    toggle_category_selection(category_data[0]["category"], selected_categories)
                elif event.key == pygame.K_2:
                    toggle_category_selection(category_data[1]["category"], selected_categories)
                elif event.key == pygame.K_3:
                    toggle_category_selection(category_data[2]["category"], selected_categories)
                elif event.key == pygame.K_4:
                    toggle_category_selection(category_data[3]["category"], selected_categories)
                elif event.key == pygame.K_5:
                    toggle_category_selection(category_data[4]["category"], selected_categories)
                elif event.key == pygame.K_6:
                    toggle_category_selection(category_data[5]["category"], selected_categories)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for index, button_rect in enumerate(category_buttons):
                    if button_rect.collidepoint(mouse_pos):
                        toggle_category_selection(category_data[index]["category"], selected_categories)

        show_category_selection(selected_categories, category_data)

    return selected_categories

def toggle_category_selection(category, selected_categories):
    # Helper function to toggle the selected category on and off
    if category in selected_categories:
        selected_categories.remove(category)
    else:
        selected_categories.add(category)

def get_game_categories(game_categories):

    selected_categories = category_selection()

    for category_info in category_data:
        category = category_info["category"]
        color_name = category_info["color_name"]
        if category in selected_categories:
            game_categories[color_name] = category

    return game_categories