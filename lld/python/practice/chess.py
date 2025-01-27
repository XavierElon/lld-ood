from abc import ABC, abstractmethod
from enum import Enum

# Strategy Pattern:
# Implemented through the polymorphic can_move() methods in piece subclasses
# Allows different movement behaviors to be encapsulated in different classes
# Makes it easy to add new piece types without modifying existing code

# State Pattern:
# The Board class maintains the game state
# Pieces track their own positions and colors
# Game rules are enforced through board state validation

# Command Pattern:
# The Move class encapsulates a move request
# Allows parameterizing requests with different moves
# Makes it easy to extend with undo/redo functionality

# Template Method Pattern:
# The abstract Piece class defines the interface (can_move())
# Concrete subclasses implement the specific movement logic
# Ensures consistent interface across all piece types

# Observer Pattern (Potential):
# The game loop could be extended to notify observers of game state changes
# Currently implemented through direct method calls, but structure allows expansion

class Color(Enum):
    WHITE = 1
    BLACK = 2

class Piece(ABC):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

    @abstractmethod
    def can_move(self, board, dest_row, dest_col):
        pass

class Pawn(Piece):
    def can_move(self, board, dest_row, dest_col):
        row_diff = dest_row - self.row
        col_diff = abs(dest_col - self.col)
        if self.color == Color.WHITE:
            return (row_diff == 1 and col_diff == 0) or \
                   (self.row == 1 and row_diff == 2 and col_diff == 0) or \
                   (row_diff == 1 and col_diff == 1 and board.get_piece(dest_row, dest_col))
        else:
            return (row_diff == -1 and col_diff == 0) or \
                   (self.row == 6 and row_diff == -2 and col_diff == 0) or \
                   (row_diff == -1 and col_diff == 1 and board.get_piece(dest_row, dest_col))

class Rook(Piece):
    def can_move(self, board, dest_row, dest_col):
        return self.row == dest_row or self.col == dest_col

class Knight(Piece):
    def can_move(self, board, dest_row, dest_col):
        row_diff = abs(dest_row - self.row)
        col_diff = abs(dest_col - self.col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

class Bishop(Piece):
    def can_move(self, board, dest_row, dest_col):
        return abs(dest_row - self.row) == abs(dest_col - self.col)

class Queen(Piece):
    def can_move(self, board, dest_row, dest_col):
        return (self.row == dest_row or self.col == dest_col) or \
               (abs(dest_row - self.row) == abs(dest_col - self.col))

class King(Piece):
    def can_move(self, board, dest_row, dest_col):
        return abs(dest_row - self.row) <= 1 and abs(dest_col - self.col) <= 1

class Move:
    def __init__(self, piece, dest_row, dest_col):
        self.piece = piece
        self.dest_row = dest_row
        self.dest_col = dest_col

class Player:
    def __init__(self, color):
        self.color = color

    def make_move(self, board, move):
        piece = move.piece
        dest_row, dest_col = move.dest_row, move.dest_col
        
        if board.is_valid_move(piece, dest_row, dest_col):
            board.set_piece(piece.row, piece.col, None)
            board.set_piece(dest_row, dest_col, piece)
            piece.row, piece.col = dest_row, dest_col
        else:
            raise ValueError("Invalid move!")

class Board:
    def __init__(self):
        self.board = [[None]*8 for _ in range(8)]
        self._initialize_board()

    def _initialize_board(self):
        # Initialize white pieces
        self.board[0] = [
            Rook(Color.WHITE, 0, 0), Knight(Color.WHITE, 0, 1),
            Bishop(Color.WHITE, 0, 2), Queen(Color.WHITE, 0, 3),
            King(Color.WHITE, 0, 4), Bishop(Color.WHITE, 0, 5),
            Knight(Color.WHITE, 0, 6), Rook(Color.WHITE, 0, 7)
        ]
        self.board[1] = [Pawn(Color.WHITE, 1, i) for i in range(8)]
        
        # Initialize black pieces
        self.board[7] = [
            Rook(Color.BLACK, 7, 0), Knight(Color.BLACK, 7, 1),
            Bishop(Color.BLACK, 7, 2), Queen(Color.BLACK, 7, 3),
            King(Color.BLACK, 7, 4), Bishop(Color.BLACK, 7, 5),
            Knight(Color.BLACK, 7, 6), Rook(Color.BLACK, 7, 7)
        ]
        self.board[6] = [Pawn(Color.BLACK, 6, i) for i in range(8)]

    def get_piece(self, row, col):
        return self.board[row][col]

    def set_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_move(self, piece, dest_row, dest_col):
        if not (0 <= dest_row < 8 and 0 <= dest_col < 8):
            return False
        target = self.get_piece(dest_row, dest_col)
        return (target is None or target.color != piece.color) and \
               piece.can_move(self, dest_row, dest_col)

    def is_checkmate(self, color):
        # TODO: Implement checkmate logic
        return False

    def is_stalemate(self, color):
        # TODO: Implement stalemate logic
        return False

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(Color.WHITE), Player(Color.BLACK)]
        self.current_player = 0

    def start(self):
        while not self._is_game_over():
            current = self.players[self.current_player]
            print(f"{current.color.name}'s turn")
            
            try:
                move = self._get_move(current)
                current.make_move(self.board, move)
                self.current_player = 1 - self.current_player
            except Exception as e:
                print(f"Error: {e}")

        self._display_result()

    def _get_move(self, player):
        src_row = int(input("Enter source row: "))
        src_col = int(input("Enter source column: "))
        dest_row = int(input("Enter destination row: "))
        dest_col = int(input("Enter destination column: "))
        
        piece = self.board.get_piece(src_row, src_col)
        if not piece or piece.color != player.color:
            raise ValueError("Invalid piece selection")
            
        return Move(piece, dest_row, dest_col)

    def _is_game_over(self):
        return self.board.is_checkmate(Color.WHITE) or \
               self.board.is_checkmate(Color.BLACK) or \
               self.board.is_stalemate(Color.WHITE) or \
               self.board.is_stalemate(Color.BLACK)

    def _display_result(self):
        if self.board.is_checkmate(Color.WHITE):
            print("Black wins by checkmate!")
        elif self.board.is_checkmate(Color.BLACK):
            print("White wins by checkmate!")
        else:
            print("Game ends in stalemate!")

if __name__ == "__main__":
    Game().start()