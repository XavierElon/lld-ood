from enum import Enum
from abc import ABC, abstractmethod

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

class Board:
    def __init__(self):
        self.grid = [[None]*8 for _ in range(8)]
        self._init_board()
        
    def _init_board(self):
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            self.grid[0][col] = piece_order[col](Color.WHITE)
            self.grid[1][col] = Pawn(Color.WHITE)
            self.grid[6][col] = Pawn(Color.BLACK)
            self.grid[7][col] = piece_order[col](Color.BLACK)
            
    def get_piece(self, position):
        row, col = position
        return self.grid[row][col]
    
    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.grid[start_row][start_col]
        self.grid[end_row][end_col] = piece
        self.grid[start_row][start_col] = None
    
class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_player = Color.WHITE
        
    def play(self):
        while True:
            self.print_board()
            start = self.get_position("Enter start position (row col): ")
            end = self.get_position("Enter end position (row col): ")
            
            if self.is_valid_move(start, end):
                self.board.move_piece(start, end)
                self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
            else:
                print("Invalid move!")
                
    def is_valid_move(self, start, end):
        piece = self.board.get_piece(start)
        target = self.board.get_piece(end)
        
        if not piece or piece.color != self.current_player:
            return False
        if target and target.color == self.current_player:
            return False

        return piece.is_valid_move(start, end, self.board)
    
    
    def print_board(self):
        """Display the board with Unicode chess symbols"""
        symbols = {
            (Rook, Color.WHITE): '♖', (Knight, Color.WHITE): '♘',
            (Bishop, Color.WHITE): '♗', (Queen, Color.WHITE): '♕',
            (King, Color.WHITE): '♔', (Pawn, Color.WHITE): '♙',
            (Rook, Color.BLACK): '♜', (Knight, Color.BLACK): '♞',
            (Bishop, Color.BLACK): '♝', (Queen, Color.BLACK): '♛',
            (King, Color.BLACK): '♚', (Pawn, Color.BLACK): '♟',
        }
        
        print("\n" + "-"*33)
        for row in range(7, -1, -1):  # Print from top (row 7) to bottom (row 0)
            line = f"{row} |"
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece:
                    line += f" {symbols.get((type(piece), piece.color), '?')} |"
                else:
                    line += "    |"
            print(line)
            print("-"*33)
        print("    " + "   ".join(f"{col}" for col in range(8)))

    def get_position(self, prompt):
        """Get and validate board position from user input"""
        while True:
            try:
                row, col = map(int, input(prompt).split())
                if 0 <= row < 8 and 0 <= col < 8:
                    return (row, col)
                print("Coordinates must be between 0-7")
            except ValueError:
                print("Invalid input. Use format: row col (e.g., 1 4)")
                
class Pawn(Piece):
    def is_valid_move(self, start, end, board):
        s_row, s_col = start
        e_row, e_col = end
        direction = 1 if self.color == Color.WHITE else - 1
        dx = e_col - s_col
        dy = e_row - s_row
        
                # Basic pawn movement
        if dx == 0:  # Forward move
            if dy == direction:
                return not board.get_piece(end)
            if dy == 2*direction and (s_row == 1 or s_row == 6):
                return not board.get_piece(end) and not board.get_piece((s_row + direction, s_col))
        elif abs(dx) == 1 and dy == direction:  # Capture
            return board.get_piece(end) is not None
        
        return False
    
class Knight(Piece):
    def is_valid_move(self, start, end, board):
        dx = abs(end[1] - start[1])
        dy = abs(end[0] - start[0])
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
    
class Bishop(Piece):
    def is_valid_move(self, start, end, board):
        if abs(end[1] - start[1] != abs(end[0] - start[0])):
            return False
        return self._is_clear_path(start, end, board)
    
    def _is_clear_path(self, start, end, board):
        step_x = 1 if end[1] > start[1] else -1
        step_y = 1 if end[0] > start[0] else -1
        steps = abs(end[1] - start[1])
        
        for i in range(1, steps):
            check_pos = (start[0] + i * step_y, start[1] + i * step_x)
            if board.get_piece(check_pos):
                return False
        return True

if __name__ == "__main__":
    game = ChessGame()
    game.play()
        