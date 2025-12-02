import pygame
import time
import random

WIDTH, HEIGTH = 1000, 800
WIN = pygame.display.set_mode([WIDTH, HEIGTH])
pygame.display.set_caption("ok")
BG = pygame.transform.scale(pygame.image.load("Graphics/bg.png"), (WIDTH, HEIGTH))
icon = pygame.image.load("Graphics/coffee-cup.png")
pygame.display.set_icon(icon)

#Player making
PLAYER_IMG = pygame.image.load("Graphics/space-invaders.png")
player_x = 450
player_y = 700

#Enemy making
ENEMEY_IMG = pygame.image.load("Graphics/alien.png")
enemey_x = random.randint(0, WIDTH - 64)
enemey_y = random.randint(50, 150)
enemey_x_change = 3

#Bullet making
BULLET_IMG = pygame.image.load("Graphics/bullet.png")
bullet_x = player_x       
bullet_y = player_y
bullet_state = "ready" # "ready" - you can't see the bullet on the screen
                        # "fire" - the bullet is currently moving

#Scroe variable
score = 0
pygame.font.init()
font = pygame.font.SysFont('comicsans', 40)
text_x = 10
text_y = 10

#Draw The Image of Player
def players(x, y):
    WIN.blit(PLAYER_IMG, (x, y))

#Draw The Image of The Enemey
def enemy(x, y):
    WIN.blit(ENEMEY_IMG, (x, y))

#Fire Bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    WIN.blit(BULLET_IMG, (x + 16, y + 10))

#Draw Score
def show_scroe(x, y):
    score_value = font.render("Score:" + str(score), True, (255, 255, 255))
    WIN.blit(score_value, (x, y))

#Collision Detection
def is_collision(enemey_x, enemey_y, bullet_x, bullet_y):
    distance = ((enemey_x - bullet_x)**2 + (enemey_y - bullet_y)**2) ** 0.5
    if distance < 27:
        return True
    return False

#main loop
run = True
frame_rate = pygame.time.Clock()
while run:
    frame_rate.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
    WIN.blit(BG, (0, 0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5
    elif keys[pygame.K_RIGHT]:
        player_x += 5
    elif keys[pygame.K_UP]:
        player_y -= 5
    elif keys[pygame.K_DOWN]:
        player_y += 5
    elif keys[pygame.K_SPACE]:
            if bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
    #making the player stay in the window
    if player_x <= 0:
        player_x = 0
    #make sure that our player does not go out of the right side of the window
    elif player_x >= WIDTH - 64:
        player_x = WIDTH - 64
    if player_y <= 0:
        player_y = 0
    #make sure that our player does not go out of the bottom side of the window
    elif player_y >= HEIGTH - 64:
        player_y = HEIGTH - 64

    #making enemey movements and checking it dosen't go out of the window
    enemey_x += enemey_x_change
    if enemey_x <= 0:
        enemey_x_change = 3
    elif enemey_x >= WIDTH - 64:
        enemey_x_change = -3

    #Bullet Movement
    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= 14

    #Collision
    collision = is_collision(enemey_x, enemey_y, bullet_x, bullet_y)
    if collision:
        bullet_y = player_y
        bullet_state = "ready"
        score += 1
        enemey_x = random.randint(0, WIDTH - 64)
        enemey_y = random.randint(50, 150)
    
    
    players(player_x, player_y)
    enemy(enemey_x, enemey_y)
    show_scroe(text_x, text_y)

    pygame.display.update()
pygame.quit()