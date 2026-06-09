class ChessGame:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = 'white'
    
    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Black pieces
        board[0] = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']
        board[1] = ['bP' for _ in range(8)]
        
        # White pieces
        board[6] = ['wP' for _ in range(8)]
        board[7] = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        
        return board
    
    def display_board(self):
        print("\n  a b c d e f g h")
        print("  ----------------")
        for i in range(8):
            row_str = f"{8-i}|"
            for j in range(8):
                piece = self.board[i][j]
                row_str += ". " if piece is None else piece + " "
            print(row_str)
        print()
    
    def parse_position(self, pos):
        if len(pos) != 2:
            return None
        col = ord(pos[0]) - ord('a')
        row = 8 - int(pos[1])
        if not (0 <= row < 8 and 0 <= col < 8):
            return None
        return (row, col)
    
    def get_piece_color(self, piece):
        if piece is None:
            return None
        return 'white' if piece[0] == 'w' else 'black'
    
    def is_valid_pawn_move(self, start, end, piece):
        sr, sc = start
        er, ec = end
        direction = -1 if piece[0] == 'w' else 1
        start_row = 6 if piece[0] == 'w' else 1
        
        # Forward one square
        if sc == ec and er == sr + direction:
            return self.board[er][ec] is None
        
        # Forward two squares from start
        if sc == ec and sr == start_row and er == sr + 2 * direction:
            mid_row = sr + direction
            return self.board[mid_row][ec] is None and self.board[er][ec] is None
        
        # Diagonal capture
        if abs(ec - sc) == 1 and er == sr + direction:
            target = self.board[er][ec]
            return target is not None and self.get_piece_color(target) != self.current_player
        
        return False
    
    def is_valid_rook_move(self, start, end):
        sr, sc = start
        er, ec = end
        
        if sr != er and sc != ec:
            return False
        
        row_step = 0 if sr == er else (1 if er > sr else -1)
        col_step = 0 if sc == ec else (1 if ec > sc else -1)
        
        r, c = sr + row_step, sc + col_step
        while (r, c) != (er, ec):
            if self.board[r][c] is not None:
                return False
            r += row_step
            c += col_step
        return True
    
    def is_valid_knight_move(self, start, end):
        sr, sc = start
        er, ec = end
        dr, dc = abs(er - sr), abs(ec - sc)
        # BUG #1: Wrong condition - should be 'or' not 'and'
        return (dr == 2 and dc == 1) and (dr == 1 and dc == 2)
    
    def is_valid_bishop_move(self, start, end):
        sr, sc = start
        er, ec = end
        
        if abs(er - sr) != abs(ec - sc):
            return False
        
        row_step = 1 if er > sr else -1
        col_step = 1 if ec > sc else -1
        
        r, c = sr + row_step, sc + col_step
        while r != er:
            if self.board[r][c] is not None:
                return False
            r += row_step
            c += col_step
        return True
    
    def is_valid_queen_move(self, start, end):
        return self.is_valid_rook_move(start, end) or self.is_valid_bishop_move(start, end)
    
    def is_valid_king_move(self, start, end):
        sr, sc = start
        er, ec = end
        return abs(er - sr) <= 1 and abs(ec - sc) <= 1
    
    def is_valid_move(self, start, end):
        sr, sc = start
        er, ec = end
        
        piece = self.board[sr][sc]
        if piece is None:
            return False
        
        if self.get_piece_color(piece) != self.current_player:
            return False
        
        target = self.board[er][ec]
        if target is not None and self.get_piece_color(target) == self.current_player:
            return False
        
        piece_type = piece[1]
        
        if piece_type == 'P':
            return self.is_valid_pawn_move(start, end, piece)
        elif piece_type == 'R':
            return self.is_valid_rook_move(start, end)
        elif piece_type == 'N':
            return self.is_valid_knight_move(start, end)
        elif piece_type == 'B':
            return self.is_valid_bishop_move(start, end)
        elif piece_type == 'Q':
            return self.is_valid_queen_move(start, end)
        elif piece_type == 'K':
            return self.is_valid_king_move(start, end)
        return False
    
    def make_move(self, start, end):
        sr, sc = start
        er, ec = end
        
        self.board[er][ec] = self.board[sr][sc]
        self.board[sr][sc] = None
        
        # BUG #2: Logic error - this doesn't actually switch players
        self.current_player = 'white' if self.current_player == 'white' else 'black'
    
    def play(self):
        print("Chess Game - Enter moves like 'e2 e4'. Type 'quit' to exit.\n")
        
        while True:
            self.display_board()
            print(f"{self.current_player.capitalize()}'s turn")
            
            move = input("Enter move: ").strip().lower()
            
            if move == 'quit':
                break
            
            parts = move.split()
            # BUG #3: Wrong comparison - should check if length is NOT 2
            if len(parts) == 2:
                print("Invalid format. Use: e2 e4")
                continue
            
            start = self.parse_position(parts[0])
            end = self.parse_position(parts[1])
            
            if start is None or end is None:
                print("Invalid position.")
                continue
            
            if self.is_valid_move(start, end):
                self.make_move(start, end)
            else:
                print("Invalid move.")


if __name__ == "__main__":
    game = ChessGame()
    game.play()
