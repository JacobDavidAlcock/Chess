# Chess Rules Screen

import pygame
from gui_components import Button

# Define colors
BG_COLOR = (34, 34, 34)
TEXT_COLOR = (255, 255, 255)
TITLE_COLOR = (100, 149, 237)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)

def show_rules_screen(screen, clock, width, height):
    """Display the chess rules and instructions screen"""
    
    try:
        title_font = pygame.font.SysFont("helveticaneue", 36, bold=True)
        header_font = pygame.font.SysFont("helveticaneue", 24, bold=True)
        text_font = pygame.font.SysFont("helveticaneue", 18)
        small_font = pygame.font.SysFont("helveticaneue", 16)
    except:
        title_font = pygame.font.SysFont(None, 44, bold=True)
        header_font = pygame.font.SysFont(None, 32, bold=True)
        text_font = pygame.font.SysFont(None, 24)
        small_font = pygame.font.SysFont(None, 20)
    
    # Back button
    back_button = Button(width - 120, height - 60, 100, 40, "Back", text_font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    
    # Rules content
    rules_content = [
        ("Chess Rules & Instructions", title_font, TITLE_COLOR),
        ("", text_font, TEXT_COLOR),
        ("Basic Objective:", header_font, TITLE_COLOR),
        ("• Checkmate the opponent's king", text_font, TEXT_COLOR),
        ("• Protect your own king from checkmate", text_font, TEXT_COLOR),
        ("", text_font, TEXT_COLOR),
        ("How Pieces Move:", header_font, TITLE_COLOR),
        ("• Pawn: Forward one square, captures diagonally", text_font, TEXT_COLOR),
        ("• Rook: Horizontally and vertically any distance", text_font, TEXT_COLOR),
        ("• Bishop: Diagonally any distance", text_font, TEXT_COLOR),
        ("• Knight: L-shape (2+1 squares)", text_font, TEXT_COLOR),
        ("• Queen: Combines rook and bishop moves", text_font, TEXT_COLOR),
        ("• King: One square in any direction", text_font, TEXT_COLOR),
        ("", text_font, TEXT_COLOR),
        ("Special Rules:", header_font, TITLE_COLOR),
        ("• Pawn Promotion: Pawn reaching the end promotes", text_font, TEXT_COLOR),
        ("• Castling: King and rook special move", text_font, TEXT_COLOR),
        ("• En Passant: Special pawn capture", text_font, TEXT_COLOR),
        ("", text_font, TEXT_COLOR),
        ("Game Controls:", header_font, TITLE_COLOR),
        ("• Click a piece to select it", text_font, TEXT_COLOR),
        ("• Click a highlighted square to move", text_font, TEXT_COLOR),
        ("• Use 'Hint' button for move suggestions", text_font, TEXT_COLOR),
        ("• Use 'Surrender' to resign the game", text_font, TEXT_COLOR),
        ("", text_font, TEXT_COLOR),
        ("Time Controls:", header_font, TITLE_COLOR),
        ("• Blitz: Fast-paced games (3-5 minutes)", text_font, TEXT_COLOR),
        ("• Rapid: Medium-paced games (10 minutes)", text_font, TEXT_COLOR),
        ("• Untimed: No time limit", text_font, TEXT_COLOR),
    ]
    
    scroll_offset = 0
    max_scroll = max(0, len(rules_content) * 30 - height + 100)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scroll_offset = max(0, scroll_offset - 30)
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(max_scroll, scroll_offset + 30)
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset = max(0, min(max_scroll, scroll_offset - event.y * 30))
            
            if back_button.handle_event(event):
                return
        
        # Drawing
        screen.fill(BG_COLOR)
        
        y_pos = 40 - scroll_offset
        for text, font, color in rules_content:
            if y_pos > -30 and y_pos < height:  # Only draw visible text
                if text:  # Don't render empty strings
                    text_surface = font.render(text, True, color)
                    screen.blit(text_surface, (40, y_pos))
            y_pos += 30
        
        # Draw scroll indicator if needed
        if max_scroll > 0:
            scroll_text = small_font.render("Use arrow keys or mouse wheel to scroll", True, (150, 150, 150))
            screen.blit(scroll_text, (40, height - 80))
        
        back_button.draw(screen)
        
        pygame.display.update()
        clock.tick(60)