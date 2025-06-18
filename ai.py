import random

PIECE_VALUES = {
    'Pawn': 1,
    'Knight': 3,
    'Bishop': 3,
    'Rook': 5,
    'Queen': 9,
    'King': 100
}

class RandomAI:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        """
        Selects a random valid move for the AI.
        """
        all_pieces = []
        for x in range(8):
            for y in range(8):
                piece = board.get_piece_at_position((x, y))
                if piece is not None and piece.color == self.color:
                    all_pieces.append(piece)
        
        while True:
            # Choose a random piece
            selected_piece = random.choice(all_pieces)
            
            # Get its valid moves
            moves = selected_piece.get_moves()
            
            # If the piece has moves, choose a random one
            if moves:
                return selected_piece, random.choice(moves)

class MinimaxAI:
    def __init__(self, color, depth=2):
        self.color = color
        self.depth = depth

    def get_move(self, board):
        best_move = None
        best_value = -float('inf')
        
        for start_pos, end_pos in self._get_all_legal_moves(board, self.color):
            piece_to_move = board.get_piece_at_position(start_pos)
            undo_data = board._make_move_for_simulation(piece_to_move, start_pos, end_pos)
            value = self.minimax(board, self.depth - 1, False)
            board._undo_move_for_simulation(undo_data)
            
            if value > best_value:
                best_value = value
                best_move = (piece_to_move, end_pos)
                
        return best_move

    def minimax(self, board, depth, is_maximizing):
        if depth == 0:
            return self._evaluate_board(board)

        player_color = self.color if is_maximizing else ('white' if self.color == 'black' else 'black')
        
        if is_maximizing:
            max_eval = -float('inf')
            for start_pos, end_pos in self._get_all_legal_moves(board, player_color):
                piece_to_move = board.get_piece_at_position(start_pos)
                undo_data = board._make_move_for_simulation(piece_to_move, start_pos, end_pos)
                eval = self.minimax(board, depth - 1, False)
                board._undo_move_for_simulation(undo_data)
                max_eval = max(max_eval, eval)
            return max_eval if max_eval != -float('inf') else 0 # Return 0 if no legal moves (stalemate)
        else: # Minimizing
            min_eval = float('inf')
            for start_pos, end_pos in self._get_all_legal_moves(board, player_color):
                piece_to_move = board.get_piece_at_position(start_pos)
                undo_data = board._make_move_for_simulation(piece_to_move, start_pos, end_pos)
                eval = self.minimax(board, depth - 1, True)
                board._undo_move_for_simulation(undo_data)
                min_eval = min(min_eval, eval)
            return min_eval if min_eval != float('inf') else 0 # Return 0 if no legal moves (stalemate)

    def _get_all_legal_moves(self, board, color):
        moves = []
        for x in range(8):
            for y in range(8):
                piece = board.get_piece_at_position((x, y))
                if piece is not None and piece.color == color:
                    start_pos = (x, y)
                    for move in board.get_legal_moves_for_piece(piece):
                        moves.append((start_pos, move))
        return moves

    def _evaluate_board(self, board):
        score = 0
        for x in range(8):
            for y in range(8):
                piece = board.get_piece_at_position((x, y))
                if piece is not None:
                    value = PIECE_VALUES.get(type(piece).__name__, 0)
                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value
        return score 