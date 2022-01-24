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
WIN_WIDTH = 600
WIN_HEIGHT = 700

#Screen instance
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# FPS cap
FPS = 60

# Background image
# BACKGROUND = pygame.image.load(os.path.join('Assets', 'alien_2.png'))


# Win text
YOU_WIN_IMAGE = pygame.image.load(os.path.join('Assets', 'you_win.png'))
YOU_WIN_RATIO = YOU_WIN_IMAGE.get_size()[0] / YOU_WIN_IMAGE.get_size()[1]
YOU_WIN = pygame.transform.scale(YOU_WIN_IMAGE, (WIN_WIDTH//2, (WIN_WIDTH//2) // YOU_WIN_RATIO))

# Lose text
YOU_LOSE_IMAGE = pygame.image.load(os.path.join('Assets', 'you_lose.png'))
YOU_LOSE_RATIO = YOU_LOSE_IMAGE.get_size()[0] / YOU_LOSE_IMAGE.get_size()[1]
YOU_LOSE = pygame.transform.scale(YOU_LOSE_IMAGE, (WIN_WIDTH//2, (WIN_WIDTH//2) // YOU_LOSE_RATIO))

# Sounds
EXPLOSION = pygame.mixer.Sound(os.path.join('Assets', 'brr.mp3'))

# Other settings
BACKGROUND_SPEED = 3 # px
LEVEL = 4

# Generic entity class that subclasses Rect and superclasses all objects that need a rect.
class Entity(pygame.Rect):
    def __init__(self, x, y, width, height, img_path) -> None:

        self.image = pygame.image.load(img_path)

        if width == 0 and height == 0:
            width, height = self.image.get_size()

        super.__init__(self, x, y, width, height)
        
        

class Ship(Entity):
    WIDTH, HEIGHT = 60, 60
    SPEED = 5 # px
    MAX_LASERS = 3
    LASER_DELAY = 300 # ms

    def __init__(self, x, y) -> None:
        x = x - self.WIDTH//2 # Place the center of the ship on x,y
        y = y - self.HEIGHT//2
        super.__init__(self, x, y, self.WIDTH, self.HEIGHT, os.path.join('Assets', 'ship.png'))
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.lives = 3
        self.last_laser = 0
        self.lasers = []


    # Ship movements
    def handle_keys(self, keys_pressed) -> None:
        if keys_pressed[pygame.K_LEFT]:
            self.x = max(self.x - self.SPEED, 0) # Border check left
        if keys_pressed[pygame.K_RIGHT]:
            self.x = min(self.x + self.SPEED, WIN_WIDTH - self.WIDTH) # border check right
        if keys_pressed[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.last_laser > self.LASER_DELAY:
                self.shoot_laser()
                self.last_laser = pygame.time.get_ticks()

    # Ship Firing function
    def shoot_laser(self) -> None: # Will not shoot more than 3 lasers at a time, one at a second
        if len(self.lasers) >= self.MAX_LASERS:
            return
        else:
            l = Laser(self.x + self.WIDTH//2, self.y) # Middle-top of the ship
            self.lasers.append(l)


class Laser(Entity):
    WIDTH, HEIGHT = 20, 60
    SPEED = 5 # px

    def __init__(self, x, y) -> None:
        x = x - self.WIDTH//2 # center laser on center ship,
        y = y + self.HEIGHT # bottom of laser on top of ship
        super.__init__(self, x, y, self.WIDTH, self.HEIGHT, os.path.join('Assets', 'ship_laser.png'))
        self.image =  pygame.transform.rotate(pygame.transform.scale(self.image, 
                        (self.HEIGHT, self.WIDTH)), 90) # Width and Height are switched because of the rotation
        pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join('Assets', 'laser.mp3')))

    @classmethod
    def movement(cls, ship, aliens):

        for l in ship.lasers: # Out of bounds
            if l.y + cls.HEIGHT == 0:
                ship.lasers.remove(l)
                continue

            for a in aliens: # Hits alien
                if l.colliderect(a):
                    aliens.remove(a)
                    ship.lasers.remove(l)
                    pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join('Assets', 'brr.mp3')))
                    continue

            l.y -= cls.SPEED # Laser progression


class Alien(Entity):
    WIDTH, HEIGHT = 40, 30
    PADDING = int(1.5 * WIDTH) # px
    MIN_BULLET_WAIT = 800 #ms
    MAX_BULLET_WAIT = 2000 #ms
    INITIAL_SPEED = 800 #ms

    def __init__(self, x, y) -> None:
        super.__init__(self, x, y, self.WIDTH, self.HEIGHT, os.path.join('Assets', 'alien.png'))
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))
        self.last_move = 0
        self.last_bullet = 0
        self.bullet_timer = random.randint(self.MIN_BULLET_WAIT, self.MAX_BULLET_WAIT)
        self.bullets = []
        self.speed = self.INITIAL_SPEED
        self.step = self.WIDTH//2

    # Alien bullet firing function
    def fire_bullet(self) -> None:
        b = Bullet(self.x + self.WIDTH//2, self.y) # Center-bottom of the alien
        Alien.add_bullet(b)

    # Aliens initial setup
    @classmethod
    def place_aliens(cls, nb_lines) -> list:
        aliens = []
        aliens_per_line = WIN_WIDTH//(cls.WIDTH + cls.PADDING) - 1
        for line in range(nb_lines):
            for col in range(aliens_per_line):
                aliens.append(Alien(col * (cls.PADDING + cls.WIDTH),
                WIN_HEIGHT//4 - line * (cls.HEIGHT + cls.PADDING)))

        return aliens

    # Alien movements
    @classmethod
    def movement(cls, aliens, ship) -> None:
        if pygame.time.get_ticks() - cls.last_move > cls.speed:
            
            for a in aliens: # Alien touches the ship = end of game
                if a.colliderect(ship):
                    ship.lives = 0
                    continue
            # Last alien decides of the bounce on screen border
            if max(map(lambda x: x.x, aliens)) + cls.WIDTH + cls.STEP > WIN_WIDTH:
                cls.step *= -1
                cls.speed = max(cls.INITIAL_SPEED//10, cls.speed - cls.INITIAL_SPEED//10)
                for alien in aliens:
                    alien.y += cls.step
            elif min(map(lambda x: x.x, aliens)) + cls.step < 0:
                cls.step *= -1
                cls.speed = max(cls.INITIAL_SPEED//10, cls.speed - cls.INITIAL_SPEED//10)
                for alien in aliens:
                    alien.y += cls.step
            else:
                for alien in aliens:
                    alien.x += cls.step
            cls.last_move = pygame.time.get_ticks()
    
    # At a random time, random alien fires bullet -> will go in game class
    @classmethod
    def try_fire(cls, aliens) -> None:
        if pygame.time.get_ticks() > cls.last_bullet + cls.bullet_timer:
            aliens[random.randint(0, len(aliens) - 1)].fire_bullet()
            cls.last_bullet = pygame.time.get_ticks()
            cls.bullet_timer = random.randint(cls.MIN_BULLET_WAIT, cls.MAX_BULLET_WAIT)


class Bullet():
    WIDTH, HEIGHT = 20, 30
    SPEED = 5 #px

    def __init__(self, x, y):
        x = x + self.WIDTH//2 # Center bullet on center ship
        super.__init__(self, x, y, self.WIDTH, self.HEIGHT, os.path.join('Assets', 'alien_bullet.png'))
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))

    @classmethod
    def movement(self, ship, aliens) -> None:
        for a in aliens:
            for b in a.bullets:
                if b.colliderect(ship):
                    ship.lives -= 1
                    a.bullets.remove(b)

            b.y += self.SPEED


class Background(Entity):
    def __init__(self) -> None:
        super.__init__(self, 0, 0, 0, 0, os.path.join('Assets', 'background.jpg'))
        self.image = pygame.transform.rotate(self.image, 90)
        self.WIDTH, self.HEIGHT = self.image.get_size()
        self.x, self.y = (-(self.WIDTH - WIN_WIDTH)//2, -(self.HEIGHT - WIN_HEIGHT)//2)

class Game():
    # Window Setup
    def __init__(self):
        pygame.display.set_caption('Vace Inspaders')
        pygame.display.set_icon(os.path.join('Assets', 'ship.png'))
        pygame.mixer.init()
        pygame.font.init()
        self.TXT_FONT = pygame.font.SysFont('Times New Romans', 25)
        self.clock = pygame.time.Clock()
        self.ship = Ship(WIN_WIDTH//2, WIN_HEIGHT - 20) # center, center.
        self.aliens = Alien.place_aliens(LEVEL)
        self.background = Background()
        self.end_state = ''


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
            self.WIN.blit(YOU_WIN, ((WIN_WIDTH - YOU_WIN.get_width())//2, (WIN_HEIGHT - YOU_WIN.get_height())//2))
        elif self.end_state == 'lose':
            self.WIN.blit(YOU_LOSE, ((WIN_WIDTH - YOU_LOSE.get_width())//2, (WIN_HEIGHT - YOU_LOSE.get_height())//2))

        pygame.display.update()

        if self.end_state == 'win' or self.end_state == 'lose':
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        wait = False


    def run_game(self):

        running = True
        while running:
            self.clock.tick(FPS)
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

            self.ship.handle_keys(keys_pressed)

            Laser.movement(self.ship, self.aliens)

            if len(self.aliens) == 0: # See how to exit
                pass

            Alien.movement(self.aliens, self.ship)

            Alien.try_fire(self.aliens)

            Bullet.bullet_movements(self.ship, self.aliens)

            if self.ship.lives == 0: # See how to exit
                    pass
            
            if self.end_state == 'lose':
                continue

            self.background.y += BACKGROUND_SPEED # Scrolls background
            self.draw_screen() # Update screen
        
        self.draw_screen() # End of game
        pygame.quit()


if __name__ == '__main__':
    g = Game()
    g.run_game()
