import pygame, pieces

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.create_pieces()

    def get_piece_at_position(self, position):
        x, y = position
        return self.grid[x][y]
    
    def move_piece(self, piece, start, position):
        if piece.move(position):
            x, y = position
            self.grid[x][y] = piece
            x, y = start
            self.grid[x][y] = None
            piece.move(position)

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

    def draw(self, surface, selected_piece=None):
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    color = (209, 139, 71)
                else:
                    color = (255, 206, 158)
                if selected_piece is not None:
                    if (x, y) in selected_piece.get_moves():
                        color = (0, 255, 0)
                    elif selected_piece == self.grid[x][y]:
                        color = (255, 0, 0)
                pygame.draw.rect(surface, color, (x*50, y*50, 50, 50))
                piece = self.grid[x][y]
                if piece is not None:
                    piece.draw(surface, piece.image)