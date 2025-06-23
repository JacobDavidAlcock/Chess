import pygame
from gui_components import Button
import rules_screen

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
    selected_game_mode = None
    
    main_buttons = {
        "pvp": Button(btn_x, 200, btn_width, btn_height, "Player vs Player", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "ai_select": Button(btn_x, 280, btn_width, btn_height, "Player vs AI", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "rules": Button(btn_x, 360, btn_width, btn_height, "Rules & Help", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "exit": Button(btn_x, 440, btn_width, btn_height, "Exit", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    }
    
    ai_buttons = {
        "pva_easy": Button(btn_x, 140, btn_width, btn_height, "Easy (Random)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_hard": Button(btn_x, 200, btn_width, btn_height, "Medium (Smart)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_aggressive": Button(btn_x, 260, btn_width, btn_height, "Hard (Aggressive)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_defensive": Button(btn_x, 320, btn_width, btn_height, "Hard (Defensive)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_extra_hard": Button(btn_x, 380, btn_width, btn_height, "Expert (Master)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "back": Button(btn_x, 450, btn_width, btn_height, "Back", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    }
    
    time_buttons = {
        "untimed": Button(btn_x, 160, btn_width, btn_height, "Untimed", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "blitz_3": Button(btn_x, 230, btn_width, btn_height, "Blitz (3 min)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "blitz_5": Button(btn_x, 300, btn_width, btn_height, "Blitz (5 min)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "rapid_10": Button(btn_x, 370, btn_width, btn_height, "Rapid (10 min)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "back": Button(btn_x, 440, btn_width, btn_height, "Back", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    }

    while True:
        if menu_state == "main":
            current_buttons = main_buttons
        elif menu_state == "ai_select":
            current_buttons = ai_buttons
        elif menu_state == "time_select":
            current_buttons = time_buttons
        else:
            current_buttons = main_buttons

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            for action, button in current_buttons.items():
                if button.handle_event(event):
                    if action == "exit":
                        pygame.quit()
                        quit()
                    elif action == "rules":
                        rules_screen.show_rules_screen(screen, clock, width, height)
                    elif action == "pvp":
                        selected_game_mode = "pvp"
                        menu_state = "time_select"
                    elif action == "ai_select":
                        menu_state = "ai_select"
                    elif action in ["pva_easy", "pva_hard", "pva_extra_hard", "pva_aggressive", "pva_defensive"]:
                        selected_game_mode = action
                        menu_state = "time_select"
                    elif action == "back":
                        if menu_state == "time_select":
                            menu_state = "ai_select" if selected_game_mode and "pva" in selected_game_mode else "main"
                        else:
                            menu_state = "main"
                        selected_game_mode = None
                    elif action in ["untimed", "blitz_3", "blitz_5", "rapid_10"]:
                        # Return the selected game mode with time control
                        time_control = None if action == "untimed" else action
                        return (selected_game_mode, time_control)

        # Drawing
        screen.fill(BG_COLOR)
        screen.blit(title_text, title_rect)
        for button in current_buttons.values():
            button.draw(screen)
        
        pygame.display.update()
        clock.tick(60)