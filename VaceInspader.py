# Custom made Space Invader type game

"""
TO DO LIST:

x Ship canon
x Alien grid
x Alien bullet (shoot at random time, from random alien)
x End screen
- Different Alien Sprites (or just different colors)
/ Sound Effects
x Add lives
x Add bullet/ship collision
x Add alien/ship collision
"""

import pygame
import os
import random

# Screen size
WIDTH = 600
HEIGHT = 700

# FPS cap
FPS = 60

# Color references
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Background image
# BACKGROUND = pygame.image.load(os.path.join('Assets', 'alien_2.png'))
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'background.jpg'))
BACKGROUND = pygame.transform.rotate(BACKGROUND_IMAGE, 90)
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = BACKGROUND.get_size()
BACKGROUND_START_W, BACKGROUND_START_H = (-(BACKGROUND_WIDTH - WIDTH)//2, -(BACKGROUND_HEIGHT - HEIGHT)//2)

# Win text
YOU_WIN_IMAGE = pygame.image.load(os.path.join('Assets', 'you_win.png'))
YOU_WIN_RATIO = YOU_WIN_IMAGE.get_size()[0] / YOU_WIN_IMAGE.get_size()[1]
YOU_WIN = pygame.transform.scale(YOU_WIN_IMAGE, (WIDTH//2, (WIDTH//2) // YOU_WIN_RATIO))

# Sprite sizes
SHIP_WIDTH, SHIP_HEIGHT = 60, 60
ALIEN_WIDTH, ALIEN_HEIGHT = 40, 30
SHIP_LASER_WIDTH, SHIP_LASER_HEIGHT = 20, 60
ALIEN_BULLET_WIDTH, ALIEN_BULLET_HEIGHT = 20, 30

# Sprites
SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'ship.png'))
SHIP = pygame.transform.scale(SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
ALIEN_IMAGE = pygame.image.load(os.path.join('Assets', 'alien.png'))
ALIEN = pygame.transform.scale(ALIEN_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT))
SHIP_LASER_IMAGE = pygame.image.load(os.path.join('Assets', 'ship_laser.png'))
# Laser's height and width are inverted here because of the rotation
SHIP_LASER = pygame.transform.rotate(pygame.transform.scale(SHIP_LASER_IMAGE, (SHIP_LASER_HEIGHT, SHIP_LASER_WIDTH)), 90)
ALIEN_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'alien_bullet.png'))
ALIEN_BULLET = pygame.transform.scale(ALIEN_BULLET_IMAGE, (ALIEN_BULLET_WIDTH, ALIEN_BULLET_HEIGHT))

# Sounds
pygame.mixer.init()
LASER_NOISE = pygame.mixer.Sound(os.path.join('Assets', 'laser.mp3'))
EXPLOSION = pygame.mixer.Sound(os.path.join('Assets', 'brr.mp3'))

# Other settings
BACKGROUND_SPEED = 3 # px
SHIP_SPEED = 5 # px
MAX_LASERS = 3
LASER_SPEED = 5 # px
LASER_DELAY = 300 # ms
ALIEN_SPEED = 800 # ms
ALIEN_STEP = ALIEN_WIDTH//2 # px
ALIEN_PADDING = int(1.5 * ALIEN_WIDTH) # px
MIN_BULLET_WAIT = 800
MAX_BULLET_WAIT = 2000
LEVEL = 4

# Window Setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill(BLACK)
pygame.display.set_caption('Vace Inspaders')
pygame.display.set_icon(SHIP)
pygame.font.init()
txt_font = pygame.font.SysFont('Times New Romans', 25)

# Ship Firing function
lasers = []
def shoot_laser(ship, lasers): # Will not shoot more than 3 lasers at a time, one at a second
    if len(lasers) >= MAX_LASERS:
        return
    else:
        l = pygame.Rect(ship.x + SHIP_WIDTH//2 - SHIP_LASER_WIDTH//2,
         ship.y - SHIP_LASER_HEIGHT,
         SHIP_LASER_WIDTH, SHIP_LASER_HEIGHT)
        pygame.mixer.Sound.play(LASER_NOISE)
        lasers.append(l)

# Aliens initial setup
def place_aliens(nb_lines):
    aliens = []
    aliens_per_line = WIDTH//(ALIEN_WIDTH + ALIEN_PADDING) - 1
    for line in range(nb_lines):
        for alien in range(aliens_per_line):
            aliens.append(pygame.Rect(alien * (ALIEN_PADDING + ALIEN_WIDTH),
             HEIGHT//4 - line * ((ALIEN_HEIGHT + ALIEN_PADDING)),
             ALIEN_WIDTH, ALIEN_HEIGHT))

    return aliens


# Alien bullet firing function
bullets = []
def fire_bullet(alien):
    b = pygame.Rect(alien.x + ALIEN_WIDTH//2 - ALIEN_BULLET_WIDTH//2,
     alien.y + ALIEN_HEIGHT, ALIEN_BULLET_WIDTH, ALIEN_BULLET_HEIGHT)
    bullets.append(b)

