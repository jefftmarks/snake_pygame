import pygame, random, csv
from colors import *

pygame.init()

# Set display
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("~~Snake~~")

# Set FPS and clock
FPS = 20
clock = pygame.time.Clock()

# Set game values
SNAKE_SIZE = 20
# To constrain random coordinates of apple to same grid as snake
WIDTH_INTERVALS = (WINDOW_WIDTH - SNAKE_SIZE) / SNAKE_SIZE
HEIGHT_INTERVALS = (WINDOW_HEIGHT - SNAKE_SIZE) / SNAKE_SIZE

head_x = CENTER_X
head_y = CENTER_Y + 100

snake_dx = 0
snake_dy = 0

score = 0

with open('high_score.txt') as file:
    high_score = file.read()

# Set fonts
font = pygame.font.Font('assets/LcdPhone-wgZ2.ttf', 48)
small_font = pygame.font.Font('assets/LcdPhone-wgZ2.ttf', 32)

# Set text
title_txt = font.render("Snake", True, GREEN, DARK_RED)
title_rect = title_txt.get_rect()
title_rect.center = (CENTER_X, CENTER_Y)

score_txt = font.render(f"Score {str(score)}", True, GREEN, DARK_RED)
score_rect = score_txt.get_rect()
score_rect.topleft = (10, 10)

high_score_txt = small_font.render(f"High Score {str(high_score)}", True, GREEN, DARK_RED)
high_score_rect = high_score_txt.get_rect()
high_score_rect.bottomleft = (10, WINDOW_HEIGHT - 10)

game_over_txt = font.render(f"GAME OVER", True, RED, DARK_GREEN)
game_over_rect = game_over_txt.get_rect()
game_over_rect.center = (CENTER_X, CENTER_Y)

new_high_score_txt = font.render(f"NEW HIGH SCORE", True, RED, DARK_GREEN)
new_high_score_rect = new_high_score_txt.get_rect()
new_high_score_rect.center = (CENTER_X, CENTER_Y - 64)

continue_txt_1 = font.render("Press any key", True, RED, DARK_GREEN)
continue_rect_1 = continue_txt_1.get_rect()
continue_rect_1.center = (CENTER_X, CENTER_Y + 64)

continue_txt_2 = font.render("to play again", True, RED, DARK_GREEN)
continue_rect_2 = continue_txt_2.get_rect()
continue_rect_2.center = (CENTER_X, continue_rect_1.centery + 48)

# Set sounds and music
pick_up_sound = pygame.mixer.Sound('assets/pick_up_sound.wav')

# Set images
def set_coord(x, y):
    return (x, y, SNAKE_SIZE, SNAKE_SIZE)


apple_coord = set_coord(500, 500)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

head_coord = set_coord(head_x, head_y)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

body_coords = []

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Move the snake
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT:
                    if snake_dx == 0:
                        snake_dx = -1 * SNAKE_SIZE
                        snake_dy = 0
                case pygame.K_RIGHT:
                    if snake_dx == 0:
                        snake_dx = SNAKE_SIZE
                        snake_dy = 0
                case pygame.K_UP:
                    if snake_dy == 0:
                        snake_dx = 0
                        snake_dy = -1 * SNAKE_SIZE
                case pygame.K_DOWN:
                    if snake_dy == 0:
                        snake_dx = 0
                        snake_dy = SNAKE_SIZE

    # Add head coordinate to first index of the body coordinate
    body_coords.insert(0, head_coord)
    body_coords.pop()

    # Update the x,y position of snake head
    head_x += snake_dx
    head_y += snake_dy
    head_coord = set_coord(head_x, head_y)

    # Check for game over
    if (
        head_rect.left < 0 or head_rect.right > WINDOW_WIDTH or
        head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT or
        head_coord in body_coords
    ):
        # Check high score
        if score > int(high_score):
            with open('high_score.txt', 'w') as file:
                file.write(str(score))
            display_surface.blit(new_high_score_txt, new_high_score_rect)

        display_surface.blit(game_over_txt, game_over_rect)
        display_surface.blit(continue_txt_1, continue_rect_1)
        display_surface.blit(continue_txt_2, continue_rect_2)
        pygame.display.update()

        # Pause the game
        paused = True
        while paused:
            for event in pygame.event.get():
                # Play again
                if event.type == pygame.KEYDOWN:
                    high_score_txt = small_font.render(f"High Score {str(score)}", True, GREEN, DARK_RED)

                    score = 0
                    head_x = CENTER_X
                    head_y = CENTER_Y + 100
                    head_coord = set_coord(head_x, head_y)
                    
                    body_coords = []
                    
                    snake_dx = 0
                    snake_dy = 0

                    paused = False
                # Quit
                if event.type == pygame.QUIT:
                    paused = False
                    running = False

    # Check for collisions
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()

        # Move apple
        apple_in_body = True
        while apple_in_body:
            apple_x = random.randint(0, WIDTH_INTERVALS) * SNAKE_SIZE
            apple_y = random.randint(0, HEIGHT_INTERVALS) * SNAKE_SIZE
            apple_coord = set_coord(apple_x, apple_y)

            if apple_coord not in body_coords:
                body_coords.append(head_coord)
                apple_in_body = False

    # Update HUD
    score_txt = font.render(f"Score {score}", True, GREEN, DARK_RED)

    # Fill surface
    display_surface.fill(WHITE)

    # Blit HUD
    display_surface.blit(title_txt, title_rect)
    display_surface.blit(score_txt, score_rect)
    display_surface.blit(high_score_txt, high_score_rect)

    # Blit assets
    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

    for body in body_coords:
        pygame.draw.rect(display_surface, DARK_GREEN, body)

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

# End game
pygame.quit()