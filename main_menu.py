import pygame
from gui_components import Button

# Define colors and fonts for a professional look
BG_COLOR = (34, 34, 34) # Dark grey
BUTTON_COLOR = (70, 130, 180) # Steel blue
BUTTON_HOVER_COLOR = (100, 149, 237) # Cornflower blue
TITLE_COLOR = (255, 255, 255) # White
TEXT_COLOR = (255, 255, 255) # White

# Main menu function
def main_menu(screen, clock, width, height):
    # Fonts
    try:
        title_font = pygame.font.SysFont("helveticaneue", 50, bold=True)
        button_font = pygame.font.SysFont("helveticaneue", 30)
    except:
        title_font = pygame.font.SysFont(None, 60, bold=True)
        button_font = pygame.font.SysFont(None, 40)
        
    title_text = title_font.render("Chess", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(width//2, 100))

    # Button Layout
    btn_width, btn_height = 300, 65
    btn_x = width // 2 - btn_width // 2
    
    # Menu states
    menu_state = "main"
    
    main_buttons = {
        "pvp": Button(btn_x, 220, btn_width, btn_height, "Player vs Player", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "ai_select": Button(btn_x, 310, btn_width, btn_height, "Player vs AI", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "exit": Button(btn_x, 400, btn_width, btn_height, "Exit", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    }
    
    ai_buttons = {
        "pva_easy": Button(btn_x, 180, btn_width, btn_height, "AI: Easy", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_hard": Button(btn_x, 270, btn_width, btn_height, "AI: Hard", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_extra_hard": Button(btn_x, 360, btn_width, btn_height, "AI: Extra Hard", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "back": Button(btn_x, 450, btn_width, btn_height, "Back", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    }

    while True:
        current_buttons = ai_buttons if menu_state == "ai_select" else main_buttons

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            for action, button in current_buttons.items():
                if button.handle_event(event):
                    if action == "exit":
                        pygame.quit()
                        quit()
                    elif action == "ai_select":
                        menu_state = "ai_select"
                    elif action == "back":
                        menu_state = "main"
                    else: # A game mode was selected
                        return action

        # Drawing
        screen.fill(BG_COLOR)
        screen.blit(title_text, title_rect)
        for button in current_buttons.values():
            button.draw(screen)
        
        pygame.display.update()
        clock.tick(60)