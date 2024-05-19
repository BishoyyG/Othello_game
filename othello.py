"""
 AUTHORS:
    Bishoy George        Bishoy.Geogre.eg@gmail.com
    Omar Ahmed Mohamed  
    Zaynab El Agamy     
    Farah Mohamad        
    Toka Abd El Ghafar  

"""


def play_game_console():
    # Function to play the game
    # Prompt user for difficulty level
    difficulty = input("Choose difficulty level (Easy, Medium, Hard): ").lower()

    # Set depth based on difficulty level
    if difficulty == 'easy':
        depth = 1
    elif difficulty == 'medium':
        depth = 3
    elif difficulty == 'hard':
        depth = 5
    else:
        # Handle invalid input by defaulting to Medium difficulty
        print("Invalid difficulty level. Defaulting to Medium.")
        depth = 3

    # Create a new game instance and start the game
    game = Othello()
    game.play_game(depth)


class Othello:
    def __init__(self):
        # Initialize the game board with empty spaces
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        # Set up the initial 4 pieces
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        # Set the starting player
        self.current_player = 'B'
        self.opponent = 'W'

    def print_board(self):
        # Print the game board to the console
        print("    0 1 2 3 4 5 6 7")
        print("    _ _ _ _ _ _ _ _")
        for i in range(8):
            print(i, '|', ' '.join(self.board[i]))

    def valid_move(self, row, col):
        # Check if the cell is empty
        if self.board[row][col] != ' ':
            return False

        # Check all 4 directions for a valid move
        for delta_r, delta_c in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + delta_r, col + delta_c
            # Move in the direction while the opponent's pieces are found
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.opponent:
                r, c = r + delta_r, c + delta_c
                # Check if the current player's piece is found after opponent's pieces
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    return True

        # No valid moves found
        return False

    def update_board(self, row, col):
        # Check if the move is valid
        if not self.valid_move(row, col):
            return False

        # Place the current player's piece on the board
        self.board[row][col] = self.current_player

        # Flip the opponent's pieces in all 4 directions
        for delta_r, delta_c in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + delta_r, col + delta_c
            to_flip = []
            # Collect opponent's pieces to flip
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.opponent:
                to_flip.append((r, c))
                r, c = r + delta_r, c + delta_c
                # Flip the pieces if the current player's piece is found after opponent's pieces
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    for r_flip, c_flip in to_flip:
                        self.board[r_flip][c_flip] = self.current_player
                    break

        # Switch the current player and opponent
        self.current_player, self.opponent = self.opponent, self.current_player
        return True

    def calculate_score(self):
        # Count the number of pieces for each player
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return {'B': black_count, 'W': white_count}

    def end_of_game(self):
        # Check if all disks are placed
        total_disks = sum(row.count('B') + row.count('W') for row in self.board)
        if total_disks >= 60:
            return True

        # Check each cell on the board for valid moves
        for i in range(8):
            for j in range(8):
                # If a valid move exists, the game is not over
                if self.valid_move(i, j):
                    return False
        # No valid moves found, the game is over
        return True


    def possible_moves(self):
        valid_moves = []  # Initialize list to store valid moves
        # Check each cell on the board
        for i in range(8):
            for j in range(8):
                # If the move is valid, add it to the list
                if self.valid_move(i, j):
                    valid_moves.append((i, j))
        # Return the list of valid moves
        return valid_moves

    def play_game(self, depth):
        # Loop until the game ends
        while not self.end_of_game():
            # Calculate and display the current scores
            scores = self.calculate_score()
            print("Black Score: ", scores['B'], "/ White Score: ", scores['W'])

            # Print the current board state
            self.print_board()
            print(f"Player {self.current_player}'s turn")

            # Get and display the possible moves
            valid_moves = self.possible_moves()
            print("Possible moves:", valid_moves)

            if self.current_player == 'B':
                # Human player (Black) makes a move
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))
                if self.update_board(row, col):
                    print("")
                else:
                    print("Invalid move, try again.")
            else:
                # AI player (White) makes a move using alpha-beta search
                _, best_move = self.alpha_beta_search(self.board, depth)
                self.update_board(best_move[0], best_move[1])

        # Game ended, print final board and scores
        self.print_board()
        scores = self.calculate_score()
        if scores['B'] > scores['W']:
            print("Black wins!")
        elif scores['B'] < scores['W']:
            print("White wins!")
        else:
            print("It's a tie!")

    def alpha_beta_search(self, board, depth):
        # Start alpha-beta search and return the best move
        _, move = self.alphabeta(board, float('-inf'), float('inf'), depth, True)
        return _, move

    def alphabeta(self, board, alpha, beta, depth, maximizing_player):
        # Terminal condition: depth limit reached or game over
        if depth == 0 or self.end_of_game():
            return self.Utility(board), None

        if maximizing_player:
            # Maximizing player's (AI) turn
            max_val = float('-inf')
            best_move = None
            for i in range(8):
                for j in range(8):
                    if self.valid_move(i, j):
                        # Copy board and simulate the move
                        new_board = [row[:] for row in board]
                        self.test_move_on_board(i, j, new_board)
                        # Recursively call alphabeta for the minimizing player
                        val, _ = self.alphabeta(new_board, alpha, beta, depth - 1, False)
                        if val > max_val:
                            max_val = val
                            best_move = (i, j)
                        alpha = max(alpha, val)
                        if beta <= alpha:
                            break
            return max_val, best_move
        else:
            # Minimizing player's (opponent) turn
            min_val = float('inf')
            best_move = None
            for i in range(8):
                for j in range(8):
                    if self.valid_move(i, j):
                        # Copy board and simulate the move
                        new_board = [row[:] for row in board]
                        self.test_move_on_board(i, j, new_board)
                        # Recursively call alphabeta for the maximizing player
                        val, _ = self.alphabeta(new_board, alpha, beta, depth - 1, True)
                        if val < min_val:
                            min_val = val
                            best_move = (i, j)
                        beta = min(beta, val)
                        if beta <= alpha:
                            break
            return min_val, best_move

    def Utility(self, board):
        # Calculate and return the utility value for the current player
        scores = self.calculate_score()
        return scores[self.current_player] - scores[self.opponent]

    def test_move_on_board(self, row, col, board):
        # Simulate a move on a given board state
        board[row][col] = self.current_player
        for delta_r, delta_c in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + delta_r, col + delta_c
            to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.opponent:
                to_flip.append((r, c))
                r, c = r + delta_r, c + delta_c
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.current_player:
                    for r_flip, c_flip in to_flip:
                        board[r_flip][c_flip] = self.current_player
                    break


if __name__ == "__main__":
    play_game_console()