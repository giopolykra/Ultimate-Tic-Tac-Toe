# main.py
import pygame
import sys
from game_logic import UltimateTicTacToe
from game_ui import UltimateTTTUI

class UltimateTTTGame:
    def __init__(self):
        self.game_logic = UltimateTicTacToe()
        self.ui = UltimateTTTUI()
        self.ai_enabled = False
        self.ai_player = None
    
    def run(self):
        """Main game loop"""
        running = True
        
        # Initial draw
        self.draw_complete_ui()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.VIDEORESIZE:
                    self.ui.handle_resize(event)
                    self.draw_complete_ui()
                
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_logic.game_over:
                    if not self.ai_enabled or self.game_logic.current_player == 'X':
                        self.handle_human_move(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_logic.reset()
                        self.draw_complete_ui()
                    elif event.key == pygame.K_a:
                        # Toggle AI (for testing)
                        self.toggle_ai()
            
            # If AI is enabled and it's AI's turn
            if (self.ai_enabled and not self.game_logic.game_over and 
                self.game_logic.current_player == 'O'):
                self.handle_ai_move()
            
            self.ui.update_display()
            
            # Small delay to prevent high CPU usage
            pygame.time.delay(10)
        
        pygame.quit()
        sys.exit()
    
    def draw_complete_ui(self):
        """Draw all UI elements"""
        self.ui.draw_board(self.game_logic)
        self.ui.draw_current_player_indicator(self.game_logic.current_player)
        self.ui.draw_move_restriction_info(self.game_logic.next_move)
        
        # If game is over, show message (on top of everything)
        if self.game_logic.game_over:
            self.ui.draw_game_over(self.game_logic.winner)

    def handle_human_move(self, mouse_pos):
        """Handle human player's move"""
        sub_board, cell = self.ui.get_clicked_cell(mouse_pos)
        
        # Make the move
        if self.game_logic.make_move(sub_board, cell):
            # Redraw complete UI
            self.draw_complete_ui()
            self.ui.update_display()
    
    def handle_ai_move(self):
        """Handle AI player's move"""
        # For now, use random move as placeholder
        # You'll replace this with your AI logic
        import random
        legal_moves = self.game_logic.get_legal_moves()
        
        if legal_moves:
            # Simple random AI for now
            sub_board, cell = random.choice(legal_moves)
            
            # Add a small delay so AI doesn't move instantly
            pygame.time.delay(500)
            
            # Make the move
            if self.game_logic.make_move(sub_board, cell):
                self.ui.draw_board(self.game_logic)
                
                if self.game_logic.game_over:
                    self.ui.draw_game_over(self.game_logic.winner)
                
                self.ui.update_display()
    
    def toggle_ai(self):
        """Toggle AI on/off"""
        self.ai_enabled = not self.ai_enabled
        print(f"AI enabled: {self.ai_enabled}")

if __name__ == "__main__":
    game = UltimateTTTGame()
    game.run()