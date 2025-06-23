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
        button_font = pygame.font.SysFont("helveticaneue", 26)  # Slightly smaller for better fit
    except:
        title_font = pygame.font.SysFont(None, 60, bold=True)
        button_font = pygame.font.SysFont(None, 34)
        
    title_text = title_font.render("Chess", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(width//2, 100))

    # Button Layout - Better spacing
    btn_width, btn_height = 280, 50  # Slightly smaller for better fit
    btn_x = width // 2 - btn_width // 2
    btn_spacing = 70  # More consistent spacing
    
    # Menu states
    menu_state = "main"
    selected_game_mode = None
    scroll_offset = 0
    max_scroll = 0

    main_buttons = {
        "pvp": Button(btn_x, 180, btn_width, btn_height, "Player vs Player", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "ai_select": Button(btn_x, 180 + btn_spacing, btn_width, btn_height, "Player vs AI", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "rules": Button(btn_x, 180 + btn_spacing * 2, btn_width, btn_height, "Rules & Help", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "exit": Button(btn_x, 180 + btn_spacing * 3, btn_width, btn_height, "Exit", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    }
    
    ai_buttons = {
        "pva_easy": Button(btn_x, 150, btn_width, btn_height, "AI: Easy (Random)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_medium": Button(btn_x, 150 + btn_spacing, btn_width, btn_height, "AI: Medium (Minimax)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_hard": Button(btn_x, 150 + btn_spacing * 2, btn_width, btn_height, "AI: Hard (Alpha-Beta)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_expert": Button(btn_x, 150 + btn_spacing * 3, btn_width, btn_height, "AI: Expert (Deep Search)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_aggressive": Button(btn_x, 150 + btn_spacing * 4, btn_width, btn_height, "AI: Aggressive Style", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "pva_defensive": Button(btn_x, 150 + btn_spacing * 5, btn_width, btn_height, "AI: Defensive Style", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "back": Button(btn_x, 150 + btn_spacing * 6, btn_width, btn_height, "Back", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    }
    
    time_buttons = {
        "untimed": Button(btn_x, 180, btn_width, btn_height, "Untimed", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "blitz_3": Button(btn_x, 180 + btn_spacing, btn_width, btn_height, "Blitz (3 min)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "blitz_5": Button(btn_x, 180 + btn_spacing * 2, btn_width, btn_height, "Blitz (5 min)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "rapid_10": Button(btn_x, 180 + btn_spacing * 3, btn_width, btn_height, "Rapid (10 min)", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
        "back": Button(btn_x, 180 + btn_spacing * 4, btn_width, btn_height, "Back", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    }

    def update_scroll_for_menu(menu_state):
        """Calculate scroll limits for different menus"""
        if menu_state == "ai_select":
            # AI menu is longer, needs scrolling
            content_height = 150 + btn_spacing * 6 + btn_height
            return max(0, content_height - height + 100)
        else:
            return 0

    while True:
        if menu_state == "main":
            current_buttons = main_buttons
        elif menu_state == "ai_select":
            current_buttons = ai_buttons
        elif menu_state == "time_select":
            current_buttons = time_buttons
        else:
            current_buttons = main_buttons
        
        # Update max scroll for current menu
        max_scroll = update_scroll_for_menu(menu_state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and max_scroll > 0:
                    scroll_offset = max(0, scroll_offset - 30)
                elif event.key == pygame.K_DOWN and max_scroll > 0:
                    scroll_offset = min(max_scroll, scroll_offset + 30)
            elif event.type == pygame.MOUSEWHEEL and max_scroll > 0:
                scroll_offset = max(0, min(max_scroll, scroll_offset - event.y * 30))
            
            # Adjust button positions based on scroll
            for button in current_buttons.values():
                original_y = button.base_rect.y
                button.base_rect.y = original_y - scroll_offset
            
            for action, button in current_buttons.items():
                if button.handle_event(event):
                    if action == "exit":
                        pygame.quit()
                        quit()
                    elif action == "rules":
                        rules_screen.show_rules_screen(screen, clock, width, height)
                        # Reset scroll when returning from rules
                        scroll_offset = 0
                    elif action == "pvp":
                        selected_game_mode = "pvp"
                        menu_state = "time_select"
                        scroll_offset = 0  # Reset scroll
                    elif action == "ai_select":
                        menu_state = "ai_select"
                        scroll_offset = 0  # Reset scroll
                    elif action in ["pva_easy", "pva_medium", "pva_hard", "pva_expert", "pva_aggressive", "pva_defensive"]:
                        selected_game_mode = action
                        menu_state = "time_select"
                        scroll_offset = 0  # Reset scroll
                    elif action == "back":
                        if menu_state == "time_select":
                            menu_state = "ai_select" if selected_game_mode and "pva" in selected_game_mode else "main"
                        else:
                            menu_state = "main"
                        selected_game_mode = None
                        scroll_offset = 0  # Reset scroll
                    elif action in ["untimed", "blitz_3", "blitz_5", "rapid_10"]:
                        # Return the selected game mode with time control
                        time_control = None if action == "untimed" else action
                        return (selected_game_mode, time_control)
            
            # Restore button positions after event handling
            for button in current_buttons.values():
                button.base_rect.y += scroll_offset

        # Drawing
        screen.fill(BG_COLOR)
        screen.blit(title_text, title_rect)
        
        # Draw buttons with scroll offset
        for button in current_buttons.values():
            # Temporarily adjust position for drawing
            button.base_rect.y -= scroll_offset
            # Only draw if button is visible
            if button.base_rect.y > -btn_height and button.base_rect.y < height:
                button.draw(screen)
            # Restore position
            button.base_rect.y += scroll_offset
        
        # Draw scroll indicator if needed
        if max_scroll > 0:
            scroll_text = pygame.font.SysFont(None, 24).render("Use arrow keys or mouse wheel to scroll", True, (150, 150, 150))
            screen.blit(scroll_text, (40, height - 40))
        
        pygame.display.update()
        clock.tick(60)