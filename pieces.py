import pygame

# This is the base class for all chess pieces
class ChessPiece:
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # tuple representing the piece's position on the board
        
    # Method to move a piece to a new position
    def move(self, new_position):
        # Check if the move is valid and then move the piece
        if new_position in self.get_moves():
            self.position = new_position
            return True

    # Method to draw a piece on the board
    def draw(self, surface, image):
        # Draw the piece's image on the given surface at its current position
        x, y = self.position
        surface.blit(image, ((x*50)+10, (y*50)+5))

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
            # if its the first move of the pawn then it can move 2 spaces
            if self.first_move:
                # if there is no piece infront of the pawn then it can move 2 spaces
                if self.get_piece_at_position((x, y+2)) is None and self.get_piece_at_position((x, y+1)) is None:
                    moves.append((x, y+2))
            # if any piece is infront of the pawn then it can't move
            if y < 7 and self.get_piece_at_position((x, y+1)) is None:
                moves.append((x, y+1))
            # if there is not a piece behind the pawn then it can move 1 space back
            if y > 0 and self.get_piece_at_position((x, y-1)) is None:
                moves.append((x, y-1))
            # if the piece is not on the first row
                # if the piece on the left diagonal is black 
            if x > 0 and y < 7 and self.get_piece_at_position((x-1, y+1)) is not None:
                if self.get_piece_at_position((x-1, y+1)).color == "black":
                    moves.append((x-1, y+1))
                # if the piece on the right diagonal is black
            if x < 7 and y < 7 and self.get_piece_at_position((x+1, y+1)) is not None:
                if self.get_piece_at_position((x+1, y+1)).color == "black":
                    moves.append((x+1, y+1))
        elif self.color == 'black':
            # if its the first move of the pawn then it can move 2 spaces
            if self.first_move:
                # if there is no piece infront of the pawn then it can move 2 spaces
                if self.get_piece_at_position((x, y-2)) is None and self.get_piece_at_position((x, y-1)) is None:
                    moves.append((x, y-2))
            # if any piece is infront of the pawn then it can't move
            if y > 0 and self.get_piece_at_position((x, y-1)) is None:
                moves.append((x, y-1))
            if y < 7 and self.get_piece_at_position((x, y+1)) is None:
                moves.append((x, y+1))
            # if the piece is not on the first row
                # if the piece on the left diagonal is black 
            if x > 0 and y > 0 and self.get_piece_at_position((x-1, y-1)) is not None:
                if self.get_piece_at_position((x-1, y-1)).color is "white":
                    moves.append((x-1, y-1))
                # if the piece on the right diagonal is black
            if x < 7 and y > 0 and self.get_piece_at_position((x+1, y-1)) is not None:
                if self.get_piece_at_position((x+1, y-1)).color is "white":
                    moves.append((x+1, y-1))
        return moves
    
    def move(self, new_position):
        if super().move(new_position):
            self.first_move = False
            return True    

