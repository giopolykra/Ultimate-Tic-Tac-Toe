import pygame
import sys

# Initialize pygame
pygame.init()

# Set up initial display
INITIAL_WIDTH, INITIAL_HEIGHT = 600, 600
LINE_WIDTH = 5
SQUARE_SIZE = INITIAL_WIDTH // 9  # Will be recalculated based on the current window size
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen and fonts
screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Ultimate Tic-Tac-Toe')
screen.fill(WHITE)
font = pygame.font.Font(None, 40)

# Game variables
board = [[' ' for _ in range(9)] for _ in range(9)]
main_board = [' ' for _ in range(9)]
current_player = 'X'
next_move = None
game_over = False


def draw_lines():
    screen.fill(WHITE)
    # Calculate sizes based on current window size
    width, height = screen.get_size()
    square_size = width // 9
    
    # Draw the main grid lines
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * width // 3, 0), (i * width // 3, height), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, i * height // 3), (width, i * height // 3), LINE_WIDTH)
    
    # Draw the sub-grid lines
    for i in range(1, 9):
        if i % 3 != 0:  # Skip the main grid lines
            pygame.draw.line(screen, BLACK, (i * square_size, 0), (i * square_size, height), 2)
            pygame.draw.line(screen, BLACK, (0, i * square_size), (width, i * square_size), 2)


def draw_figures():
    width, height = screen.get_size()
    square_size = width // 9
    circle_radius = square_size // 3
    space = square_size // 4

    for row in range(9):
        for col in range(9):
            sub_board_index = (row // 3) * 3 + (col // 3)
            cell_index = (row % 3) * 3 + (col % 3)
            if main_board[sub_board_index] == 'X':
                draw_giant_x(row, col, square_size, space)
            elif main_board[sub_board_index] == 'O':
                draw_giant_o(row, col, square_size, circle_radius)
            elif board[sub_board_index][cell_index] == 'X':
                draw_x(row, col, square_size, space)
            elif board[sub_board_index][cell_index] == 'O':
                draw_o(row, col, square_size, circle_radius)


def draw_x(row, col, square_size, space):
    start_desc = (col * square_size + space, row * square_size + space)
    end_desc = (col * square_size + square_size - space, row * square_size + square_size - space)
    pygame.draw.line(screen, RED, start_desc, end_desc, CROSS_WIDTH)
    start_asc = (col * square_size + space, row * square_size + square_size - space)
    end_asc = (col * square_size + square_size - space, row * square_size + space)
    pygame.draw.line(screen, RED, start_asc, end_asc, CROSS_WIDTH)


def draw_o(row, col, square_size, circle_radius):
    center = (col * square_size + square_size // 2, row * square_size + square_size // 2)
    pygame.draw.circle(screen, BLUE, center, circle_radius, CIRCLE_WIDTH)


def draw_giant_x(row, col, square_size, space):
    # Calculate top-left of the sub-board
    start_col = (col // 3) * 3 * square_size
    start_row = (row // 3) * 3 * square_size

    start_desc = (start_col + space, start_row + space)
    end_desc = (start_col + 3 * square_size - space, start_row + 3 * square_size - space)
    pygame.draw.line(screen, RED, start_desc, end_desc, CROSS_WIDTH)

    start_asc = (start_col + space, start_row + 3 * square_size - space)
    end_asc = (start_col + 3 * square_size - space, start_row + space)
    pygame.draw.line(screen, RED, start_asc, end_asc, CROSS_WIDTH)


def draw_giant_o(row, col, square_size, circle_radius):
    # Calculate center of the sub-board
    center_col = (col // 3) * 3 * square_size + (3 * square_size) // 2
    center_row = (row // 3) * 3 * square_size + (3 * square_size) // 2
    giant_radius = 3 * square_size // 2 - SPACE
    pygame.draw.circle(screen, BLUE, (center_col, center_row), giant_radius, CIRCLE_WIDTH)


def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    return None


def check_sub_board_winner(sub_board_index):
    sub_board = board[sub_board_index]
    return check_winner(sub_board)


def check_main_board_winner():
    return check_winner(main_board)


def is_draw():
    return all(cell != ' ' for cell in main_board)


def mark_square(sub_board_index, cell_index, player):
    # Mark the player's move
    board[sub_board_index][cell_index] = player
    draw_figures()
    pygame.display.update()
    pygame.time.wait(500)  # Wait for 500 milliseconds to show the move
    # Check if this move wins the sub-board
    winner = check_sub_board_winner(sub_board_index)
    if winner:
        main_board[sub_board_index] = winner
        board[sub_board_index] = [winner] * 9  # Mark the sub-board with the winner's marker


def restart():
    screen.fill(WHITE)
    draw_lines()
    global board, main_board, current_player, next_move, game_over
    board = [[' ' for _ in range(9)] for _ in range(9)]
    main_board = [' ' for _ in range(9)]
    current_player = 'X'
    next_move = None
    game_over = False


draw_lines()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            draw_lines()
            draw_figures()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            width, height = screen.get_size()
            square_size = width // 9

            mouseX = event.pos[0]  # X
            mouseY = event.pos[1]  # Y

            clicked_row = mouseY // square_size
            clicked_col = mouseX // square_size

            sub_board_index = (clicked_row // 3) * 3 + (clicked_col // 3)
            cell_index = (clicked_row % 3) * 3 + (clicked_col % 3)

            # Check if the player is allowed to play on this sub-board
            if (next_move is None or next_move == sub_board_index) and main_board[sub_board_index] == ' ' and board[sub_board_index][cell_index] == ' ':
                mark_square(sub_board_index, cell_index, current_player)
                if check_main_board_winner():
                    game_over = True
                    print(f"Player {current_player} wins!")
                elif is_draw():
                    game_over = True
                    print("The game is a draw!")
                else:
                    next_move = cell_index  # Set the next move to the clicked cell
                    # Check if the sub-board for the next move is already won or full
                    if main_board[next_move] != ' ' or all(board[next_move][i] != ' ' for i in range(9)):
                        next_move = None  # Allow the next player to choose any sub-board
                    current_player = 'O' if current_player == 'X' else 'X'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

    draw_figures()
    pygame.display.update()
