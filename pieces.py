import pygame

# This is the base class for all chess pieces
class ChessPiece:
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # tuple representing the piece's position on the board
        
    # Method to move a piece to a new position
    def move(self, new_position):
        self.position = new_position
        return True

    # Method to draw a piece on the board
    def draw(self, surface, image):
        # Draw the piece's image on the given surface at its current position
        x, y = self.position
        surface.blit(image, ((x*50)+10, (y*50)+5))

    def copy(self, get_piece_at_position):
        return self.__class__(self.color, self.position, get_piece_at_position)

class Pawn(ChessPiece):
    def __init__(self, color, position, get_piece_at_position):
        super().__init__(color, position)
        self.image = pygame.transform.scale(pygame.image.load(f"Icons/chess-pawn-solid{'-white' if color == 'white' else ''}.png"), (30, 40))
        self.get_piece_at_position = get_piece_at_position
        # if the pawn has moved then it can't move 2 spaces
        self.first_move = True
        
    def draw(self, surface, image):
        super().draw(surface, self.image)

    def get_moves(self):
        moves = []
        x, y = self.position
        
        if self.color == 'white':
            # Forward movement
            if y < 7 and self.get_piece_at_position((x, y + 1)) is None:
                moves.append((x, y + 1))
                # First move
                if self.first_move and y < 6 and self.get_piece_at_position((x, y + 2)) is None:
                    moves.append((x, y + 2))
            
            # Diagonal captures
            if y < 7 and x > 0:
                piece = self.get_piece_at_position((x - 1, y + 1))
                if piece is not None and piece.color == 'black':
                    moves.append((x - 1, y + 1))
            if y < 7 and x < 7:
                piece = self.get_piece_at_position((x + 1, y + 1))
                if piece is not None and piece.color == 'black':
                    moves.append((x + 1, y + 1))

        elif self.color == 'black':
            # Forward movement
            if y > 0 and self.get_piece_at_position((x, y - 1)) is None:
                moves.append((x, y - 1))
                # First move
                if self.first_move and y > 1 and self.get_piece_at_position((x, y - 2)) is None:
                    moves.append((x, y - 2))

            # Diagonal captures
            if y > 0 and x > 0:
                piece = self.get_piece_at_position((x - 1, y - 1))
                if piece is not None and piece.color == 'white':
                    moves.append((x - 1, y - 1))
            if y > 0 and x < 7:
                piece = self.get_piece_at_position((x + 1, y - 1))
                if piece is not None and piece.color == 'white':
                    moves.append((x + 1, y - 1))
                
        return moves
    
    def move(self, new_position):
        super().move(new_position)
        self.first_move = False
        return True    

    def can_promote(self):
        """Check if this pawn can be promoted (reached the opposite end)"""
        x, y = self.position
        if self.color == 'white' and y == 7:
            return True
        elif self.color == 'black' and y == 0:
            return True
        return False

    def copy(self, get_piece_at_position):
        pawn_copy = super().copy(get_piece_at_position)
        pawn_copy.first_move = self.first_move
        return pawn_copy

class Rook(ChessPiece):
    def __init__(self, color, position, get_piece_at_position):
        super().__init__(color, position)
        self.get_piece_at_position = get_piece_at_position
        self.image = pygame.transform.scale(pygame.image.load(f"Icons/chess-rook-solid{'-white' if color == 'white' else ''}.png"), (30, 40))
        self.has_moved = False

    def draw(self, surface, image):
        super().draw(surface, self.image)

    def move(self, new_position):
        super().move(new_position)
        self.has_moved = True
        return True

    def copy(self, get_piece_at_position):
        rook_copy = super().copy(get_piece_at_position)
        rook_copy.has_moved = self.has_moved
        return rook_copy

    def get_moves(self):
        moves = []
        x, y = self.position
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Down, Up, Right, Left
        
        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i
                
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = self.get_piece_at_position((new_x, new_y))
                    if piece is None:
                        moves.append((new_x, new_y))
                    else:
                        if piece.color != self.color:
                            moves.append((new_x, new_y))
                        break # Stop searching in this direction
                else:
                    break # Out of bounds
        return moves
    
class Bishop(ChessPiece):
    def __init__(self, color, position, get_piece_at_position):
        super().__init__(color, position)
        self.image = pygame.transform.scale(pygame.image.load(f"Icons/chess-bishop-solid{'-white' if color == 'white' else ''}.png"), (30, 40))
        self.get_piece_at_position = get_piece_at_position

    def draw(self, surface, image):
        super().draw(surface, self.image)

    def get_moves(self):
        moves = []
        x, y = self.position

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # Diagonals
        
        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i
                
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = self.get_piece_at_position((new_x, new_y))
                    if piece is None:
                        moves.append((new_x, new_y))
                    else:
                        if piece.color != self.color:
                            moves.append((new_x, new_y))
                        break # Stop searching in this direction
                else:
                    break # Out of bounds
        return moves
    
class Knight(ChessPiece):
    def __init__(self, color, position, get_piece_at_position):
        super().__init__(color, position)
        self.image = pygame.transform.scale(pygame.image.load(f"Icons/chess-knight-solid{'-white' if color == 'white' else ''}.png"), (30, 40))
        self.get_piece_at_position = get_piece_at_position

    def draw(self, surface, image):
        super().draw(surface, self.image)
    
    def get_moves(self):
        moves = []
        x, y = self.position
        
        possible_moves = [
            (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2),
            (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1)
        ]
        
        for move in possible_moves:
            new_x, new_y = move
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.get_piece_at_position((new_x, new_y))
                if piece is None or piece.color != self.color:
                    moves.append(move)
        return moves
    
class Queen(ChessPiece):
    def __init__(self, color, position, get_piece_at_position):
        super().__init__(color, position)
        self.image = pygame.transform.scale(pygame.image.load(f"Icons/chess-queen-solid{'-white' if color == 'white' else ''}.png"), (30, 40))
        self.get_piece_at_position = get_piece_at_position

    def draw(self, surface, image):
        super().draw(surface, self.image)

    def get_moves(self):
        moves = []
        x, y = self.position

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)] # All 8 directions
        
        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i
                
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece = self.get_piece_at_position((new_x, new_y))
                    if piece is None:
                        moves.append((new_x, new_y))
                    else:
                        if piece.color != self.color:
                            moves.append((new_x, new_y))
                        break # Stop searching in this direction
                else:
                    break # Out of bounds
        return moves
    
class King(ChessPiece):
    def __init__(self, color, position, get_piece_at_position):
        super().__init__(color, position)
        self.image = pygame.transform.scale(pygame.image.load(f"Icons/chess-king-solid{'-white' if color == 'white' else ''}.png"), (30, 40))
        self.get_piece_at_position = get_piece_at_position
        self.has_moved = False

    def draw(self, surface, image):
        super().draw(surface, self.image) 

    def move(self, new_position):
        super().move(new_position)
        self.has_moved = True
        return True

    def copy(self, get_piece_at_position):
        king_copy = super().copy(get_piece_at_position)
        king_copy.has_moved = self.has_moved
        return king_copy

    def get_moves(self):
        moves = []
        x, y = self.position
        
        possible_moves = [
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)
        ]
        
        for move in possible_moves:
            new_x, new_y = move
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = self.get_piece_at_position((new_x, new_y))
                if piece is None or piece.color != self.color:
                    moves.append(move)
        return moves