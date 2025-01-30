# Design Patterns Used
# Singleton Pattern (GameManager)

# The GameManager class uses a class-level _instance attribute and a @staticmethod get_instance() method.
# The double-checked locking approach with threading.Lock ensures that only one instance of GameManager is created even in a multi-threaded environment.
# Encapsulation and Cohesion

# Classes like Board, Snake, Ladder, Dice, Player, and SnakeAndLadderGame each handle a specific aspect of the game.
# This adheres to good object-oriented design principles: each class is responsible for a cohesive set of behaviors.
# (Optional) Threading / Concurrency

# The GameManager launches each game in its own thread. While not strictly a "design pattern," it demonstrates concurrent design where multiple games can run in parallel.

import random
import threading

class Snake:
    """
    Represents a snake on the board with a start and end position.
    If a player lands on 'start', they go down to 'end'.
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end


class Ladder:
    """
    Represents a ladder on the board with a start and end position.
    If a player lands on 'start', they climb up to 'end'.
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end


class Board:
    """
    Represents the game board. By default, it is size 100.
    It contains lists of snakes and ladders, and a helper method to
    get the new position if the player lands on a snake or a ladder.
    """
    BOARD_SIZE = 100

    def __init__(self):
        self.snakes = []
        self.ladders = []
        self._initialize_snakes_and_ladders()

    def _initialize_snakes_and_ladders(self):
        # Initialize snakes
        self.snakes.append(Snake(16, 6))
        self.snakes.append(Snake(48, 26))
        self.snakes.append(Snake(64, 60))
        self.snakes.append(Snake(93, 73))

        # Initialize ladders
        self.ladders.append(Ladder(1, 38))
        self.ladders.append(Ladder(4, 14))
        self.ladders.append(Ladder(9, 31))
        self.ladders.append(Ladder(21, 42))
        self.ladders.append(Ladder(28, 84))
        self.ladders.append(Ladder(51, 67))
        self.ladders.append(Ladder(80, 99))

    def get_board_size(self):
        return Board.BOARD_SIZE

    def get_new_position_after_snake_or_ladder(self, position):
        """
        If 'position' matches the start of any snake or ladder,
        return the end of that snake/ladder. Otherwise return the original position.
        """
        for snake in self.snakes:
            if snake.get_start() == position:
                return snake.get_end()

        for ladder in self.ladders:
            if ladder.get_start() == position:
                return ladder.get_end()

        return position


class Dice:
    """
    Represents a dice which returns a random value between MIN_VALUE and MAX_VALUE.
    """
    MIN_VALUE = 1
    MAX_VALUE = 6

    def roll(self):
        return random.randint(Dice.MIN_VALUE, Dice.MAX_VALUE)


class Player:
    """
    Represents a player with a name and current position on the board.
    """
    def __init__(self, name):
        self.name = name
        self.position = 0

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position


class SnakeAndLadderGame:
    """
    Represents a single instance of the Snake and Ladder game.
    """
    def __init__(self, player_names):
        self.board = Board()
        self.dice = Dice()
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0

    def play(self):
        """
        Continuously take turns until one player reaches the final cell.
        """
        while not self._is_game_over():
            current_player = self.players[self.current_player_index]
            dice_roll = self.dice.roll()
            new_position = current_player.get_position() + dice_roll

            if new_position <= self.board.get_board_size():
                new_position = self.board.get_new_position_after_snake_or_ladder(new_position)
                current_player.set_position(new_position)
                print(f"{current_player.get_name()} rolled a {dice_roll} "
                      f"and moved to position {current_player.get_position()}")

            # Check if the player has won
            if current_player.get_position() == self.board.get_board_size():
                print(f"{current_player.get_name()} wins!")
                break

            # Next player's turn
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def _is_game_over(self):
        """
        Check if any player has reached the end of the board.
        """
        for player in self.players:
            if player.get_position() == self.board.get_board_size():
                return True
        return False


class GameManager:
    """
    Manages multiple Snake and Ladder games.
    Demonstrates the Singleton pattern using a class-level _instance.
    """
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.games = []

    @staticmethod
    def get_instance():
        """
        Double-checked locking Singleton pattern to ensure only one instance
        of GameManager is created, even in a multi-threaded environment.
        """
        if not GameManager._instance:
            with GameManager._lock:
                if not GameManager._instance:
                    GameManager._instance = GameManager()
        return GameManager._instance

    def start_new_game(self, player_names):
        """
        Starts a new Snake and Ladder game in a separate thread.
        """
        game = SnakeAndLadderGame(player_names)
        self.games.append(game)
        threading.Thread(target=game.play).start()


class SnakeAndLadderDemo:
    """
    Demo class that starts multiple games using the GameManager.
    """
    @staticmethod
    def run():
        game_manager = GameManager.get_instance()

        # Start game 1
        players1 = ["Player 1", "Player 2", "Player 3"]
        game_manager.start_new_game(players1)

        # Start game 2
        players2 = ["Player 4", "Player 5"]
        game_manager.start_new_game(players2)


if __name__ == "__main__":
    SnakeAndLadderDemo.run()
