import os
import pygame
import random

# initialize pygame
pygame.init()

# set the size of the game window
win_width = 500
win_height = 500
win = pygame.display.set_mode((win_width, win_height))

# set the title of the game window
pygame.display.set_caption("Jumping Game")

# define the colors we'll use
black = (0, 0, 0)
white = (255, 255, 255)

# define the player's starting position and speed
player_x = 100
player_speed = 10
player_jump_speed = 20
player_jump_height = 200
player_falling = False
player_y_vel = 0

# load the player's sprite
player_img_path = os.path.join("sprites", "player.png")
player_img = pygame.image.load(player_img_path)
player_width = player_img.get_width()
player_height = player_img.get_height()

# define the ground's position and size
ground_height = 50
ground_y = win_height - ground_height
ground_rect = pygame.Rect(0, ground_y, win_width, ground_height)

# define the player's Rect object
player_y = ground_y - player_height
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# define the obstacle's size and speed
obstacle_width = 30
obstacle_height = 50
obstacle_speed = 10

# define the obstacle list
obstacles = []

# define the game clock
clock = pygame.time.Clock()

# define the game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player_falling:
                player_y_vel = -player_jump_speed
                player_falling = True

    # update the player's position
    player_rect.y += player_y_vel
    if player_falling:
        player_y_vel += 1
        if player_rect.bottom >= ground_rect.top:
            player_falling = False
            player_rect.bottom = ground_rect.top
            player_y_vel = 0

    # update the obstacles' positions
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed

    # create a new obstacle if necessary
    if len(obstacles) == 0 or obstacles[-1].x < win_width - obstacle_speed * 60:
        obstacle_x = win_width + obstacle_width
        obstacle_y = ground_y - obstacle_height
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
        obstacles.append(obstacle_rect)

    # remove obstacles that have gone off the left edge of the screen
    obstacles = [obstacle for obstacle in obstacles if obstacle.right > 0]

    # check for collisions with obstacles
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            running = False

    # draw the game objects
    win.fill(white)
    win.blit(player_img, player_rect)
    pygame.draw.rect(win, black, ground_rect)
    for obstacle in obstacles:
        pygame.draw.rect(win, black, obstacle)

    # update the display
    pygame.display.update()

    # limit the game to 60 frames per second
    clock.tick(60)

# quit pygame when the game loop is done
pygame.quit()
