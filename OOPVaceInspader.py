# Custom made Space Invader type game

"""
TO DO LIST:

OOP Version:

x Make everything OOP...
- Start networking part!
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

# Lose text
YOU_LOSE_IMAGE = pygame.image.load(os.path.join('Assets', 'you_lose.png'))
YOU_LOSE_RATIO = YOU_LOSE_IMAGE.get_size()[0] / YOU_LOSE_IMAGE.get_size()[1]
YOU_LOSE = pygame.transform.scale(YOU_LOSE_IMAGE, (WIDTH//2, (WIDTH//2) // YOU_LOSE_RATIO))

# Sprite sizes
SHIP_WIDTH, SHIP_HEIGHT = 60, 60
ALIEN_WIDTH, ALIEN_HEIGHT = 40, 30
SHIP_LASER_WIDTH, SHIP_LASER_HEIGHT = 20, 60
ALIEN_BULLET_WIDTH, ALIEN_BULLET_HEIGHT = 20, 30

# Sprites
SHIP1_IMAGE = pygame.image.load(os.path.join('Assets', 'ship.png'))
SHIP1 = pygame.transform.scale(SHIP1_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))
ALIEN_IMAGE = pygame.image.load(os.path.join('Assets', 'alien.png'))
ALIEN = pygame.transform.scale(ALIEN_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT))
SHIP_LASER_IMAGE = pygame.image.load(os.path.join('Assets', 'ship_laser.png'))
# Laser's height and width are inverted here because of the 90 deg anti-clockwise rotation
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
LASER1_SPEED = 5 # px
LASER_DELAY = 300 # ms
ALIEN_SPEED = 800 # ms
ALIEN_STEP = ALIEN_WIDTH//2 # px
ALIEN_PADDING = int(1.5 * ALIEN_WIDTH) # px
MIN_BULLET_WAIT = 800
MAX_BULLET_WAIT = 2000
LEVEL = 4

# Code-wide tools
clock = pygame.time.Clock()
r_gen = random.Random()

class Ship():
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - SHIP_WIDTH//2, HEIGHT - 10 - SHIP_HEIGHT, SHIP_WIDTH, SHIP_HEIGHT)
        self.last_laser = 0
        self.lasers = []
        self.lives = 3

    @property
    def x(self):
        return self.rect.x 

    @x.setter
    def x(self, val):
        self.rect.x = val

    @property
    def y(self):
        return self.rect.y

    @y.setter 
    def y(self, val):
        self.rect.y = val

    # Ship movements
    def movements(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.x = max(self.x - SHIP_SPEED, 0) # Border check left

        if keys_pressed[pygame.K_RIGHT]:
            self.x = min(self.x + SHIP_SPEED, WIDTH - SHIP_WIDTH) # border check right


        if keys_pressed[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.last_laser > LASER_DELAY:
                self.shoot_laser()
                self.last_laser = pygame.time.get_ticks()

    # Ship Firing function
    def shoot_laser(self): # Will not shoot more than 3 lasers at a time, one at a second
        if len(self.lasers) >= MAX_LASERS:
            return
        else:
            l = Laser(self)
            pygame.mixer.Sound.play(LASER_NOISE)
            self.lasers.append(l)


class Laser():
    def __init__(self, ship):
        self.rect = pygame.Rect(ship.x + SHIP_WIDTH//2 - SHIP_LASER_WIDTH//2,
            ship.y - SHIP_LASER_HEIGHT,
            SHIP_LASER_WIDTH, SHIP_LASER_HEIGHT)

    @property
    def x(self):
        return self.rect.x 

    @x.setter
    def x(self, val):
        self.rect.x = val

    @property
    def y(self):
        return self.rect.y

    @y.setter 
    def y(self, val):
        self.rect.y = val


class Alien():
    bullets = []

    def __init__(self, start_x, start_y):
        self.rect = pygame.Rect(start_x, start_y, ALIEN_WIDTH, ALIEN_HEIGHT)

    @property 
    def x(self):
        return self.rect.x 

    @x.setter
    def x(self, val):
        self.rect.x = val

    @property
    def y(self):
        return self.rect.y

    @y.setter 
    def y(self, val):
        self.rect.y = val

    @classmethod
    def add_bullet(cls, b):
        cls.bullets.append(b)

    # Alien bullet firing function
    def fire_bullet(self):
        b = Bullet(self)
        Alien.add_bullet(b)


class Bullet():
    def __init__(self, alien):
        self.rect = pygame.Rect(alien.x + ALIEN_WIDTH//2 - ALIEN_BULLET_WIDTH//2,
                    alien.y + ALIEN_HEIGHT, 
                    ALIEN_BULLET_WIDTH, ALIEN_BULLET_HEIGHT)

    @property 
    def x(self):
        return self.rect.x 

    @x.setter
    def x(self, val):
        self.rect.x = val

    @property
    def y(self):
        return self.rect.y

    @y.setter 
    def y(self, val):
        self.rect.y = val


class Game():
    # Window Setup
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.font.init()
    TXT_FONT = pygame.font.SysFont('Times New Romans', 25)
    pygame.display.set_caption('Vace Inspaders')
    pygame.display.set_icon(SHIP1)

    def __init__(self):
        self.ship = Ship()
        self.aliens = self.place_aliens(LEVEL)
        self.alien_speed = ALIEN_SPEED
        self.alien_step = ALIEN_STEP
        self.background = pygame.Rect(BACKGROUND_START_W, BACKGROUND_START_H, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        self.last_move = 0
        self.last_bullet = 0
        self.bullet_timer = r_gen.randint(MIN_BULLET_WAIT, MAX_BULLET_WAIT)
        self.end_state = ''

    # Aliens initial setup
    def place_aliens(self, nb_lines):
        aliens = []
        aliens_per_line = WIDTH//(ALIEN_WIDTH + ALIEN_PADDING) - 1
        for line in range(nb_lines):
            for col in range(aliens_per_line):
                aliens.append(Alien(col * (ALIEN_PADDING + ALIEN_WIDTH),
                HEIGHT//4 - line * (ALIEN_HEIGHT + ALIEN_PADDING)))

        return aliens

    # Alien movements
    def alien_movements(self):
        if pygame.time.get_ticks() - self.last_move > self.alien_speed:
            # Alien touches the ship
            for a in self.aliens:
                if a.rect.colliderect(self.ship):
                    running = False
                    continue

            # Last alien decides of the bounce on screen border
            if max(map(lambda x: x.x, self.aliens)) + ALIEN_WIDTH + self.alien_step > WIDTH:
                self.alien_step *= -1
                self.alien_speed = max(ALIEN_SPEED//10, self.alien_speed - ALIEN_SPEED//10)
                for alien in self.aliens:
                    alien.y += ALIEN_STEP

            elif min(map(lambda x: x.x, self.aliens)) + self.alien_step < 0:
                self.alien_step *= -1
                self.alien_speed = max(ALIEN_SPEED//10, self.alien_speed - ALIEN_SPEED//10)
                for alien in self.aliens:
                    alien.y += ALIEN_STEP

            else:
                for alien in self.aliens:
                    alien.x += self.alien_step
        
            self.last_move = pygame.time.get_ticks()

    # At a random time, random alien fires bullet -> will go in game class
    def alien_fire(self):
        if pygame.time.get_ticks() > self.last_bullet + self.bullet_timer:
            self.aliens[r_gen.randint(0, len(self.aliens) - 1)].fire_bullet()
            self.last_bullet = pygame.time.get_ticks()
            self.bullet_timer = r_gen.randint(MIN_BULLET_WAIT, MAX_BULLET_WAIT)

    # Ship lasers
    def laser_movements(self):
        for l in self.ship.lasers: # Out of bounds
            if l.y + SHIP_LASER_HEIGHT == 0:
                self.ship.lasers.remove(l)
                continue

            for a in self.aliens: # Hits alien
                if l.rect.colliderect(a):
                    self.aliens.remove(a)
                    self.ship.lasers.remove(l)
                    pygame.mixer.Sound.play(EXPLOSION)
                    continue

            l.y -= LASER1_SPEED # Laser progression

    # Alien Bullets
    def bullet_movements(self):
        for b in Alien.bullets:
            if b.rect.colliderect(self.ship):
                self.ship.lives -= 1
                Alien.bullets.remove(b)

            if self.ship.lives == 0:
                running = False
                self.end_state = 'lose'
                continue

            b.y += LASER1_SPEED

    # Screen updating function
    def draw_screen(self):
        lives_display = self.TXT_FONT.render('LIVES: ' + str(self.ship.lives), False, WHITE)
        
        self.WIN.blit(BACKGROUND, (self.background.x, self.background.y % BACKGROUND_HEIGHT))
        self.WIN.blit(BACKGROUND, (self.background.x, (self.background.y % BACKGROUND_HEIGHT) - BACKGROUND_HEIGHT))
        self.WIN.blit(SHIP1, (self.ship.x, self.ship.y))
        for a in self.aliens:
            self.WIN.blit(ALIEN, (a.x, a.y))
        for l in self.ship.lasers:
            self.WIN.blit(SHIP_LASER, (l.x, l.y))
        for b in Alien.bullets:
            self.WIN.blit(ALIEN_BULLET, (b.x, b.y))

        self.WIN.blit(lives_display, (10, 10))
        if self.end_state == 'win':
            self.WIN.blit(YOU_WIN, ((WIDTH - YOU_WIN.get_width())//2, (HEIGHT - YOU_WIN.get_height())//2))
        elif self.end_state == 'lose':
            self.WIN.blit(YOU_LOSE, ((WIDTH - YOU_LOSE.get_width())//2, (HEIGHT - YOU_LOSE.get_height())//2))

        pygame.display.update()

        if self.end_state == 'win' or self.end_state == 'lose':
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        wait = False


    def run_game(self):

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

            if len(self.aliens) == 0:
                running = False
                self.end_state = 'win'
                continue

            self.ship.movements(keys_pressed)

            self.alien_fire()

            self.alien_movements()

            self.laser_movements()

            self.bullet_movements()
            
            if self.end_state == 'lose':
                continue

            self.background.y += BACKGROUND_SPEED # Scrolls background
            self.draw_screen() # Update screen
        
        self.draw_screen() # End of game
        pygame.quit()


if __name__ == '__main__':
    g = Game()
    g.run_game()
