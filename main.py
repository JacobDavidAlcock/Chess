import pygame, main_menu, board

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
     startGame = False
     # Set the selected piece to None
     selected_piece = None
     # Set the current player
     current_player = 'white'
     while True:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and startGame==True:
                x, y = event.pos
                x //= 50
                y //= 50
                if selected_piece is not None:
                    if chess_board.move_piece(selected_piece, selected_piece.position, (x, y)):
                        selected_piece = None
                        if current_player == 'white':
                            current_player = 'black'
                        else:
                            current_player = 'white'
                piece = chess_board.get_piece_at_position((x, y))
                if piece is not None and piece.color is not current_player:  # Only allow white pieces to be selected
                    selected_piece = piece
                else:
                    selected_piece = None

        
        # Call the main menu function to start the game
        if startGame == False:
            if main_menu.main_menu(screen=screen, clock=clock, width=width, height=height) == "play":
                startGame = True
        elif startGame == True:
            # Clear the screen with the background color
            screen.fill(background_colour)
        
            # Draw the chess board and pieces
            chess_board.draw(surface=screen, selected_piece=selected_piece)
            # Update the screen
            pygame.display.update()
        
            # Set the frame rate of the game to 60 FPS
            clock.tick(60)

main_loop()

# Exit the game engine
pygame.quit()


