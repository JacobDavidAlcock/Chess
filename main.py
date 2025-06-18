import pygame, main_menu, board
from ai import RandomAI, MinimaxAI, AlphaBetaAI
from gui_components import Button

# Initialize the game engine
pygame.init()

# --- Constants and Setup ---
# Screen dimensions
BOARD_SIZE = 400
PANEL_SIZE = 250
WIDTH, HEIGHT = BOARD_SIZE + PANEL_SIZE, 600 # Increased height
size = (WIDTH, HEIGHT)

# Colors
BACKGROUND_COLOR = (49, 46, 43) # Wood-like dark brown
PANEL_COLOR = (34, 34, 34) # Dark grey for the panel
TEXT_COLOR = (255, 255, 255)
CHECK_COLOR = (255, 80, 80) # Bright red for check

# Screen setup
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
board_surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
board_y_offset = (HEIGHT - BOARD_SIZE) // 2

# Fonts
try:
    ui_font_bold = pygame.font.SysFont("helveticaneue", 28, bold=True)
    ui_font = pygame.font.SysFont("helveticaneue", 18)
    capture_font = pygame.font.SysFont("helveticaneue", 16)
except:
    ui_font_bold = pygame.font.SysFont(None, 36, bold=True)
    ui_font = pygame.font.SysFont(None, 24)
    capture_font = pygame.font.SysFont(None, 22)

# UI Elements
PANEL_X = BOARD_SIZE + 20
surrender_button = Button(BOARD_SIZE + 25, HEIGHT - 70, PANEL_SIZE - 50, 50, "Surrender", ui_font_bold, (180, 70, 70), (237, 100, 100))