class Rook(ChessPiece):
    def __init__(self, color, position, get_piece_at_position):
        super().__init__(color, position)
        self.get_piece_at_position = get_piece_at_position
        self.image = pygame.transform.scale(pygame.image.load(f"Icons/chess-rook-solid{'-white' if color == 'white' else ''}.png"), (30, 40))

    def draw(self, surface, image):
        super().draw(surface, self.image)

    def get_moves(self):
        moves = []
        x, y = self.position
        for i in range(1, 8):
            # Right
            if x + i < 8:
                if self.get_piece_at_position((x+i, y)) is None:
                    add=True
                    for j in range(1, i):
                        if self.get_piece_at_position((x+j, y)) is not None:
                            add=False
                    if add:
                        moves.append((x+i, y))
                else:
                    if self.get_piece_at_position((x+i, y)).color != self.color:
                        add=True
                        for j in range(1, i):
                            if self.get_piece_at_position((x+i, y)) is not None:
                                add=False
                        if add:
                            moves.append((x+i, y))
            # Left
            if x - i >= 0:
                if self.get_piece_at_position((x-i, y)) is None:
                    add=True
                    for j in range(1, i):
                        if self.get_piece_at_position((x-j, y)) is not None:
                            add=False
                    if add:
                        moves.append((x-i, y))
                else:
                    if self.get_piece_at_position((x-i, y)).color != self.color:
                        add=True
                        for j in range(1, i):
                            if self.get_piece_at_position((x-i, y)) is not None:
                                add=False
                        if add:
                            moves.append((x-i, y))
            # Down
            if y + i < 8:
                if self.get_piece_at_position((x, y+i)) is None:
                    add=True
                    for j in range(1, i):
                        if self.get_piece_at_position((x, y+j)) is not None:
                            add=False
                    if add:
                        moves.append((x, y+i))
                else:
                    if self.get_piece_at_position((x, y+i)).color != self.color:
                        add=True
                        for j in range(1, i):
                            if self.get_piece_at_position((x, y+i)) is not None:
                                add=False
                        if add:
                            moves.append((x, y+i))
            # Up
            if y - i >= 0:
                if self.get_piece_at_position((x, y-i)) is None:
                    add=True
                    for j in range(1, i):
                        if self.get_piece_at_position((x, y-j)) is not None:
                            add=False
                    if add:
                        moves.append((x, y-i))
                else:
                    if self.get_piece_at_position((x, y-i)).color != self.color:
                        add=True
                        for j in range(1, i):
                            if self.get_piece_at_position((x, y-j)) is not None:
                                add=False
                        if add:
                            moves.append((x, y-i))
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
        for i in range(1, 8):
            # Right down diagonal
            if x + i < 8 and y + i < 8:
                if self.get_piece_at_position((x+i, y+i)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x+j, y+j)) is not None:
                            add = False
                    if add:
                        moves.append((x+i, y+i))
                elif self.get_piece_at_position((x+i, y+i)) is not None:
                    if self.get_piece_at_position((x+i, y+i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x+j, y+j)) is not None:
                                add = False
                        if add:
                            moves.append((x+i, y+i))
            # Left up diagonal
            if x - i >= 0 and y - i >= 0:
                if self.get_piece_at_position((x-i, y-i)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x-j, y-j)) is not None:
                            add = False
                    if add:
                        moves.append((x-i, y-i))
                elif self.get_piece_at_position((x-i, y-i)) is not None:
                    if self.get_piece_at_position((x-i, y-i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x-j, y-j)) is not None:
                                add = False
                        if add:
                            moves.append((x-i, y-i))
            # Right up diagonal
            if x + i < 8 and y - i >= 0: 
                if self.get_piece_at_position((x+i, y-i)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x+j, y-j)) is not None:
                            add = False
                    if add:
                        moves.append((x+i, y-i))
                elif self.get_piece_at_position((x+i, y-i)) is not None:
                    if self.get_piece_at_position((x+i, y-i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x+j, y-j)) is not None:
                                add = False
                        if add:
                            moves.append((x+i, y-i))
            # Left down diagonal
            if x - i >= 0 and y + i < 8: 
                if self.get_piece_at_position((x-i, y+i)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x-j, y+j)) is not None:
                            add = False
                    if add:
                        moves.append((x-i, y+i))
                elif self.get_piece_at_position((x-i, y+i)) is not None:
                    if self.get_piece_at_position((x-i, y+i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x-j, y+j)) is not None:
                                add = False
                        if add:
                            moves.append((x-i, y+i))
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
        # Down right
        if x + 2 < 8 and y + 1 < 8:
            if self.get_piece_at_position((x+2, y+1)) is None:
                moves.append((x+2, y+1))
            elif self.get_piece_at_position((x+2, y+1)).color is not self.color:
                moves.append((x+2, y+1))
        # Down left
        if x + 2 < 8 and y - 1 >= 0: 
            if self.get_piece_at_position((x+2, y-1)) is None:
                moves.append((x+2, y-1))
            elif self.get_piece_at_position((x+2, y-1)).color is not self.color:
                moves.append((x+2, y-1))
        # Up right
        if x - 2 >= 0 and y + 1 < 8:
            if self.get_piece_at_position((x-2, y+1)) is None:
                moves.append((x-2, y+1))
            elif self.get_piece_at_position((x-2, y+1)).color is not self.color:
                moves.append((x-2, y+1))
        # Up left
        if x - 2 >= 0 and y - 1 >= 0:
            if self.get_piece_at_position((x-2, y-1)) is None:
                moves.append((x-2, y-1))
            elif self.get_piece_at_position((x-2, y-1)).color is not self.color:
                moves.append((x-2, y-1))
        # Right down
        if x + 1 < 8 and y + 2 < 8:
            if self.get_piece_at_position((x+1, y+2)) is None:
                moves.append((x+1, y+2))
            elif self.get_piece_at_position((x+1, y+2)).color is not self.color:
                moves.append((x+1, y+2))
        # Right up
        if x + 1 < 8 and y - 2 >= 0:
            if self.get_piece_at_position((x+1, y-2)) is None:
                moves.append((x+1, y-2))
            elif self.get_piece_at_position((x+1, y-2)).color is not self.color:
                moves.append((x+1, y-2))
        # Left down
        if x - 1 >= 0 and y + 2 < 8:
            if self.get_piece_at_position((x-1, y+2)) is None:
                moves.append((x-1, y+2))
            elif self.get_piece_at_position((x-1, y+2)).color is not self.color:
                moves.append((x-1, y+2))
        # Left up
        if x - 1 >= 0 and y - 2 >= 0: 
            if self.get_piece_at_position((x-1, y-2)) is None:
                moves.append((x-1, y-2))
            elif self.get_piece_at_position((x-1, y-2)).color is not self.color:
                moves.append((x-1, y-2))
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
        for i in range(1, 8):
            # Right
            if x + i < 8: 
                if self.get_piece_at_position((x+i, y)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x+j, y)) is not None:
                            add = False
                    if add:
                        moves.append((x+i, y))
                else:
                    if self.get_piece_at_position((x+i, y)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x+j, y)) is not None:
                                add = False
                        if add:
                            moves.append((x+i, y))
            # Left
            if x - i >= 0:
                if self.get_piece_at_position((x-i, y)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x-j, y)) is not None:
                            add = False
                    if add:
                        moves.append((x-i, y))
                else:
                    if self.get_piece_at_position((x-i, y)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x-j, y)) is not None:
                                add = False
                        if add:
                            moves.append((x-i, y))
            # Down
            if y + i < 8:
                if self.get_piece_at_position((x, y+i)) is None: 
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x, y+j)) is not None:
                            add = False
                    if add:
                        moves.append((x, y+i))
                else:
                    if self.get_piece_at_position((x, y+i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x, y+j)) is not None:
                                add = False
                        if add:
                            moves.append((x, y+i))
            # Up
            if y - i >= 0:
                if self.get_piece_at_position((x, y-i)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x, y-j)) is not None:
                            add = False
                    if add:
                        moves.append((x, y-i))
                else:
                    if self.get_piece_at_position((x, y-i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x, y-j)) is not None:
                                add = False
                        if add:
                            moves.append((x, y-i))
            # Right down diagonal
            if x + i < 8 and y + i < 8:
                if self.get_piece_at_position((x+i, y+i)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x+j, y+j)) is not None:
                            add = False
                    if add:
                        moves.append((x+i, y+i))
                else:
                    if self.get_piece_at_position((x+i, y+i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x+j, y+j)) is not None:
                                add = False
                        if add:
                            moves.append((x+i, y+i))
            # Left up diagonal
            if x - i >= 0 and y - i >= 0:
                if self.get_piece_at_position((x-i, y-i)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x-j, y-j)) is not None:
                            add = False
                    if add: 
                        moves.append((x-i, y-i))
                else:
                    if self.get_piece_at_position((x-i, y-i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x-j, y-j)) is not None:
                                add = False
                        if add:
                            moves.append((x-i, y-i))
            # Right up diagonal
            if x + i < 8 and y - i >= 0:
                if self.get_piece_at_position((x+i, y-i)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x+j, y-j)) is not None:
                            add = False
                    if add:
                        moves.append((x+i, y-i))
                else:
                    if self.get_piece_at_position((x+i, y-i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x+j, y-j)) is not None:
                                add = False
                        if add:
                            moves.append((x+i, y-i))
            # Left down diagonal
            if x - i >= 0 and y + i < 8:
                if self.get_piece_at_position((x-i, y+i)) is None:
                    add = True
                    for j in range(1, i):
                        if self.get_piece_at_position((x-j, y+j)) is not None:
                            add = False
                    if add:
                        moves.append((x-i, y+i))
                else:
                    if self.get_piece_at_position((x-i, y+i)).color is not self.color:
                        add = True
                        for j in range(1, i):
                            if self.get_piece_at_position((x-j, y+j)) is not None:
                                add = False
                        if add:
                            moves.append((x-i, y+i))
        return moves
    
