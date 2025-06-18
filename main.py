import pygame, main_menu, board
from ai import RandomAI, MinimaxAI

# Initialize the game engine
pygame.init()

# Set the width and height of the screen [width, height]
size = width, height = 400, 400
# Set the screen
screen = pygame.display.set_mode(size)
# Set the background color
background_colour = 255, 255, 255
# Set the screen background
screen.fill(background_colour)
# Set the caption
pygame.display.set_caption("Chess")
# Set the clock
clock = pygame.time.Clock()

# Create the board object
chess_board = board.Board()


# Main loop
def main_loop():
     # Set the start game variable to False
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
            
            game_mode = main_menu.main_menu(screen=screen, clock=clock, width=width, height=height)
            if game_mode == "pva_easy":
                ai_player = RandomAI('black')
            elif game_mode == "pva_hard":
                ai_player = MinimaxAI('black')
            continue # Go back to the start of the loop to process the next frame

        # --- Event Handling ---
        is_ai_turn = (game_mode in ["pva_easy", "pva_hard"] and current_player == 'black')

        if not game_over:
            if is_ai_turn:
                pygame.time.wait(100) # Short delay for AI move
                piece, move = ai_player.get_move(chess_board)
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
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = event.pos
                        x //= 50
                        y //= 50
                        if selected_piece is not None:
                            if (x, y) in legal_moves_for_selected_piece:
                                chess_board.move_piece(selected_piece, selected_piece.position, (x, y))
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

                        piece = chess_board.get_piece_at_position((x, y))
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
        # Clear the screen with the background color
        screen.fill(background_colour)
    
        # Draw the chess board and pieces
        chess_board.draw(surface=screen, selected_piece=selected_piece, legal_moves=legal_moves_for_selected_piece)

        if game_over:
            font = pygame.font.SysFont(None, 50)
            text = font.render(game_over_message, True, (255, 0, 0))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(20, 20))
            screen.blit(text, text_rect)
            
            # Add a sub-text to restart
            sub_font = pygame.font.SysFont(None, 30)
            sub_text = sub_font.render("Click anywhere to return to menu", True, (0, 0, 0))
            sub_text_rect = sub_text.get_rect(center=(width // 2, height // 2 + 40))
            screen.blit(sub_text, sub_text_rect)

        # Update the screen
        pygame.display.update()
    
        # Set the frame rate of the game to 60 FPS
        clock.tick(60)

main_loop()

# Exit the game engine
pygame.quit()


