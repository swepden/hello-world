"""
A simple Snake game implemented using Pygame.
"""
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREEN_BG = (0, 150, 50) # New background color
PARTY_HAT_COLOR = (255, 0, 255) # Magenta for the hat

# Define window dimensions and cell size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20

# Ensure WINDOW_WIDTH and WINDOW_HEIGHT are multiples of CELL_SIZE
if WINDOW_WIDTH % CELL_SIZE != 0 or WINDOW_HEIGHT % CELL_SIZE != 0:
    raise ValueError("WINDOW_WIDTH and WINDOW_HEIGHT must be multiples of CELL_SIZE")

# Snake properties
snake_pos = [10, 5]  # Initial x, y grid coordinates for the head
snake_body = [[10, 5], [9, 5], [8, 5]]  # List of [x,y] segment coordinates, head first
direction = "RIGHT"
change_to_direction = direction

# Food properties - Initial food placement, ensuring it's not on the snake
food_pos = []
new_food_pos_found = False
while not new_food_pos_found:
    temp_food_pos = [random.randrange(1, (WINDOW_WIDTH // CELL_SIZE)), random.randrange(1, (WINDOW_HEIGHT // CELL_SIZE))]
    if temp_food_pos not in snake_body:
        food_pos = temp_food_pos
        new_food_pos_found = True
food_spawn = True

# Game State variables
game_over = False
score = 0

# Create the game display screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# FPS controller
fps_controller = pygame.time.Clock()

# Function to display score
def show_score(choice, color, font_name, size):
    """Displays the current score on the screen."""
    score_font = pygame.font.SysFont(font_name, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:  # For displaying during gameplay
        score_rect.midtop = (WINDOW_WIDTH / 10, 15)
    # else: # Choice 0 for game over screen score is handled directly in show_game_over_screen
    screen.blit(score_surface, score_rect)

# Game Over function
def show_game_over_screen():
    """Displays the Game Over message and final score, then quits."""
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render('Game Over!', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
    screen.blit(game_over_surface, game_over_rect)

    # Display final score
    final_score_font = pygame.font.SysFont('times new roman', 30)
    final_score_surface = final_score_font.render('Your Score : ' + str(score), True, RED)
    final_score_rect = final_score_surface.get_rect()
    final_score_rect.midtop = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.8)
    screen.blit(final_score_surface, final_score_rect)

    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Allows exiting the loop if sys.exit() hasn't been called
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to_direction = "UP"
            elif event.key == pygame.K_DOWN:
                change_to_direction = "DOWN"
            elif event.key == pygame.K_LEFT:
                change_to_direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                change_to_direction = "RIGHT"

    if not game_over:
        # Validate direction change
        if change_to_direction == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to_direction == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to_direction == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to_direction == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        # Update snake position
        if direction == "UP":
            snake_pos[1] -= 1
        if direction == "DOWN":
            snake_pos[1] += 1
        if direction == "LEFT":
            snake_pos[0] -= 1
        if direction == "RIGHT":
            snake_pos[0] += 1

        # Boundary collision check
        if snake_pos[0] < 0 or snake_pos[0] >= (WINDOW_WIDTH // CELL_SIZE) or \
           snake_pos[1] < 0 or snake_pos[1] >= (WINDOW_HEIGHT // CELL_SIZE):
            game_over = True

        # Snake body mechanism (insert new head)
        snake_body.insert(0, list(snake_pos))

        # Self-collision check (only if not already game over by boundary)
        if not game_over:
            for block in snake_body[1:]:
                if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                    game_over = True
                    break

        # Food eating logic
        if not game_over: # Process food only if game is still on
            if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
                score += 10
                food_spawn = False
            else:
                snake_body.pop() # Pop tail if no food eaten AND no game over

            if not food_spawn:
                # Respawn food, ensuring it's not on the snake's body
                new_food_pos_found = False
                while not new_food_pos_found:
                    food_pos = [random.randrange(1, (WINDOW_WIDTH // CELL_SIZE)), random.randrange(1, (WINDOW_HEIGHT // CELL_SIZE))]
                    if food_pos not in snake_body:
                        new_food_pos_found = True
                food_spawn = True

    # --- Drawing Part --- (Happens regardless of game_over to show final state)
    screen.fill(GREEN_BG)
    # Draw grid
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WINDOW_WIDTH, y))
    # Draw snake
    for segment in snake_body:
        center_x = segment[0] * CELL_SIZE + CELL_SIZE // 2
        center_y = segment[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, GREEN, (center_x, center_y), CELL_SIZE // 2)

    # Draw party hat on the snake's head
    if snake_body: # Ensure snake_body is not empty
        head_segment = snake_body[0]
        head_center_x = head_segment[0] * CELL_SIZE + CELL_SIZE // 2
        head_center_y = head_segment[1] * CELL_SIZE + CELL_SIZE // 2

        hat_height = CELL_SIZE * 0.8
        hat_width_base = CELL_SIZE * 0.6

        point1 = (head_center_x - hat_width_base // 2, head_center_y - CELL_SIZE // 4) # Left base
        point2 = (head_center_x + hat_width_base // 2, head_center_y - CELL_SIZE // 4) # Right base
        point3 = (head_center_x, head_center_y - CELL_SIZE // 4 - hat_height)     # Tip

        hat_points = [point1, point2, point3]
        pygame.draw.polygon(screen, PARTY_HAT_COLOR, hat_points)

    # Draw food
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0] * CELL_SIZE, food_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Show live score
    show_score(1, WHITE, 'times new roman', 20)

    # --- Game Over Handling ---
    if game_over:
        show_game_over_screen() # This function handles message and exits

    pygame.display.flip()
    fps_controller.tick(10)

# Cleanup if loop somehow exits normally (e.g., by 'running = False' and not sys.exit() from game over)
pygame.quit()
sys.exit()
