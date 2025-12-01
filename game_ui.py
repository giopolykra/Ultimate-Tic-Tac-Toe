# game_ui.py
import pygame
import sys

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 230, 255, 100)  # Light blue with transparency

# Drawing constants
LINE_WIDTH = 5
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

class UltimateTTTUI:
    def __init__(self, width=600, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption('Ultimate Tic-Tac-Toe')
        self.font = pygame.font.Font(None, 40)
        self.width = width
        self.height = height
        
    def draw_board(self, game_logic):
        """Draw the complete game board"""
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_highlight(game_logic.next_move)
        self.draw_figures(game_logic)
        
    def draw_grid(self):
        """Draw the grid lines"""
        width, height = self.screen.get_size()
        
        # Draw main grid lines (3x3)
        for i in range(1, 3):
            # Vertical lines
            pygame.draw.line(self.screen, BLACK, 
                           (i * width // 3, 0), 
                           (i * width // 3, height), 
                           LINE_WIDTH)
            # Horizontal lines
            pygame.draw.line(self.screen, BLACK, 
                           (0, i * height // 3), 
                           (width, i * height // 3), 
                           LINE_WIDTH)
        
        # Draw sub-grid lines (9x9)
        square_size = width // 9
        for i in range(1, 9):
            if i % 3 != 0:  # Skip where main lines already are
                # Vertical lines
                pygame.draw.line(self.screen, BLACK, 
                               (i * square_size, 0), 
                               (i * square_size, height), 2)
                # Horizontal lines
                pygame.draw.line(self.screen, BLACK, 
                               (0, i * square_size), 
                               (width, i * square_size), 2)
    
    def draw_highlight(self, next_move):
        """Draw a semi-transparent highlight over the permissible sub-board"""
        if next_move is None:
            return  # No restriction - highlight all valid boards
        
        width, height = self.screen.get_size()
        square_size = width // 9
        
        # Calculate which 3x3 sub-board to highlight
        sub_board = next_move
        row = sub_board // 3
        col = sub_board % 3
        
        # Create a semi-transparent surface for the highlight
        highlight_surface = pygame.Surface((square_size * 3, square_size * 3), pygame.SRCALPHA)
        
        # Draw the haze effect (multiple options - choose one):
        
        # Option 1: Simple translucent rectangle
        highlight_surface.fill(HIGHLIGHT_COLOR)
        
        # Option 2: Gradient effect (more visually appealing)
        # for i in range(3):
        #     for j in range(3):
        #         alpha = 50 + 20 * ((i + j) % 3)
        #         cell_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        #         cell_surface.fill((200, 230, 255, alpha))
        #         highlight_surface.blit(cell_surface, (j * square_size, i * square_size))
        
        # Option 3: Border highlight only
        # pygame.draw.rect(highlight_surface, HIGHLIGHT_COLOR, 
        #                 (0, 0, square_size * 3, square_size * 3), 3)
        
        # Position the highlight
        x_pos = col * (square_size * 3)
        y_pos = row * (square_size * 3)
        
        # Draw highlight
        self.screen.blit(highlight_surface, (x_pos, y_pos))
        
        # Optional: Draw a border around the highlighted area
        border_color = (100, 150, 255)  # Darker blue for border
        pygame.draw.rect(self.screen, border_color, 
                        (x_pos, y_pos, square_size * 3, square_size * 3), 3)
        
        # Optional: Add text indicator
        if width > 400:  # Only show text if window is large enough
            font = pygame.font.Font(None, 30)
            text = font.render(f"Play here", True, border_color)
            text_rect = text.get_rect(center=(x_pos + square_size * 1.5, y_pos - 20))
            self.screen.blit(text, text_rect)
    
    def draw_figures(self, game_logic):
        """Draw Xs and Os on the board"""
        width, height = self.screen.get_size()
        square_size = width // 9
        circle_radius = square_size // 3
        space = square_size // 4
        
        # Draw regular Xs and Os
        for sub_board in range(9):
            for cell in range(9):
                row = (sub_board // 3) * 3 + (cell // 3)
                col = (sub_board % 3) * 3 + (cell % 3)
                
                # If sub-board is won, draw giant figure
                if game_logic.main_board[sub_board] != ' ':
                    if game_logic.main_board[sub_board] == 'X':
                        self.draw_giant_x(row, col, square_size, space)
                    elif game_logic.main_board[sub_board] == 'O':
                        self.draw_giant_o(row, col, square_size, circle_radius)
                # Draw regular figures
                elif game_logic.board[sub_board][cell] == 'X':
                    self.draw_x(row, col, square_size, space)
                elif game_logic.board[sub_board][cell] == 'O':
                    self.draw_o(row, col, square_size, circle_radius)
    
    def draw_x(self, row, col, square_size, space):
        """Draw a regular X"""
        start_desc = (col * square_size + space, row * square_size + space)
        end_desc = (col * square_size + square_size - space, row * square_size + square_size - space)
        pygame.draw.line(self.screen, RED, start_desc, end_desc, CROSS_WIDTH)
        
        start_asc = (col * square_size + space, row * square_size + square_size - space)
        end_asc = (col * square_size + square_size - space, row * square_size + space)
        pygame.draw.line(self.screen, RED, start_asc, end_asc, CROSS_WIDTH)
    
    def draw_o(self, row, col, square_size, circle_radius):
        """Draw a regular O"""
        center = (col * square_size + square_size // 2, row * square_size + square_size // 2)
        pygame.draw.circle(self.screen, BLUE, center, circle_radius, CIRCLE_WIDTH)
    
    def draw_giant_x(self, row, col, square_size, space):
        """Draw a giant X covering a sub-board"""
        start_col = (col // 3) * 3 * square_size
        start_row = (row // 3) * 3 * square_size
        
        start_desc = (start_col + space, start_row + space)
        end_desc = (start_col + 3 * square_size - space, start_row + 3 * square_size - space)
        pygame.draw.line(self.screen, RED, start_desc, end_desc, CROSS_WIDTH)
        
        start_asc = (start_col + space, start_row + 3 * square_size - space)
        end_asc = (start_col + 3 * square_size - space, start_row + space)
        pygame.draw.line(self.screen, RED, start_asc, end_asc, CROSS_WIDTH)
    
    def draw_giant_o(self, row, col, square_size, circle_radius):
        """Draw a giant O covering a sub-board"""
        start_col = (col // 3) * 3 * square_size
        start_row = (row // 3) * 3 * square_size
        center_col = start_col + (3 * square_size) // 2
        center_row = start_row + (3 * square_size) // 2
        giant_radius = 3 * square_size // 2 - (square_size // 4)
        pygame.draw.circle(self.screen, BLUE, (center_col, center_row), giant_radius, CIRCLE_WIDTH)
    
    def draw_game_over(self, winner):
        """Draw game over message"""
        width, height = self.screen.get_size()
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        if winner:
            text = f"Player {winner} wins!"
            color = RED if winner == 'X' else BLUE
        else:
            text = "Game is a draw!"
            color = BLACK
        
        font = pygame.font.Font(None, 74)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(width//2, height//2))
        self.screen.blit(text_surf, text_rect)
        
        # Draw restart instruction
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(width//2, height//2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_current_player_indicator(self, current_player):
        """Draw indicator showing whose turn it is"""
        width, height = self.screen.get_size()
        
        if current_player == 'X':
            color = RED
            symbol = "X"
        else:
            color = BLUE
            symbol = "O"
        
        # Draw indicator in top-left corner
        font = pygame.font.Font(None, 36)
        text = font.render(f"Current: {symbol}", True, color)
        self.screen.blit(text, (10, 10))
        
        # Optional: Draw a small preview of the symbol
        preview_size = 30
        if current_player == 'X':
            pygame.draw.line(self.screen, color, (15, 45), (15 + preview_size, 45 + preview_size), 3)
            pygame.draw.line(self.screen, color, (15, 45 + preview_size), (15 + preview_size, 45), 3)
        else:
            pygame.draw.circle(self.screen, color, (15 + preview_size//2, 45 + preview_size//2), 
                             preview_size//2, 2)
    
    def draw_move_restriction_info(self, next_move):
        """Draw information about move restrictions"""
        width, height = self.screen.get_size()
        
        font = pygame.font.Font(None, 28)
        
        if next_move is None:
            text = "You can play in any available sub-board"
            color = (0, 150, 0)  # Green
        else:
            text = f"You must play in sub-board {next_move + 1}"
            color = (200, 100, 0)  # Orange
        
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(width//2, height - 20))
        self.screen.blit(text_surf, text_rect)
    
    def get_clicked_cell(self, pos):
        """Convert mouse position to board coordinates"""
        width, height = self.screen.get_size()
        square_size = width // 9
        
        x, y = pos
        clicked_row = y // square_size
        clicked_col = x // square_size
        
        sub_board = (clicked_row // 3) * 3 + (clicked_col // 3)
        cell = (clicked_row % 3) * 3 + (clicked_col % 3)
        
        return sub_board, cell
    
    def update_display(self):
        """Update the display"""
        pygame.display.update()
    
    def handle_resize(self, event):
        """Handle window resize"""
        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)