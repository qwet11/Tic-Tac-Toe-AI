from abc import abstractmethod
import random
from copy import deepcopy

class Game():
    X_PIECE = 'X'
    O_PIECE = 'O'
    EMPTY_PIECE = ' '

    def __init__(self):
        self.reset_board()
    
    # Print iterations progress (from StackOverflow)
    def printProgressBar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

    # Reset the tic-tac-toe board
    def reset_board(self) -> None: 
        self.board = self.create_board()

    # Return a new tic-tac-toe board
    def create_board(self) -> list:
        # Board will hold the values ('X', 'O', or ' ')
        board = []

        for _ in range(3):
            board.append([Game.EMPTY_PIECE, Game.EMPTY_PIECE, Game.EMPTY_PIECE])
        
        return board
    
    # Returns a string representation of the board
    def print_board(self) -> str:
        result = f"""
         {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]} 
        ---|---|---
         {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]} 
        ---|---|---
         {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]} 
        """
        
        return result
    
    # Updates board with move
    def make_move(self, piece, row, col) -> None:
        # Check if move is valid
        if(row > 2 or row < 0 or col > 2 or col < 0):
            raise Exception("Move out of range")
        elif(self.board[row][col] != Game.EMPTY_PIECE):
            raise Exception("Piece already in square")
        else:
            self.board[row][col] = piece

    # Return current board
    def get_board(self) -> list:
        return self.board

    # Returns true if the piece won
    def is_player_win(self, piece) -> bool: 
        for i in range(len(self.board)):
            # Check rows
            row_victory = (self.board[i][0] == piece) and (self.board[i][1] == piece) and (self.board[i][2] == piece)

            # Check columns
            col_victory = (self.board[0][i] == piece) and (self.board[1][i] == piece) and (self.board[2][i] == piece)

            if(row_victory or col_victory):
                return True

        # Check diagonals 
        forward_diag_victory = (self.board[0][0] == piece) and (self.board[1][1] == piece) and (self.board[2][2] == piece)
        backward_diag_victory = (self.board[2][0] == piece) and (self.board[1][1] == piece) and (self.board[0][2] == piece)

        if(forward_diag_victory or backward_diag_victory):
            return True  
        
        return False
    
    # Returns true if the piece won
    def general_is_player_win(board, piece) -> bool: 
        for i in range(len(board)):
            # Check rows
            row_victory = (board[i][0] == piece) and (board[i][1] == piece) and (board[i][2] == piece)

            # Check columns
            col_victory = (board[0][i] == piece) and (board[1][i] == piece) and (board[2][i] == piece)

            if(row_victory or col_victory):
                return True

        # Check diagonals 
        forward_diag_victory = (board[0][0] == piece) and (board[1][1] == piece) and (board[2][2] == piece)
        backward_diag_victory = (board[2][0] == piece) and (board[1][1] == piece) and (board[0][2] == piece)

        if(forward_diag_victory or backward_diag_victory):
            return True  
        
        return False
    
    def get_opponent_piece(piece) -> (X_PIECE or O_PIECE):
        if piece == Game.X_PIECE:
            return Game.O_PIECE
        elif piece == Game.O_PIECE:
            return Game.X_PIECE

    # Returns true if either player won or a tie
    def is_game_over(self) -> bool: 
        return self.is_player_win(Game.X_PIECE) or self.is_player_win(Game.O_PIECE) or self.is_tie()

    # Returns the player who won. Returns None if no player won 
    def get_win_player(self) -> (X_PIECE or O_PIECE or None):
        if self.is_player_win(Game.X_PIECE):
            return Game.X_PIECE
        elif self.is_player_win(Game.O_PIECE):
            return Game.O_PIECE
        else:
            return None
    
    # Returns true if move is legal. Return false otherwise
    def is_legal_move(self, piece, row, col) -> bool:
        return self.board[row][col] == Game.EMPTY_PIECE 

    # Returns true if move is legal. Returns false otherwise
    def general_is_legal_move(board, piece, row, col) -> bool:
        return board[row][col] == Game.EMPTY_PIECE

    # Returns true if game is tie. Returns false otherwise
    def is_tie(self) -> bool:
        for row in self.board:
            if Game.EMPTY_PIECE in row:
                return False
        
        return self.get_win_player() is None

    def general_is_tie(board) -> bool:
        for row in board:
            if Game.EMPTY_PIECE in row:
                return False
        
        return Game.general_is_player_win(board, Game.X_PIECE) is False and Game.general_is_player_win(board, Game.O_PIECE) is False

    # Plays tic-tac-toe with bots and return the bot index of who won (0 for bot_1, 1 for bot_2, -1 for tie)
    def play_game(self, bot_1, bot_2, save_game: bool = False) -> int:
        players = [bot_1, bot_2]
        curr_player_index = 0
        # print(self.print_board())

        if(save_game):
            game_moves = []

        while not self.is_game_over():
            curr_bot = players[curr_player_index]
            bot_move_row, bot_move_col = curr_bot.get_move(self.board)
            self.make_move(curr_bot.get_piece(), bot_move_row, bot_move_col)
            curr_player_index = (curr_player_index+1) % 2

            if(save_game):
                game_moves.append((curr_bot.get_piece(), bot_move_row, bot_move_col))
            # print(self.print_board())
        
        if(save_game):
            with open("game_moves.txt", "a") as f:
                f.write("\nGAME START\n")
                for move in game_moves:
                    f.write(str(move) + "\n")

        if self.is_tie():
            if(save_game):
                with open("game_moves.txt", "a") as f:
                    f.write("TIE\n")
                    f.write("\nGAME END\n")
            return -1
        elif self.get_win_player() == bot_1.get_piece():
            if(save_game):
                with open("game_moves.txt", "a") as f:
                    f.write("Bot 1 Won!\n")
                    f.write("\nGAME END\n")
            return 0
        else:
            if(save_game):
                with open("game_moves.txt", "a") as f:
                    f.write("Bot 2 Won!\n")
                    f.write("\nGAME END\n")
            return 1

    # Plays tic-tac-toe with bots and return the percentage of games won by each bot (in the format [bot_1_win_percentage, bot_2_win_percentage])
    def play_games(self, bot_1, bot_2, generations: int, save_game: bool = False) -> tuple:
        num_wins = [0, 0] # Index 0 for bot_1, index 1 for bot_1
        bot_1.set_piece(Game.X_PIECE)
        bot_2.set_piece(Game.O_PIECE)
        
        self.printProgressBar(0, generations, prefix = "Progress:", suffix = "Complete", length = 50)
        for i in range(generations):
            self.reset_board()
            win_index = self.play_game(bot_1, bot_2, save_game)
            bot_1.switch_piece()
            bot_2.switch_piece()
            if win_index != -1:
                num_wins[win_index] += 1

            # Update Progress Bar
            self.printProgressBar(i + 1, generations, prefix = 'Progress:', suffix = 'Complete', length = 50)
        
        return f"Win ratios: {[num_wins[0]/generations, num_wins[1]/generations]}"
        
