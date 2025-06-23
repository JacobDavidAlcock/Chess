import pygame, main_menu, board
from ai import RandomAI, MinimaxAI, AlphaBetaAI, ExpertAI, AggressiveAI, DefensiveAI
from gui_components import Button, PromotionDialog

# Initialize the game engine
pygame.init()
pygame.mixer.init()

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
surrender_button = Button(BOARD_SIZE + 25, HEIGHT - 120, (PANEL_SIZE - 50) // 2 - 5, 40, "Surrender", ui_font, (180, 70, 70), (237, 100, 100))
hint_button = Button(BOARD_SIZE + 25 + (PANEL_SIZE - 50) // 2 + 5, HEIGHT - 120, (PANEL_SIZE - 50) // 2 - 5, 40, "Hint", ui_font, (70, 130, 180), (100, 149, 237))

# Sound Manager Class
class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            # Create simple beep sounds using pygame mixer
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            self.move_sound = self._create_simple_beep(0.1)
            self.capture_sound = self._create_simple_beep(0.15, pitch=1.2)
            self.check_sound = self._create_simple_beep(0.2, pitch=1.5)
            self.game_over_sound = self._create_simple_beep(0.3, pitch=0.8)
        except Exception as e:
            print(f"Sound system disabled: {e}")
            self.enabled = False
    
    def _create_simple_beep(self, duration, pitch=1.0):
        """Create a simple beep sound using pygame"""
        if not self.enabled:
            return None
        try:
            import numpy as np
            sample_rate = 22050
            frames = int(duration * sample_rate)
            frequency = 440 * pitch
            
            # Generate sine wave
            arr = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
            arr = (arr * 32767).astype(np.int16)
            arr = np.repeat(arr.reshape(frames, 1), 2, axis=1)
            
            sound = pygame.sndarray.make_sound(arr)
            return sound
        except ImportError:
            # Fallback: create a very simple sound without numpy
            try:
                # Even simpler approach - use pygame's built-in mixer
                sample_rate = 22050
                frames = int(duration * sample_rate)
                frequency = int(440 * pitch)
                
                # Create a simple sine wave manually
                import math
                arr = []
                for i in range(frames):
                    wave_val = int(16000 * math.sin(2 * math.pi * frequency * i / sample_rate))
                    arr.append([wave_val, wave_val])
                
                # Convert to pygame sound
                sound_array = pygame.array.array('h', [item for sublist in arr for item in sublist])
                sound = pygame.sndarray.make_sound(sound_array.reshape((frames, 2)))
                return sound
            except Exception as e:
                print(f"Sound fallback failed: {e}")
                return None
        except Exception as e:
            print(f"Sound creation failed: {e}")
            return None
    
    def play_move(self):
        if self.enabled and self.move_sound:
            try:
                self.move_sound.play()
            except:
                pass
    
    def play_capture(self):
        if self.enabled and self.capture_sound:
            try:
                self.capture_sound.play()
            except:
                pass
    
    def play_check(self):
        if self.enabled and self.check_sound:
            try:
                self.check_sound.play()
            except:
                pass
    
    def play_game_over(self):
        if self.enabled and self.game_over_sound:
            try:
                self.game_over_sound.play()
            except:
                pass

# Initialize sound manager
sound_manager = SoundManager()

class ChessClock:
    def __init__(self, time_control=None):
        self.time_control = time_control
        if time_control == "blitz_3":
            self.white_time = self.black_time = 180  # 3 minutes in seconds
        elif time_control == "blitz_5":
            self.white_time = self.black_time = 300  # 5 minutes
        elif time_control == "rapid_10":
            self.white_time = self.black_time = 600  # 10 minutes
        else:
            self.white_time = self.black_time = None  # Untimed
            
        self.last_update = pygame.time.get_ticks()
        self.active_player = None
        
    def start_turn(self, player_color):
        self.active_player = player_color
        self.last_update = pygame.time.get_ticks()
        
    def end_turn(self):
        if self.active_player and self.time_control:
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - self.last_update) / 1000.0
            
            if self.active_player == 'white':
                self.white_time = max(0, self.white_time - elapsed)
            else:
                self.black_time = max(0, self.black_time - elapsed)
                
        self.active_player = None
        
    def update(self):
        if self.active_player and self.time_control:
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - self.last_update) / 1000.0
            
            if self.active_player == 'white':
                self.white_time = max(0, self.white_time - elapsed)
            else:
                self.black_time = max(0, self.black_time - elapsed)
                
            self.last_update = current_time
            
    def is_time_up(self, player_color):
        if not self.time_control:
            return False
        time_left = self.white_time if player_color == 'white' else self.black_time
        return time_left is not None and time_left <= 0
        
    def get_time_string(self, player_color):
        if not self.time_control:
            return "∞"
        time_left = self.white_time if player_color == 'white' else self.black_time
        if time_left is None:
            return "∞"
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        return f"{minutes:02d}:{seconds:02d}"

