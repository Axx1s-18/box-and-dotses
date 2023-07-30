import pygame
import random
import tkinter as tk
from tkinter import messagebox
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()
music_file = "music.mp3"
noise_file = pygame.mixer.Sound("noise.mp3")
click_sound = pygame.mixer.Sound("click.wav")
pygame.mixer.music.load(music_file)

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
GRID_SIZE = 10
CELL_SIZE = 50
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_FILE = "mimafuse.ttf"
FONT_FILE = "mishmash.ttf"

# Calculate the appropriate window size to take up the entire screen
window_width = GRID_SIZE * CELL_SIZE
window_height = GRID_SIZE * CELL_SIZE
if window_width > SCREEN_WIDTH or window_height > SCREEN_HEIGHT:
    aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
    if window_width / window_height > aspect_ratio:
        window_width = int(SCREEN_WIDTH)
        window_height = int(SCREEN_WIDTH / (GRID_SIZE / CELL_SIZE))
    else:
        window_height = int(SCREEN_HEIGHT)
        window_width = int(SCREEN_HEIGHT * (GRID_SIZE / CELL_SIZE))

# Load the background image for the main menu and instructions screen
background_image = pygame.image.load("wallpaper.png")

# Set the window size before the main game loop
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)

# Load a custom font
custom_font = pygame.font.Font("mimafuse.ttf", 18)
# Load a custom font
customfont = pygame.font.Font("mishmash.ttf", 18)

# Function to set the volume of music and clicking sound
def set_volume(music_volume, click_volume):
    pygame.mixer.music.set_volume(music_volume)
    click_sound.set_volume(click_volume)

# Create the game window (fullscreen mode)
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Longest Line")

# Function to display the win screen with buttons
def show_win_screen(winner):
    root = tk.Tk()
    root.withdraw()

    if winner == "Player":
        message = "You win!\nPlay again?"
    elif winner == "AI":
        message = "AI wins!\nPlay again?"
    else:
        message = "It's a draw!\nPlay again?"

    result = messagebox.askquestion("Game Over", message)
    root.destroy()

    if result == "yes":
        start_new_game()
    else:
        pygame.quit()
        quit()

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

music_volume = 0.3
click_volume = 0.5

# Function to start a new game
def start_new_game():
    reset_game()

def draw_gradient_rect(surface, rect, color_left, color_right):
    gradient = pygame.Surface(rect.size, pygame.SRCALPHA)
    gradient_rect = pygame.Rect(0, 0, rect.width, rect.height)
    brightness_factor = 0.5  # Adjust this value to make the gradient darker or lighter

    for x in range(rect.width):
        r = int(color_left[0] + (color_right[0] - color_left[0]) * (x / rect.width))
        g = int(color_left[1] + (color_right[1] - color_left[1]) * (x / rect.width))
        b = int(color_left[2] + (color_right[2] - color_left[2]) * (x / rect.width))

        # Darken the color components
        r = int(r * brightness_factor)
        g = int(g * brightness_factor)
        b = int(b * brightness_factor)

        color = (r, g, b)
        pygame.draw.line(gradient, color, (x, 0), (x, rect.height))

    surface.blit(gradient, rect.topleft)

def draw_game_background():
    # Scale the background image to fit the window size while maintaining aspect ratio
    aspect_ratio = background_image.get_width() / background_image.get_height()
    scaled_width = WINDOW_SIZE[0]
    scaled_height = int(WINDOW_SIZE[0] / aspect_ratio)

    if scaled_height > WINDOW_SIZE[1]:
        scaled_width = int(WINDOW_SIZE[1] * aspect_ratio)
        scaled_height = WINDOW_SIZE[1]

    scaled_background = pygame.transform.scale(background_image, (scaled_width, scaled_height))

    # Calculate the position to center the scaled image
    x_offset = (WINDOW_SIZE[0] - scaled_width) // 2
    y_offset = (WINDOW_SIZE[1] - scaled_height) // 2

    # Blit the scaled image onto the window
    window.blit(scaled_background, (x_offset, y_offset))

def draw_main_menu_background():
    # Fill the window with the background image
    window.blit(background_image, (0, 0))

def draw_instructions_background():
    # This function intentionally does not draw anything, making the background transparent
    pass