class Bot():
    # All bots implemented in the game should extend this class 
    def __init__(self, *piece):
        if len(piece) == 0:
            self.piece = None
        else:
            self.piece = piece[0]

    def set_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece

    def switch_piece(self):
        if self.piece == Game.X_PIECE:
            self.piece = Game.O_PIECE
        else:
            self.piece = Game.X_PIECE

    @abstractmethod
    # Makes a legal move in the tic-tac-toe board
    def get_move(self, board):
        pass
    
class Random_Bot(Bot):
    def get_move(self, board):
        # Plays a random move
        while True:
            move_row = int(random.random() * 3)
            move_col = int(random.random() * 3)

            if Game.general_is_legal_move(board, self.piece, move_row, move_col):
                return [move_row, move_col]

class Look_Ahead_Bot(Bot):
    def get_move(self, board):
        # Plays a move that wins the game if possible
        for row in range(3):
            for col in range(3):
                if Game.general_is_legal_move(board, self.piece, row, col):
                    temp_board = deepcopy(board)
                    temp_board[row][col] = self.piece
                    if Game.general_is_player_win(temp_board, self.piece):
                        return [row, col]
                    else:
                        temp_board[row][col] = Game.EMPTY_PIECE
        
        # Plays a random move
        while True:
            move_row = int(random.random() * 3)
            move_col = int(random.random() * 3)

            if Game.general_is_legal_move(board, self.piece, move_row, move_col):
                return [move_row, move_col]

class Min_Max_Bot(Bot): 
    def __init__(self, max_depth, *piece):
        super().__init__(*piece)
        self.max_depth = max_depth

    def get_move(self, board):
        if(self.piece == None):
            raise Exception("Piece not set")

        # Plays a move that will result in the most wins
        temp_board = deepcopy(board)
        best_move_row = -1
        best_move_col = -1
        best_move_score = -99999999999999
        for row in range(3):
            for col in range(3):
                if Game.general_is_legal_move(board, self.piece, row, col):
                    score = self.min_max(temp_board, row, col, self.max_depth, 0)
                    if score > best_move_score:
                        best_move_row = row
                        best_move_col = col
                        best_move_score = score
        
        return [best_move_row, best_move_col]

    def min_max(self, board, input_row, input_col, max_depth, depth):
        # Returns the score of the board
        if depth % 2 == 0:
            curr_piece = self.piece
        else: 
            curr_piece = Game.get_opponent_piece(self.piece)

        temp_board = deepcopy(board)
        temp_board[input_row][input_col] = curr_piece

        if Game.general_is_player_win(temp_board, curr_piece):
            return 100 * (max_depth - depth) # Win score
        elif Game.general_is_tie(temp_board):
            return 0 # Tie score
        elif Game.general_is_player_win(temp_board, Game.get_opponent_piece(curr_piece)):
            return -100 * (max_depth - depth) # Lose score
        elif depth == max_depth:
            return 0
        else:
            best_score = None
            for row in range(3):
                for col in range(3):
                    if Game.general_is_legal_move(temp_board, curr_piece, row, col):
                        temp_temp_board = deepcopy(temp_board)
                        temp_temp_board[row][col] = curr_piece
                        score = self.min_max(temp_temp_board, row, col, max_depth, depth+1)
                        
                        if best_score == None:
                            best_score = score
                            continue

                        if(depth % 2 == 0):
                            best_score = -1 * max(best_score, score)
                        else:
                            best_score = -1 * max(best_score, score)
            return best_score

if __name__ == "__main__":
    game = Game()

    # print(game.play_games(Random_Bot(), Random_Bot(), 100000)) # Win Ratios: [0.58707, 0.28589]
    # print(game.play_games(Look_Ahead_Bot(), Random_Bot(), 100000)) # Win Ratios: [0.81319, 0.11996]
    # print(game.play_games(Min_Max_Bot(3), Random_Bot(), 100)) # Win ratios: [0.97, 0.02]
    print(game.play_games(Min_Max_Bot(5), Random_Bot(), 50, save_game = True)) # Win ratios: [0.92, 0.04]