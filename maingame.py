import pygame
import random
import tkinter as tk
from tkinter import messagebox

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 10
CELL_SIZE = 50
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the game window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Longest Line")

# Function to display the win screen with buttons
def show_win_screen(winner):
    root = tk.Tk()
    root.withdraw()
    if winner == "Player":
        result = messagebox.askquestion("Game Over", "You win!\nPlay again?")
    elif winner == "AI":
        result = messagebox.askquestion("Game Over", "AI wins!\nPlay again?")
    else:
        result = messagebox.askquestion("Game Over", "It's a draw!\nPlay again?")
        
    if result == "yes":
        reset_game()
    else:
        global running
        running = False

# Function to draw the grid
def draw_grid():
    for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
        pygame.draw.line(window, BLACK, (x, 0), (x, WINDOW_SIZE[1]))
    for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
        pygame.draw.line(window, BLACK, (0, y), (WINDOW_SIZE[0], y))

# Function to check for a win
def check_win(player):
    for x in range(GRID_SIZE - 5):
        for y in range(GRID_SIZE):
            if all(board[x + i][y] == player for i in range(6)):
                return True
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 5):
            if all(board[x][y + i] == player for i in range(6)):
                return True
    for x in range(GRID_SIZE - 5):
        for y in range(GRID_SIZE - 5):
            if all(board[x + i][y + i] == player for i in range(6)):
                return True
            if all(board[x + i][y + 5 - i] == player for i in range(6)):
                return True
    return False

# Function to reset the game
def reset_game():
    global board, player_turn, game_over
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player_turn = True
    game_over = False

# Initialize game variables
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player_turn = True
game_over = False

# Function to get the gradient color for a pixel inside a cell
def get_gradient_color(x, y, px, py):
    total_size = GRID_SIZE * CELL_SIZE
    # Top-left corner color (Tropical cyan for the player, Light soft red for the AI)
    if board[x][y] == BLUE:
        color_tl = (0, 255, 255)  # Tropical cyan (bright cyan)
    elif board[x][y] == RED:
        color_tl = (255, 102, 102)  # Light soft red
    else:
        color_tl = (255, 255, 255)  # Empty cell color

    # Bottom-right corner color (Fresh minty green for the player, Pastel orange for the AI)
    if board[x][y] == BLUE:
        color_br = (0, 128, 128)  # Fresh minty green (a darker cyan)
    elif board[x][y] == RED:
        color_br = (255, 178, 102)  # Pastel orange
    else:
        color_br = (255, 255, 255)  # Empty cell color

    # Calculate the gradient color for the current pixel
    grad_color = (
        color_tl[0] + (color_br[0] - color_tl[0]) * (px + x * CELL_SIZE) / total_size,
        color_tl[1] + (color_br[1] - color_tl[1]) * (py + y * CELL_SIZE) / total_size,
        color_tl[2] + (color_br[2] - color_tl[2]) * (px + x * CELL_SIZE) / total_size,
    )

    return grad_color

# Game loop
running = True
while running:
    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if player_turn:
                # Get the clicked cell position
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if board[x][y] is None:
                    board[x][y] = BLUE
                    if check_win(BLUE):
                        game_over = True
                        show_win_screen("Player")
                    else:
                        player_turn = False
                        # AI move (randomly selects an empty cell)
                        while not game_over:
                            x_ai, y_ai = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
                            if board[x_ai][y_ai] is None:
                                board[x_ai][y_ai] = RED
                                if check_win(RED):
                                    game_over = True
                                    show_win_screen("AI")
                                player_turn = True
                                break

    # Draw the grid
    draw_grid()

    # Draw the gradient lines
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[x][y] is not None:
                for px in range(CELL_SIZE):
                    for py in range(CELL_SIZE):
                        grad_color = get_gradient_color(x, y, px, py)
                        window.set_at((x * CELL_SIZE + px, y * CELL_SIZE + py), grad_color)

    pygame.display.flip()

    # Check for restart or quit
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset_game()
    elif keys[pygame.K_q]:
        running = False

# Quit Pygame
pygame.quit()