# Screen updating function
def draw_screen(background, ship, aliens, lasers, bullets, running, lives):
    lives_display = txt_font.render('LIVES: ' + str(lives), False, WHITE)
    
    WIN.blit(BACKGROUND, (background.x, background.y % BACKGROUND_HEIGHT))
    WIN.blit(BACKGROUND, (background.x, (background.y % BACKGROUND_HEIGHT) - BACKGROUND_HEIGHT))
    WIN.blit(SHIP, (ship.x, ship.y))
    for a in aliens:
        WIN.blit(ALIEN, (a.x, a.y))
    for l in lasers:
        WIN.blit(SHIP_LASER, (l.x, l.y))
    for b in bullets:
        WIN.blit(ALIEN_BULLET, (b.x, b.y))

    WIN.blit(lives_display, (10, 10))
    if not running:
        WIN.blit(YOU_WIN, ((WIDTH - YOU_WIN.get_width())//2, (HEIGHT - YOU_WIN.get_height())//2))

    pygame.display.update()

    if not running:
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    pygame.quit()


clock = pygame.time.Clock()
r_gen = random.Random()

def main():
    # Initialization
    ship = pygame.Rect(WIDTH//2 - SHIP_WIDTH//2, HEIGHT - 10 - SHIP_HEIGHT, SHIP_WIDTH, SHIP_HEIGHT)
    aliens = place_aliens(LEVEL)
    alien_speed = ALIEN_SPEED
    alien_step = ALIEN_STEP
    background = pygame.Rect(BACKGROUND_START_W, BACKGROUND_START_H, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
    last_laser = 0
    last_move = 0
    last_bullet = 0
    bullet_timer = r_gen.randint(MIN_BULLET_WAIT, MAX_BULLET_WAIT)
    lives = 3

    # Game Loop
    running = True
    while running:
        clock.tick(FPS)
        # Exit Condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()

        if len(aliens) == 0:
            running = False
            continue

        # Ship movements
        if keys_pressed[pygame.K_LEFT]:
            ship.x = max(ship.x - SHIP_SPEED, 0) # Border check left

        if keys_pressed[pygame.K_RIGHT]:
            ship.x = min(ship.x + SHIP_SPEED, WIDTH - SHIP_WIDTH) # border check right


        if keys_pressed[pygame.K_SPACE]:
            if pygame.time.get_ticks() - last_laser > LASER_DELAY:
                shoot_laser(ship, lasers)
                last_laser = pygame.time.get_ticks()

        # At a random time, random alien fires bullet
        if pygame.time.get_ticks() > last_bullet + bullet_timer:
            fire_bullet(aliens[r_gen.randint(0, len(aliens) - 1)])
            last_bullet = pygame.time.get_ticks()
            bullet_timer = r_gen.randint(MIN_BULLET_WAIT, MAX_BULLET_WAIT)


        # Alien movements
        if pygame.time.get_ticks() - last_move > alien_speed:
            # Alien touches the ship
            for a in aliens:
                if a.colliderect(ship):
                    running = False
                    continue

            # Last alien decides of the bounce on screen border
            if max(map(lambda x: x.x, aliens)) + ALIEN_WIDTH + alien_step > WIDTH:
                alien_step *= -1
                alien_speed = max(ALIEN_SPEED//10, alien_speed - ALIEN_SPEED//10)
                for alien in aliens:
                    alien.y += ALIEN_STEP

            elif min(map(lambda x: x.x, aliens)) + alien_step < 0:
                alien_step *= -1
                alien_speed = max(ALIEN_SPEED//10, alien_speed - ALIEN_SPEED//10)
                for alien in aliens:
                    alien.y += ALIEN_STEP

            else:
                for alien in aliens:
                    alien.x += alien_step
        
            last_move = pygame.time.get_ticks()

        
    # Projectiles movements
        # Ship lasers
        for l in lasers: # Out of bounds
            if l.y + SHIP_LASER_HEIGHT == 0:
                lasers.remove(l)
                continue

            for a in aliens: # Hits alien
                if l.colliderect(a):
                    aliens.remove(a)
                    lasers.remove(l)
                    pygame.mixer.Sound.play(EXPLOSION)
                    continue

            l.y -= LASER_SPEED # Laser progression

        # Alien Bullets
        for b in bullets:
            if b.colliderect(ship):
                lives -= 1
                bullets.remove(b)

            if lives == 0:
                running = False
                continue

            b.y += LASER_SPEED

        background.y += BACKGROUND_SPEED # Scrolls background
        draw_screen(background, ship, aliens, lasers, bullets, running, lives) # Update screen
    draw_screen(background, ship, aliens, lasers, bullets, running, lives) # End of game


if __name__ == '__main__':
    main()
