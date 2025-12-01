# game_logic.py
class UltimateTicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(9)] for _ in range(9)]
        self.main_board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.next_move = None
        self.game_over = False
        self.winner = None
    
    def get_legal_moves(self):
        """Get all legal moves for the current state"""
        legal_moves = []
        
        if self.next_move is None:
            # Can play on any sub-board that's not won
            sub_boards = [i for i in range(9) if self.main_board[i] == ' ']
        else:
            sub_boards = [self.next_move] if self.main_board[self.next_move] == ' ' else []
        
        for sub in sub_boards:
            for cell in range(9):
                if self.board[sub][cell] == ' ':
                    legal_moves.append((sub, cell))
        
        return legal_moves
    
    def make_move(self, sub_board, cell):
        """Make a move and update game state"""
        if self.game_over:
            return False
        
        # Validate move
        if not self.is_valid_move(sub_board, cell):
            return False
        
        # Make the move
        self.board[sub_board][cell] = self.current_player
        
        # Check if this move wins the sub-board
        sub_winner = self.check_sub_board_winner(sub_board)
        if sub_winner:
            self.main_board[sub_board] = sub_winner
            self.board[sub_board] = [sub_winner] * 9
        
        # Check if game is over
        self.check_game_over()
        
        # Update next move
        if not self.game_over:
            self.next_move = cell if self.main_board[cell] == ' ' else None
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return True
    
    def is_valid_move(self, sub_board, cell):
        """Check if a move is valid"""
        if self.next_move is not None and self.next_move != sub_board:
            return False
        
        if self.main_board[sub_board] != ' ':
            return False
        
        if self.board[sub_board][cell] != ' ':
            return False
        
        return True
    
    def check_sub_board_winner(self, sub_board_index):
        """Check if a sub-board has a winner"""
        sub_board = self.board[sub_board_index]
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        
        for combo in winning_combinations:
            a, b, c = combo
            if sub_board[a] != ' ' and sub_board[a] == sub_board[b] == sub_board[c]:
                return sub_board[a]
        
        # Check if sub-board is full (draw)
        if all(cell != ' ' for cell in sub_board):
            return 'D'  # Draw
        
        return None
    
    def check_game_over(self):
        """Check if the main game is over"""
        # Check for winner
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combo in winning_combinations:
            a, b, c = combo
            if self.main_board[a] != ' ' and self.main_board[a] == self.main_board[b] == self.main_board[c]:
                self.game_over = True
                self.winner = self.main_board[a]
                return
        
        # Check if main board is full
        if all(cell != ' ' for cell in self.main_board):
            self.game_over = True
            self.winner = None  # Draw
            return
    
    def reset(self):
        """Reset the game to initial state"""
        self.board = [[' ' for _ in range(9)] for _ in range(9)]
        self.main_board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.next_move = None
        self.game_over = False
        self.winner = None
    
    def get_game_state(self):
        """Return a copy of the current game state"""
        return {
            'board': [row[:] for row in self.board],
            'main_board': self.main_board[:],
            'current_player': self.current_player,
            'next_move': self.next_move,
            'game_over': self.game_over,
            'winner': self.winner
        }