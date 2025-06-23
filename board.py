import pygame, pieces
from pieces import King, Pawn, Queen, Rook, Bishop, Knight

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.create_pieces()
        self.king_position = {'white': (4, 0), 'black': (4, 7)}
        self.captured_pieces = {'white': [], 'black': []}
        self.last_move = None  # Store (piece, start_pos, end_pos) for en passant
        self.promotion_pending = None  # Store pawn that needs promotion
        self._move_cache = {}  # Cache for expensive move calculations
        self._board_hash = None  # Cache board state hash

    # Get the piece at a given position
    def get_piece_at_position(self, position):
        x, y = position
        return self.grid[x][y]
    
    def is_in_check(self, king_color):
        king_pos = self.king_position[king_color]
        opponent_color = 'black' if king_color == 'white' else 'white'
        for x in range(8):
            for y in range(8):
                piece = self.get_piece_at_position((x, y))
                if piece is not None and piece.color == opponent_color:
                    if king_pos in piece.get_moves():
                        return True
        return False

    def get_legal_moves_for_piece(self, piece):
        legal_moves = []
        if piece is None: return []
        
        start_pos = piece.position
        
        # Get normal moves
        for end_pos in piece.get_moves():
            undo_data = self._make_move_for_simulation(piece, start_pos, end_pos)
            if not self.is_in_check(piece.color):
                legal_moves.append(end_pos)
            self._undo_move_for_simulation(undo_data)
            
        # Add castling moves for king
        if isinstance(piece, King) and not piece.has_moved:
            king_x, king_y = piece.position
            
            # Kingside castling
            rook = self.get_piece_at_position((7, king_y))
            if isinstance(rook, Rook) and self.can_castle(piece, rook):
                legal_moves.append((king_x + 2, king_y))
                
            # Queenside castling  
            rook = self.get_piece_at_position((0, king_y))
            if isinstance(rook, Rook) and self.can_castle(piece, rook):
                legal_moves.append((king_x - 2, king_y))
        
        # Add en passant moves for pawn
        if isinstance(piece, Pawn):
            pawn_x, pawn_y = piece.position
            direction = 1 if piece.color == 'white' else -1
            
            # Check left and right for en passant
            for dx in [-1, 1]:
                target_pos = (pawn_x + dx, pawn_y + direction)
                if 0 <= target_pos[0] < 8 and 0 <= target_pos[1] < 8:
                    if self.can_en_passant(piece, target_pos):
                        legal_moves.append(target_pos)
        
        return legal_moves

    def get_all_legal_moves_for_player(self, player_color):
        all_legal_moves = []
        for x in range(8):
            for y in range(8):
                piece = self.get_piece_at_position((x,y))
                if piece is not None and piece.color == player_color:
                    legal_moves_for_piece = self.get_legal_moves_for_piece(piece)
                    if legal_moves_for_piece:
                        all_legal_moves.extend(legal_moves_for_piece)
        return all_legal_moves

    def check_game_status(self, player_color):
        if not self.get_all_legal_moves_for_player(player_color):
            if self.is_in_check(player_color):
                return "checkmate"
            else:
                return "stalemate"
        return None

    # Move a piece to a given position
    def move_piece(self, piece, start, position):
        captured_piece = self.get_piece_at_position(position)
        
        # Handle en passant capture
        if isinstance(piece, Pawn) and captured_piece is None and start[0] != position[0]:
            # This is an en passant capture
            enemy_pawn_pos = (position[0], start[1])
            enemy_pawn = self.get_piece_at_position(enemy_pawn_pos)
            if enemy_pawn:
                self.captured_pieces[enemy_pawn.color].append(enemy_pawn)
                self.grid[enemy_pawn_pos[0]][enemy_pawn_pos[1]] = None
        
        # Handle castling
        if isinstance(piece, King) and abs(position[0] - start[0]) == 2:
            # This is a castling move
            king_x, king_y = start
            new_king_x, new_king_y = position
            
            if new_king_x > king_x:  # Kingside castling
                rook = self.get_piece_at_position((7, king_y))
                rook.move((new_king_x - 1, new_king_y))
                self.grid[new_king_x - 1][new_king_y] = rook
                self.grid[7][king_y] = None
            else:  # Queenside castling
                rook = self.get_piece_at_position((0, king_y))
                rook.move((new_king_x + 1, new_king_y))
                self.grid[new_king_x + 1][new_king_y] = rook
                self.grid[0][king_y] = None
        
        # Normal capture
        if captured_piece:
            self.captured_pieces[captured_piece.color].append(captured_piece)

        # Move the piece
        piece.move(position)
        x, y = position
        self.grid[x][y] = piece
        x, y = start
        self.grid[x][y] = None
        
        # Update king position
        if isinstance(piece, King):
            self.king_position[piece.color] = position
            
        # Check for pawn promotion
        if isinstance(piece, Pawn) and piece.can_promote():
            self.promotion_pending = piece
            
        # Store last move for en passant
        self.last_move = (piece, start, position)
        
        return True

    def _make_move_for_simulation(self, piece, start, end):
        captured_piece = self.get_piece_at_position(end)
        was_pawn_first_move = isinstance(piece, Pawn) and piece.first_move
        
        # Update grid and piece state for the simulation
        piece.position = end
        if was_pawn_first_move:
            piece.first_move = False

        self.grid[end[0]][end[1]] = piece
        self.grid[start[0]][start[1]] = None
        if isinstance(piece, King):
            self.king_position[piece.color] = end
        
        return (piece, start, end, captured_piece, was_pawn_first_move)

    def _undo_move_for_simulation(self, undo_data):
        piece, start, end, captured_piece, was_pawn_first_move = undo_data
        
        # Restore grid and piece state
        piece.position = start
        if was_pawn_first_move:
            piece.first_move = True

        self.grid[start[0]][start[1]] = piece
        self.grid[end[0]][end[1]] = captured_piece
        
        if isinstance(piece, King):
            self.king_position[piece.color] = start
        
    # Create the pieces
    def create_pieces(self):
        # White pawns
        for x in range(8):
            self.grid[x][1] = pieces.Pawn('white', (x, 1), self.get_piece_at_position)
        # Black pawns
        for x in range(8):
            self.grid[x][6] = pieces.Pawn('black', (x, 6), self.get_piece_at_position)
        # White rooks
        self.grid[0][0] = pieces.Rook('white', (0, 0), self.get_piece_at_position)
        self.grid[7][0] = pieces.Rook('white', (7, 0), self.get_piece_at_position)
        # Black rooks
        self.grid[0][7] = pieces.Rook('black', (0, 7), self.get_piece_at_position)
        self.grid[7][7] = pieces.Rook('black', (7, 7), self.get_piece_at_position)
        # White bishops
        self.grid[2][0] = pieces.Bishop('white', (2, 0), self.get_piece_at_position)
        self.grid[5][0] = pieces.Bishop('white', (5, 0), self.get_piece_at_position)
        # Black bishops
        self.grid[2][7] = pieces.Bishop('black', (2, 7), self.get_piece_at_position)
        self.grid[5][7] = pieces.Bishop('black', (5, 7), self.get_piece_at_position)
        # White knights
        self.grid[1][0] = pieces.Knight('white', (1, 0), self.get_piece_at_position)
        self.grid[6][0] = pieces.Knight('white', (6, 0), self.get_piece_at_position)
        # Black knights
        self.grid[1][7] = pieces.Knight('black', (1, 7), self.get_piece_at_position)
        self.grid[6][7] = pieces.Knight('black', (6, 7), self.get_piece_at_position)
        # White queen
        self.grid[3][0] = pieces.Queen('white', (3, 0), self.get_piece_at_position)
        # Black queen
        self.grid[3][7] = pieces.Queen('black', (3, 7), self.get_piece_at_position)
        # White king
        self.grid[4][0] = pieces.King('white', (4, 0), self.get_piece_at_position)
        # Black king
        self.grid[4][7] = pieces.King('black', (4, 7), self.get_piece_at_position)

    # Draw the board
    def draw(self, surface, selected_piece=None, legal_moves=[], hint_move=None):
        # Classic color scheme
        colors = [(238, 238, 210), (118, 150, 86)] # Off-white and dark green
        highlight_color = (246, 246, 130) # Yellow for legal moves
        selected_color = (186, 202, 68) # Lighter green for selected piece
        hint_color = (255, 165, 0) # Orange for hint moves
        
        for y in range(8):
            for x in range(8):
                color = colors[(x + y) % 2]
                
                if selected_piece is not None:
                    if selected_piece.position == (x,y):
                        color = selected_color
                    elif (x, y) in legal_moves:
                        color = highlight_color
                
                # Highlight hint move
                if hint_move and ((x, y) == hint_move[0] or (x, y) == hint_move[1]):
                    color = hint_color
                        
                pygame.draw.rect(surface, color, (x*50, y*50, 50, 50))
                piece = self.grid[x][y]
                if piece is not None:
                    piece.draw(surface, piece.image)

    def copy(self):
        new_board = Board()
        new_board.grid = [[piece.copy(new_board.get_piece_at_position) if piece is not None else None for piece in row] for row in self.grid]
        new_board.king_position = self.king_position.copy()
        new_board.captured_pieces = {color: list(pieces) for color, pieces in self.captured_pieces.items()}
        return new_board

    def promote_pawn(self, pawn, promotion_choice='queen'):
        """Promote a pawn to the specified piece type"""
        x, y = pawn.position
        color = pawn.color
        
        if promotion_choice == 'queen':
            new_piece = Queen(color, (x, y), self.get_piece_at_position)
        elif promotion_choice == 'rook':
            new_piece = Rook(color, (x, y), self.get_piece_at_position)
        elif promotion_choice == 'bishop':
            new_piece = Bishop(color, (x, y), self.get_piece_at_position)
        elif promotion_choice == 'knight':
            new_piece = Knight(color, (x, y), self.get_piece_at_position)
        else:
            new_piece = Queen(color, (x, y), self.get_piece_at_position)  # Default to queen
            
        self.grid[x][y] = new_piece
        return new_piece

    def can_castle(self, king, rook):
        """Check if castling is possible between king and rook"""
        if king.has_moved or rook.has_moved:
            return False
            
        # Check if squares between king and rook are empty
        king_x, king_y = king.position
        rook_x, rook_y = rook.position
        
        if king_y != rook_y:  # Must be on same rank
            return False
            
        start_x = min(king_x, rook_x) + 1
        end_x = max(king_x, rook_x)
        
        for x in range(start_x, end_x):
            if self.get_piece_at_position((x, king_y)) is not None:
                return False
                
        # Check if king is in check or would pass through check
        if self.is_in_check(king.color):
            return False
            
        # Check if king would pass through attacked squares
        direction = 1 if rook_x > king_x else -1
        for step in range(1, 3):  # King moves 2 squares
            test_pos = (king_x + step * direction, king_y)
            if self._is_square_under_attack(test_pos, king.color):
                return False
                
        return True

    def _is_square_under_attack(self, position, king_color):
        """Check if a square is under attack by the opposing color"""
        opponent_color = 'black' if king_color == 'white' else 'white'
        for x in range(8):
            for y in range(8):
                piece = self.get_piece_at_position((x, y))
                if piece is not None and piece.color == opponent_color:
                    if position in piece.get_moves():
                        return True
        return False

    def can_en_passant(self, pawn, target_pos):
        """Check if en passant capture is possible"""
        if not isinstance(pawn, Pawn):
            return False
            
        if self.last_move is None:
            return False
            
        last_piece, last_start, last_end = self.last_move
        
        # Last move must be a pawn moving 2 squares
        if not isinstance(last_piece, Pawn):
            return False
            
        if abs(last_end[1] - last_start[1]) != 2:
            return False
            
        # Target position must be the square the enemy pawn passed over
        expected_target = (last_end[0], (last_start[1] + last_end[1]) // 2)
        if target_pos != expected_target:
            return False
            
        # Pawn must be adjacent to the enemy pawn
        pawn_x, pawn_y = pawn.position
        enemy_x, enemy_y = last_end
        
        if pawn_y != enemy_y or abs(pawn_x - enemy_x) != 1:
            return False
            
        return True