def draw_panel(surface, current_player, is_in_check, captured_white, captured_black):
    """Draws the UI panel on the right side of the screen."""
    panel_rect = pygame.Rect(BOARD_SIZE, 0, PANEL_SIZE, HEIGHT)
    pygame.draw.rect(surface, PANEL_COLOR, panel_rect)

    # Turn indicator
    turn_text = f"{current_player.capitalize()}'s Turn"
    turn_surf = ui_font_bold.render(turn_text, True, TEXT_COLOR)
    surface.blit(turn_surf, (PANEL_X, 20))

    # Check indicator
    if is_in_check:
        check_surf = ui_font_bold.render("CHECK!", True, CHECK_COLOR)
        surface.blit(check_surf, (PANEL_X, 60))

    # Captured pieces
    y_offset = 120
    for color, pieces in [("White", captured_black), ("Black", captured_white)]:
        capture_title_surf = ui_font.render(f"Captured by {color}:", True, TEXT_COLOR)
        surface.blit(capture_title_surf, (PANEL_X, y_offset))
        
        for i, piece in enumerate(pieces):
            # Draw smaller images for captured pieces
            img = pygame.transform.scale(piece.image, (20, 25))
            surface.blit(img, (PANEL_X + (i % 8) * 25, y_offset + 30 + (i // 8) * 30))
        y_offset += 150 # Increased spacing
        
    # Draw surrender button
    surrender_button.draw(screen)

def animate_move(piece, start_pos_board, end_pos_board, real_board_state):
    """Animates a piece moving from start to end."""
    start_x_pixel = start_pos_board[0] * 50
    start_y_pixel = start_pos_board[1] * 50
    end_x_pixel = end_pos_board[0] * 50
    end_y_pixel = end_pos_board[1] * 50

    total_frames = 15  # Animation duration
    
    # Create a temporary board surface without the piece that is moving
    temp_board_surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
    
    # Temporarily remove piece from start to draw the underlying board
    moving_piece_data = real_board_state.get_piece_at_position(start_pos_board)
    real_board_state.grid[start_pos_board[0]][start_pos_board[1]] = None

    for frame in range(total_frames + 1):
        progress = frame / total_frames
        
        # Linear interpolation
        current_x = start_x_pixel + (end_x_pixel - start_x_pixel) * progress
        current_y = start_y_pixel + (end_y_pixel - start_y_pixel) * progress
        
        # Redraw everything
        screen.fill(BACKGROUND_COLOR)
        
        # Draw the board state (without the moving piece)
        real_board_state.draw(surface=temp_board_surface)
        screen.blit(temp_board_surface, (0, board_y_offset))
        
        # Draw the UI panel
        is_in_check = real_board_state.is_in_check('white' if moving_piece_data.color == 'black' else 'black')
        draw_panel(screen, moving_piece_data.color, is_in_check, real_board_state.captured_pieces['white'], real_board_state.captured_pieces['black'])
        
        # Draw the floating piece
        screen.blit(moving_piece_data.image, (current_x + 10, current_y + board_y_offset + 5))
        
        pygame.display.flip()
        clock.tick(60)
        
    # Restore piece to its logical start position before the final move
    real_board_state.grid[start_pos_board[0]][start_pos_board[1]] = moving_piece_data

# Main loop
def main_loop():
     # Game state variables
     chess_board = board.Board()
     game_mode = None
     ai_player = None
     # Set the selected piece to None
     selected_piece = None
     # Set the current player
     current_player = 'white'
     game_over = False
     game_over_message = ""
     legal_moves_for_selected_piece = []

     while True:
        # Call the main menu function to start the game
        if game_mode is None:
            # Reset game state for a new game
            chess_board = board.Board()
            current_player = 'white'
            game_over = False
            selected_piece = None
            
            game_mode = main_menu.main_menu(screen=screen, clock=clock, width=WIDTH, height=HEIGHT)
            if game_mode == "pva_easy":
                ai_player = RandomAI('black')
            elif game_mode == "pva_hard":
                ai_player = MinimaxAI('black')
            elif game_mode == "pva_extra_hard":
                ai_player = AlphaBetaAI('black')
            continue # Go back to the start of the loop to process the next frame

        # --- Event Handling ---
        is_ai_turn = (game_mode in ["pva_easy", "pva_hard", "pva_extra_hard"] and current_player == 'black')

        if not game_over:
            if is_ai_turn:
                piece, move = ai_player.get_move(chess_board)
                if piece and move:
                    animate_move(piece, piece.position, move, chess_board)
                    chess_board.move_piece(piece, piece.position, move)
                    current_player = 'white'
                    
                    # Check game status after AI move
                    game_status = chess_board.check_game_status(current_player)
                    if game_status:
                        game_over = True
                        if game_status == 'checkmate':
                            winner = 'Black'
                            game_over_message = f"Checkmate! {winner} wins."
                        else:
                            game_over_message = "Stalemate! It's a draw."
            else: # Human player's turn
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    if surrender_button.handle_event(event):
                        game_over = True
                        winner = 'Black' if current_player == 'white' else 'White'
                        game_over_message = f"{current_player.capitalize()} surrendered. {winner} wins."
                        break # Exit event loop for this frame

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = event.pos
                        if x < BOARD_SIZE and y >= board_y_offset and y < board_y_offset + BOARD_SIZE: # Only process clicks on the board
                            board_x = x
                            board_y = y - board_y_offset
                            board_x //= 50
                            board_y //= 50
                            if selected_piece is not None:
                                if (board_x, board_y) in legal_moves_for_selected_piece:
                                    start_pos = selected_piece.position
                                    end_pos = (board_x, board_y)
                                    
                                    animate_move(selected_piece, start_pos, end_pos, chess_board)
                                    chess_board.move_piece(selected_piece, start_pos, end_pos)
                                    
                                    selected_piece = None
                                    legal_moves_for_selected_piece = []
                                    current_player = 'black' if current_player == 'white' else 'white'
                                    
                                    # Check game status after human move
                                    game_status = chess_board.check_game_status(current_player)
                                    if game_status:
                                        game_over = True
                                        if game_status == 'checkmate':
                                            winner = 'White'
                                            game_over_message = f"Checkmate! {winner} wins."
                                        else:
                                            game_over_message = "Stalemate! It's a draw."

                            piece = chess_board.get_piece_at_position((board_x, board_y))
                            if piece is not None and piece.color == current_player:
                                selected_piece = piece
                                legal_moves_for_selected_piece = chess_board.get_legal_moves_for_piece(piece)
                            else:
                                selected_piece = None
                                legal_moves_for_selected_piece = []
        else: # Game is over
             for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game_mode = None # Return to main menu

        # --- Drawing ---
        screen.fill(BACKGROUND_COLOR)
    
        # Draw the chess board onto its own surface, then blit it to the screen
        chess_board.draw(surface=board_surface, selected_piece=selected_piece, legal_moves=legal_moves_for_selected_piece)
        screen.blit(board_surface, (0, board_y_offset))

        # Draw UI Panel
        is_in_check = chess_board.is_in_check(current_player)
        draw_panel(screen, current_player, is_in_check, chess_board.captured_pieces['white'], chess_board.captured_pieces['black'])

        if game_over:
            # Dim the screen
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0,0,0,128)) 
            screen.blit(s, (0,0))

            font = ui_font_bold
            text = font.render(game_over_message, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            screen.blit(text, text_rect)
            
            # Add a sub-text to restart
            sub_font = ui_font
            sub_text = sub_font.render("Click anywhere to return to menu", True, (200, 200, 200))
            sub_text_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(sub_text, sub_text_rect)

        # Update the screen
        pygame.display.update()
    
        # Set the frame rate of the game to 60 FPS
        clock.tick(60)

main_loop()

# Exit the game engine
pygame.quit()


