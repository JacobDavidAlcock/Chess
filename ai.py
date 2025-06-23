import random

PIECE_VALUES = {
    'Pawn': 1,
    'Knight': 3,
    'Bishop': 3,
    'Rook': 5,
    'Queen': 9,
    'King': 100
}

# Piece-Square Tables for positional evaluation
PAWN_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

PIECE_TABLES = {
    'Pawn': PAWN_TABLE,
    'Knight': KNIGHT_TABLE,
    'Bishop': BISHOP_TABLE,
    'Rook': ROOK_TABLE,
    'Queen': QUEEN_TABLE,
    'King': KING_TABLE
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
    def __init__(self, color, depth=2):  # Reduced from 2 to keep it moderate
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
        our_mobility = 0
        enemy_mobility = 0
        
        for x in range(8):
            for y in range(8):
                piece = board.get_piece_at_position((x, y))
                if piece is not None:
                    piece_type = type(piece).__name__
                    base_value = PIECE_VALUES.get(piece_type, 0)
                    
                    # Get positional bonus from piece-square tables
                    if piece_type in PIECE_TABLES:
                        table = PIECE_TABLES[piece_type]
                        # Flip table for black pieces
                        if piece.color == 'black':
                            positional_bonus = table[7-y][x] / 100.0
                        else:
                            positional_bonus = table[y][x] / 100.0
                    else:
                        positional_bonus = 0
                    
                    piece_value = base_value + positional_bonus
                    
                    if piece.color == self.color:
                        score += piece_value
                        # Count mobility for our pieces (lightweight)
                        if piece_type in ['Queen', 'Rook', 'Bishop']:  # Only major pieces for performance
                            our_mobility += len(piece.get_moves()) * 0.01
                    else:
                        score -= piece_value
                        # Count enemy mobility (lightweight)
                        if piece_type in ['Queen', 'Rook', 'Bishop']:  # Only major pieces for performance
                            enemy_mobility += len(piece.get_moves()) * 0.01
                        
        # Add mobility bonus (reduced weight for performance)
        score += (our_mobility - enemy_mobility)
        
        # King safety evaluation (simplified)
        if board.is_in_check(self.color):
            score -= 0.3
        enemy_color = 'white' if self.color == 'black' else 'black'
        if board.is_in_check(enemy_color):
            score += 0.3
            
        return score

class AlphaBetaAI(MinimaxAI):
    def __init__(self, color, depth=4): # Increased depth for highest difficulty
        super().__init__(color, depth)

    def get_move(self, board):
        best_move = None
        best_value = -float('inf')
        
        for start_pos, end_pos in self._get_all_legal_moves(board, self.color):
            piece_to_move = board.get_piece_at_position(start_pos)
            undo_data = board._make_move_for_simulation(piece_to_move, start_pos, end_pos)
            value = self.minimax(board, self.depth - 1, -float('inf'), float('inf'), False)
            board._undo_move_for_simulation(undo_data)
            
            if value > best_value:
                best_value = value
                best_move = (piece_to_move, end_pos)
                
        return best_move

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return self._evaluate_board(board)

        player_color = self.color if is_maximizing else ('white' if self.color == 'black' else 'black')
        
        if is_maximizing:
            max_eval = -float('inf')
            for start_pos, end_pos in self._get_all_legal_moves(board, player_color):
                piece_to_move = board.get_piece_at_position(start_pos)
                undo_data = board._make_move_for_simulation(piece_to_move, start_pos, end_pos)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board._undo_move_for_simulation(undo_data)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break # Prune
            return max_eval if max_eval != -float('inf') else 0
        else: # Minimizing
            min_eval = float('inf')
            for start_pos, end_pos in self._get_all_legal_moves(board, player_color):
                piece_to_move = board.get_piece_at_position(start_pos)
                undo_data = board._make_move_for_simulation(piece_to_move, start_pos, end_pos)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board._undo_move_for_simulation(undo_data)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break # Prune
            return min_eval if min_eval != float('inf') else 0 

class AggressiveAI(AlphaBetaAI):
    """AI that prefers attacking moves and piece activity"""
    def __init__(self, color, depth=3):  # Intermediate difficulty
        super().__init__(color, depth)
        
    def _evaluate_board(self, board):
        score = super()._evaluate_board(board)
        
        # Optimized bonus for attacking opponent's pieces (reduced complexity)
        enemy_color = 'white' if self.color == 'black' else 'black'
        attack_bonus = 0
        center_bonus = 0
        
        for x in range(8):
            for y in range(8):
                piece = board.get_piece_at_position((x, y))
                if piece is not None and piece.color == self.color:
                    # Center control bonus (lightweight check)
                    if 2 <= x <= 5 and 2 <= y <= 5:  # Expanded center
                        center_bonus += 0.1
                    
                    # Only check attack potential for major pieces (performance optimization)
                    if piece.__class__.__name__ in ['Queen', 'Rook', 'Bishop', 'Knight']:
                        moves = piece.get_moves()
                        for move in moves:
                            target_piece = board.get_piece_at_position(move)
                            if target_piece and target_piece.color == enemy_color:
                                # Simplified attack bonus
                                attack_bonus += 0.05
                                break  # Only count first attack per piece for performance
                                
        score += attack_bonus + center_bonus
        return score

class DefensiveAI(AlphaBetaAI):
    """AI that prefers solid, defensive moves and king safety"""
    def __init__(self, color, depth=3):  # Intermediate difficulty
        super().__init__(color, depth)
        
    def _evaluate_board(self, board):
        score = super()._evaluate_board(board)
        
        # Extra penalty for being in check
        if board.is_in_check(self.color):
            score -= 1.0
            
        # Optimized king safety evaluation
        king_pos = board.king_position[self.color]
        king_x, king_y = king_pos
        friendly_pieces_nearby = 0
        defense_bonus = 0
        
        # Check king safety (lightweight)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = king_x + dx, king_y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    piece = board.get_piece_at_position((nx, ny))
                    if piece and piece.color == self.color:
                        friendly_pieces_nearby += 1
        
        score += friendly_pieces_nearby * 0.2
        
        # Simplified piece defense evaluation (only for major pieces)
        for x in range(8):
            for y in range(8):
                piece = board.get_piece_at_position((x, y))
                if piece is not None and piece.color == self.color:
                    # Only check defense for valuable pieces
                    if piece.__class__.__name__ in ['Queen', 'Rook']:
                        # Quick check if piece is defended
                        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < 8 and 0 <= ny < 8:
                                defender = board.get_piece_at_position((nx, ny))
                                if defender and defender.color == self.color:
                                    defense_bonus += 0.05
                                    break  # Only count first defender for performance
        
        score += defense_bonus
        return score 