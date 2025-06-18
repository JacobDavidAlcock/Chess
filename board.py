import pygame, pieces
from pieces import King, Pawn

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.create_pieces()
        self.king_position = {'white': (4, 0), 'black': (4, 7)}

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
        for end_pos in piece.get_moves():
            undo_data = self._make_move_for_simulation(piece, start_pos, end_pos)
            if not self.is_in_check(piece.color):
                legal_moves.append(end_pos)
            self._undo_move_for_simulation(undo_data)
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
        # This is now the definitive move function. No return value needed.
        piece.move(position)
        x, y = position
        self.grid[x][y] = piece
        x, y = start
        self.grid[x][y] = None
        if isinstance(piece, King):
            self.king_position[piece.color] = position
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
    def draw(self, surface, selected_piece=None, legal_moves=[]):
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    color = (209, 139, 71)
                else:
                    color = (255, 206, 158)
                if selected_piece is not None:
                    if (x, y) in legal_moves:
                        color = (0, 255, 0)
                    elif selected_piece == self.grid[x][y]:
                        color = (255, 0, 0)
                pygame.draw.rect(surface, color, (x*50, y*50, 50, 50))
                piece = self.grid[x][y]
                if piece is not None:
                    piece.draw(surface, piece.image)

    def copy(self):
        new_board = Board()
        new_board.grid = [[piece.copy(new_board.get_piece_at_position) if piece is not None else None for piece in row] for row in self.grid]
        new_board.king_position = self.king_position.copy()
        return new_board