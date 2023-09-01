import pygame
from pygame import mixer

import math
import random

# CUSTOM LOOK FOR ERRORS DISPLAY
import pretty_errors

pretty_errors.configure(
    separator_character='*',
    line_color=pretty_errors.BRIGHT_RED + '-> ' + pretty_errors.default_config.line_color,
    lines_before=5,
    lines_after=5,
    code_color=pretty_errors.BLUE,
    filename_color=pretty_errors.BRIGHT_BLACK,
    function_color=pretty_errors.BLACK,
    line_number_color=pretty_errors.BRIGHT_GREEN + 'Line: '
)

from actors.player import Player
from actors.bullets import Bullets
from actors.enemies import Enemies
from actors.player_upgrades import PlayerUpgrades

# Initialize the Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1920, 1100))

'''
Keeping all media rendering outside the Main Game Loop 
so rendering of images/sounds does not need to be re-rendered
at every 'game surface' update
'''

# Background image
background = pygame.image.load('./images/background.png')

# Background Sound
mixer.music.load("./sounds/background.wav")
mixer.music.set_volume(0.6)
mixer.music.play(-1)

# App Name and Icon
pygame.display.set_caption("Space Invaders Clone")
icon = pygame.image.load('./images/player_spaceship_sprite.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('./images/player_spaceship_sprite.png')
playerX = 930
playerY = 1020
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10
# Creates initial enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./images/enemy_spaceship_sprite.png'))
    # Random coordinates for enemy spawning positions
    enemyX.append(random.randint(0, 1856)) # 1856 = 1920 (game surface) - 64 (enemy ship width)
    enemyY.append(random.randint(50, 400))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready - bullet is hidden and ready to be fired
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('./images/laser_bullet.png')
bulletX = 0
bulletY = 980
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('./font/scifi.otf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('./font/scifi.otf', 64)

# Game Score section
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 0))
    # blit means to draw the object on screen (game surface)
    screen.blit(score, (x, y))

# Game Over text
def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(over_text, (700, 500))

# Player - initial placement of player
def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy - initial placement of all the enemies
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet
# Fire - The bullet is currently moving
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 26, y + 10))

# Taking Enemy Ship and Bullet coordinates 
# and if they are closer then 27px then they 'collided'
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Main Game Loop - keeps the game running
# all events in here
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    
    # Controls & Quit 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            # check whether its right arrow / left arrow / space bar 
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("./sounds/laser.wav")
                    bulletSound.set_volume(0.3)
                    bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # Stop movement of ship with KEYUP as arrows are released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Keep Player Spaceship from going off screen
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1856: # 1920 (game surface) - 64 (player ship width)
        playerX = 1856

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 972: # Enemy Ship reaches Player Ship
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            # ADD
            # GAME OVER SOUND EFFECT !!!!!!!!!!!!!!!!
            
            game_over_text()
            break
            # ADD
            # RESTART GAME | QUIT buttons !!!!!!!!!!!!!!!!!!!!
        
        # Keep Enemy Spaceship from going off screen AND lower it when it hits boundary
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1856: # 1920 (game surface) - 64 (player ship width)
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision of bullet and enemy
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("./sounds/explosion.wav")
            explosionSound.set_volume(0.3)
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # Next generation enemies speed up
            if enemyX_change[i] > 0:
                enemyX_change[i] += 1
            else:
                enemyX_change[i] -= 1
            #num_of_enemies += 1      !!!!!!!!!!!!!!!!!!!!!!!!!
            enemyX[i] = random.randint(0, 1856)
            enemyY[i] = random.randint(50, 150)
            # ADD:
            # check for enemies overlapping and space them out !!!!!!!!!!!!!!!!!!!!!!

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 1000
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    
    show_score(textX, textY)
    
    # Continuous updating of game window 
    pygame.display.update()