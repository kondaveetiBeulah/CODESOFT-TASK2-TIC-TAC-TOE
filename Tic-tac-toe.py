import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board represented as a list
        self.current_winner = None  # keep track of winner

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2 etc (tells us what number corresponds to what box)
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        # returns a list of indexes of the empty spots
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        # if valid move, then make the move (assign square to letter)
        # then return true, if invalid, return false
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # winner if 3 in a row anywhere...we have to check all of these
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # left-right diagonal
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # right-left diagonal
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

def minimax(board, maximizing_player, depth, alpha, beta):
    if board.current_winner:
        if board.current_winner == 'O':  # AI is maximizing player
            return -1
        elif board.current_winner == 'X':  # human is minimizing player
            return 1
        else:
            return 0

    if not board.empty_squares():
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.available_moves():
            board.make_move(move, 'X')
            eval = minimax(board, False, depth + 1, alpha, beta)
            board.board[move] = ' '  # undo move
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.available_moves():
            board.make_move(move, 'O')
            eval = minimax(board, True, depth + 1, alpha, beta)
            board.board[move] = ' '  # undo move
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_computer_move(board):
    best_move = -1
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in board.available_moves():
        board.make_move(move, 'O')
        eval = minimax(board, True, 0, alpha, beta)
        board.board[move] = ' '  # undo move
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

def play_game():
    board = TicTacToe()
    print("Welcome to Tic-Tac-Toe!")
    print("Here is the board layout:")
    TicTacToe.print_board_nums()
    print("To make a move, enter the number corresponding to the position.")
    print("You (X) will play against the computer (O). Let's start!")
    board.print_board()

    while board.empty_squares():
        if board.current_winner:
            break
        human_move = None
        while human_move not in range(9):
            try:
                human_move = int(input("Enter your move (0-8): "))
                if human_move not in board.available_moves():
                    raise ValueError
            except ValueError:
                print("Invalid move. Try again.")
        board.make_move(human_move, 'X')
        board.print_board()

        if board.current_winner:
            break

        computer_move = get_computer_move(board)
        board.make_move(computer_move, 'O')
        board.print_board()

    if board.current_winner == 'X':
        print("Congratulations! You won!")
    elif board.current_winner == 'O':
        print("Sorry, you lost. The computer won.")
    else:
        print("It's a tie!")

if __name__ == '__main__':
    play_game()