class King(ChessPiece):
    def __init__(self, color, position, get_piece_at_position):
        super().__init__(color, position)
        self.image = pygame.transform.scale(pygame.image.load(f"Icons/chess-king-solid{'-white' if color == 'white' else ''}.png"), (30, 40))
        self.get_piece_at_position = get_piece_at_position

    def draw(self, surface, image):
        super().draw(surface, self.image) 

    def get_moves(self):
        moves = []
        x, y = self.position
        # Right
        if x + 1 < 8:
            if self.get_piece_at_position((x+1, y)) is None or self.get_piece_at_position((x+1, y)).color is not self.color:
                moves.append((x+1, y))
        # Left
        if x - 1 >= 0:
            if self.get_piece_at_position((x-1, y)) is None or self.get_piece_at_position((x-1, y)).color is not self.color:
                moves.append((x-1, y))
        # Down
        if y + 1 < 8:
            if self.get_piece_at_position((x, y+1)) is None or self.get_piece_at_position((x, y+1)).color is not self.color:
                moves.append((x, y+1))
        # Up
        if y - 1 >= 0:
            if self.get_piece_at_position((x, y-1)) is None or self.get_piece_at_position((x, y-1)).color is not self.color:
                moves.append((x, y-1))
        # Right down diagonal
        if x + 1 < 8 and y + 1 < 8:
            if self.get_piece_at_position((x+1, y+1)) is None or self.get_piece_at_position((x+1, y+1)).color is not self.color:
                moves.append((x+1, y+1))
        # Left up diagonal
        if x - 1 >= 0 and y - 1 >= 0:
            if self.get_piece_at_position((x-1, y-1)) is None or self.get_piece_at_position((x-1, y-1)).color is not self.color:
                moves.append((x-1, y-1))
        # Right up diagonal
        if x + 1 < 8 and y - 1 >= 0:
            if self.get_piece_at_position((x+1, y-1)) is None or self.get_piece_at_position((x+1, y-1)).color is not self.color:
                moves.append((x+1, y-1))
        # Left down diagonal
        if x - 1 >= 0 and y + 1 < 8:
            if self.get_piece_at_position((x-1, y+1)) is None or self.get_piece_at_position((x-1, y+1)).color is not self.color:
                moves.append((x-1, y+1))
        return moves