def draw_panel(surface, current_player, is_in_check, captured_white, captured_black, chess_clock=None):
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

    # Chess clock display
    y_offset = 100
    if chess_clock and chess_clock.time_control:
        white_time = chess_clock.get_time_string('white')
        black_time = chess_clock.get_time_string('black')
        
        # White time
        white_color = (255, 255, 255) if current_player == 'white' else (180, 180, 180)
        white_surf = ui_font.render(f"White: {white_time}", True, white_color)
        surface.blit(white_surf, (PANEL_X, y_offset))
        
        # Black time
        black_color = (255, 255, 255) if current_player == 'black' else (180, 180, 180)
        black_surf = ui_font.render(f"Black: {black_time}", True, black_color)
        surface.blit(black_surf, (PANEL_X, y_offset + 25))
        
        y_offset += 70

    # Captured pieces
    for color, pieces in [("White", captured_black), ("Black", captured_white)]:
        capture_title_surf = ui_font.render(f"Captured by {color}:", True, TEXT_COLOR)
        surface.blit(capture_title_surf, (PANEL_X, y_offset))
        
        for i, piece in enumerate(pieces):
            # Draw smaller images for captured pieces
            img = pygame.transform.scale(piece.image, (20, 25))
            surface.blit(img, (PANEL_X + (i % 8) * 25, y_offset + 30 + (i // 8) * 30))
        y_offset += 150 # Increased spacing
        
    # Draw surrender and hint buttons
    surrender_button.draw(surface)
    hint_button.draw(surface)

def animate_move(piece, start_pos_board, end_pos_board, real_board_state, chess_clock=None):
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
        real_board_state.draw(surface=temp_board_surface, hint_move=None)
        screen.blit(temp_board_surface, (0, board_y_offset))
        
        # Draw the UI panel
        is_in_check = real_board_state.is_in_check('white' if moving_piece_data.color == 'black' else 'black')
        draw_panel(screen, moving_piece_data.color, is_in_check, real_board_state.captured_pieces['white'], real_board_state.captured_pieces['black'], chess_clock)
        
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
     time_control = None
     ai_player = None
     chess_clock = None
     # Set the selected piece to None
     selected_piece = None
     # Set the current player
     current_player = 'white'
     game_over = False
     game_over_message = ""
     legal_moves_for_selected_piece = []
     promotion_dialog = None
     hint_move = None  # Store the hint move to highlight
     hint_ai = MinimaxAI(current_player, depth=2)  # AI for hints
     hint_enabled = False  # Track if hints are currently shown
     move_count = 0  # Track move count for performance tuning
     last_board_hash = None  # For caching expensive calculations

     while True:
        # Call the main menu function to start the game
        if game_mode is None:
            # Reset game state for a new game
            chess_board = board.Board()
            current_player = 'white'
            game_over = False
            selected_piece = None
            
            menu_result = main_menu.main_menu(screen=screen, clock=clock, width=WIDTH, height=HEIGHT)
            game_mode, time_control = menu_result
            chess_clock = ChessClock(time_control)
            chess_clock.start_turn(current_player)
            
            if game_mode == "pva_easy":
                ai_player = RandomAI('black')
            elif game_mode == "pva_medium":
                ai_player = MinimaxAI('black', depth=2)
            elif game_mode == "pva_hard":
                ai_player = AlphaBetaAI('black', depth=3)
            elif game_mode == "pva_expert":
                ai_player = ExpertAI('black', depth=4)
            elif game_mode == "pva_aggressive":
                ai_player = AggressiveAI('black')
            elif game_mode == "pva_defensive":
                ai_player = DefensiveAI('black')
            continue # Go back to the start of the loop to process the next frame

        # --- Event Handling ---
        is_ai_turn = (game_mode in ["pva_easy", "pva_medium", "pva_hard", "pva_expert", "pva_aggressive", "pva_defensive"] and current_player == 'black')

        # Update chess clock
        if chess_clock:
            chess_clock.update()
            if chess_clock.is_time_up(current_player):
                game_over = True
                winner = 'Black' if current_player == 'white' else 'White'
                game_over_message = f"Time up! {winner} wins."
                sound_manager.play_game_over()

        if not game_over:
            if is_ai_turn:
                piece, move = ai_player.get_move(chess_board)
                if piece and move:
                    # Check if it's a capture before moving
                    is_capture = chess_board.get_piece_at_position(move) is not None
                    
                    animate_move(piece, piece.position, move, chess_board, chess_clock)
                    chess_board.move_piece(piece, piece.position, move)
                    
                    # Play appropriate sound
                    if is_capture:
                        sound_manager.play_capture()
                    else:
                        sound_manager.play_move()
                    
                    # Handle AI pawn promotion (auto-promote to queen)
                    if chess_board.promotion_pending:
                        chess_board.promote_pawn(chess_board.promotion_pending, 'queen')
                        chess_board.promotion_pending = None
                    
                    # Clear hints when AI moves
                    hint_enabled = False
                    hint_move = None
                    update_hint_button_text(hint_enabled)
                    
                    # Update chess clock
                    if chess_clock:
                        chess_clock.end_turn()
                    
                    current_player = 'white'
                    
                    # Start new turn for chess clock
                    if chess_clock:
                        chess_clock.start_turn(current_player)
                    
                    # Check game status after AI move
                    game_status = chess_board.check_game_status(current_player)
                    if game_status:
                        game_over = True
                        sound_manager.play_game_over()
                        if game_status == 'checkmate':
                            winner = 'Black'
                            game_over_message = f"Checkmate! {winner} wins."
                        else:
                            game_over_message = "Stalemate! It's a draw."
                    elif chess_board.is_in_check(current_player):
                        sound_manager.play_check()
            else: # Human player's turn
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    # Handle promotion dialog first
                    if promotion_dialog:
                        promotion_choice = promotion_dialog.handle_event(event)
                        if promotion_choice:
                            chess_board.promote_pawn(chess_board.promotion_pending, promotion_choice)
                            chess_board.promotion_pending = None
                            promotion_dialog = None
                            
                            selected_piece = None
                            legal_moves_for_selected_piece = []
                            
                            # Clear hints when promotion is completed
                            hint_enabled = False
                            hint_move = None
                            update_hint_button_text(hint_enabled)
                            
                            # Update chess clock
                            if chess_clock:
                                chess_clock.end_turn()
                            
                            current_player = 'black' if current_player == 'white' else 'white'
                            
                            # Start new turn for chess clock
                            if chess_clock:
                                chess_clock.start_turn(current_player)
                            
                            # Check game status after promotion
                            game_status = chess_board.check_game_status(current_player)
                            if game_status:
                                game_over = True
                                if game_status == 'checkmate':
                                    winner = 'White'
                                    game_over_message = f"Checkmate! {winner} wins."
                                else:
                                    game_over_message = "Stalemate! It's a draw."
                        continue  # Skip regular event handling while dialog is open

                    if surrender_button.handle_event(event):
                        game_over = True
                        winner = 'Black' if current_player == 'white' else 'White'
                        game_over_message = f"{current_player.capitalize()} surrendered. {winner} wins."
                        break # Exit event loop for this frame

                    if hint_button.handle_event(event):
                        # Toggle hint system
                        if hint_enabled and hint_move:
                            # Turn off hints
                            hint_enabled = False
                            hint_move = None
                        else:
                            # Turn on hints - calculate best move
                            hint_enabled = True
                            hint_ai.color = current_player  # Update AI color to current player
                            hint_result = hint_ai.get_move(chess_board)
                            if hint_result:
                                hint_piece, hint_target = hint_result
                                hint_move = (hint_piece.position, hint_target)
                            else:
                                hint_move = None
                        update_hint_button_text(hint_enabled)

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
                                    
                                    # Check if it's a capture before moving
                                    is_capture = chess_board.get_piece_at_position(end_pos) is not None
                                    
                                    animate_move(selected_piece, start_pos, end_pos, chess_board, chess_clock)
                                    chess_board.move_piece(selected_piece, start_pos, end_pos)
                                    
                                    # Play appropriate sound
                                    if is_capture:
                                        sound_manager.play_capture()
                                    else:
                                        sound_manager.play_move()
                                    
                                    # Check for pawn promotion
                                    if chess_board.promotion_pending:
                                        dialog_x = (WIDTH - 320) // 2
                                        dialog_y = (HEIGHT - 180) // 2
                                        promotion_dialog = PromotionDialog(dialog_x, dialog_y, chess_board.promotion_pending.color, ui_font)
                                    else:
                                        selected_piece = None
                                        legal_moves_for_selected_piece = []
                                        
                                        # Clear hints when move is made
                                        hint_enabled = False
                                        hint_move = None
                                        update_hint_button_text(hint_enabled)
                                        
                                        # Track move count for performance
                                        move_count += 1
                                        
                                        # Update chess clock
                                        if chess_clock:
                                            chess_clock.end_turn()
                                        
                                        current_player = 'black' if current_player == 'white' else 'white'
                                        
                                        # Start new turn for chess clock
                                        if chess_clock:
                                            chess_clock.start_turn(current_player)
                                        
                                        # Check game status after human move
                                        game_status = chess_board.check_game_status(current_player)
                                        if game_status:
                                            game_over = True
                                            sound_manager.play_game_over()
                                            if game_status == 'checkmate':
                                                winner = 'White'
                                                game_over_message = f"Checkmate! {winner} wins."
                                            else:
                                                game_over_message = "Stalemate! It's a draw."
                                        elif chess_board.is_in_check(current_player):
                                            sound_manager.play_check()

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
        chess_board.draw(surface=board_surface, selected_piece=selected_piece, legal_moves=legal_moves_for_selected_piece, hint_move=hint_move)
        screen.blit(board_surface, (0, board_y_offset))

        # Draw UI Panel
        is_in_check = chess_board.is_in_check(current_player)
        draw_panel(screen, current_player, is_in_check, chess_board.captured_pieces['white'], chess_board.captured_pieces['black'], chess_clock)

        # Draw promotion dialog if active
        if promotion_dialog:
            promotion_dialog.draw(screen)

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

def update_hint_button_text(hint_enabled):
    """Update hint button text based on current state"""
    global hint_button
    hint_button.text = "Hide Hint" if hint_enabled else "Show Hint"

main_loop()

# Exit the game engine
pygame.quit()