def show_main_menu():
    pygame.mixer.music.play(-1)
    while True:
        window.fill(WHITE)
        # Draw the background image
        window.blit(background_image, (0, 0))
    
        menu_font = custom_font
        option_color = (0, 0, 0)
        option_spacing = 80
        menu_width = 200
        menu_height = 3 * option_spacing + 50

        # Calculate the center of the screen
        screen_center_x = SCREEN_WIDTH // 2
        screen_center_y = SCREEN_HEIGHT // 2

        menu_x = screen_center_x - menu_width // 2
        menu_y = screen_center_y - menu_height // 2

        menu_options = {
            "New Game": pygame.Rect(menu_x, menu_y, menu_width, 50),
            "Instructions": pygame.Rect(menu_x, menu_y + option_spacing, menu_width, 50),
            "Fake Settings": pygame.Rect(menu_x, menu_y + 2 * option_spacing, menu_width, 50),  # Add a new option for "Settings"
            "Quit": pygame.Rect(menu_x, menu_y + 3 * option_spacing, menu_width, 50)  # Adjust the positions for additional option
        }

        option_texts = {
            option: menu_font.render(option, True, option_color) for option in menu_options
        }

        # Adjust Y position for each option text to align with the top of the box
        for option, text in option_texts.items():
            text_rect = text.get_rect(center=(menu_x + menu_width // 2, menu_options[option].y + menu_options[option].h // 2))
            option_texts[option] = text, text_rect

        while True:
            window.fill(WHITE)
            # Draw the background image
            window.blit(background_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for option, rect in menu_options.items():
                        if rect.collidepoint(event.pos):
                            click_sound.play()
                            if option == "New Game":
                                start_new_game()
                            elif option == "Instructions":
                                show_instructions_screen()
                            elif option == "Fake Settings":
                                pass
                            else:
                                pygame.quit()
                                quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    if menu_options["Fake Settings"].collidepoint(pygame.mouse.get_pos()):
                        pygame.mixer.music.stop()
                        noise_file.play()

            for option, rect in menu_options.items():
                if rect.collidepoint(pygame.mouse.get_pos()):
                    draw_gradient_rect(window, rect, (200, 200, 200), (150, 150, 150))  # Gradient when the mouse is over it
                pygame.draw.rect(window, BLACK, rect, 2)  # Draw a black border around the option
                text, text_rect = option_texts[option]
                window.blit(text, text_rect)

            pygame.display.flip()



# Function to display the instructions screen
def show_instructions_screen():
    # Blit the background image onto the window
    window.blit(background_image, (0, 0))
    instructions_font = customfont
    instructions_color = (255, 255, 255)  # White color for the actual instructions text
    shadow_color = (50, 50, 50)  # Color for the shadow effect
    instructions = [
        "Instructions:",
        "",
        "1. The game is played on a 10x10 grid.",
        "2. You are the blue player, and the AI is the red player.",
        "3. To win, you must form a line of 6 squares in any direction: horizontally, vertically, or diagonally.",
        "4. Click on an empty cell to place your square.",
        "5. The AI will take its turn automatically after you place your square.",
        "6. If the grid is full and no one has formed a line of 6 squares, the game is a draw.",
        "",
        "Click anywhere to return to the main menu."
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Return to the main menu
                return

        # Calculate the starting Y position for instructions text
        text_start_y = window.get_height() // 2 - len(instructions) * 30 // 2

        for i, line in enumerate(instructions):
            # Render the shadow text with an offset position
            shadow_text = instructions_font.render(line, True, shadow_color)
            shadow_text_rect = shadow_text.get_rect(center=(window.get_width() // 2 + 2, text_start_y + i * 30 + 2))
            window.blit(shadow_text, shadow_text_rect)

            # Render the main text at the original position with white color
            instruction_text = instructions_font.render(line, True, instructions_color)
            text_rect = instruction_text.get_rect(center=(window.get_width() // 2, text_start_y + i * 30))
            window.blit(instruction_text, text_rect)

        pygame.display.flip()

# Function to show the main menu after a game ends
def show_main_menu_after_game():
    global running
    show_main_menu()
    running = False


# Game loop
running = True
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
window = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
show_main_menu()

while running:
    screen.blit(background_image,(0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
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

    # Clear the window first
    window.fill(WHITE)

    # Check which screen to draw based on the current state
    if in_game:
        draw_game_background()
        # Draw the game grid and other game elements here
        # ... (draw_grid() and other game drawing functions)
    elif in_instructions:
        draw_instructions_background()
        # Draw the instructions screen here
        # ... (draw_instructions_screen() function)
    else:
        draw_main_menu_background()
        # Draw the main menu here
        # ... (draw_main_menu() function)

    pygame.display.flip()

    # Check for restart or quit
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        reset_game()
    elif keys[pygame.K_q]:
        running = False

# Quit Pygame
pygame.quit()