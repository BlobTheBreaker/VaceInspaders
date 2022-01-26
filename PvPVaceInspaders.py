# Custom made Space Invader type game

"""
TO DO LIST:

OOP Version:

x Make everything OOP...
"""

from html import entities
import pygame
import os
import random

# Screen size
WIN_WIDTH = 600
WIN_HEIGHT = 700

#Screen instance
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


# Generic entity class that subclasses Rect and superclasses all objects that need a rect.
class Entity(pygame.Rect):
    def __init__(self, x, y, width, height, img_path) -> None:
        self.image = pygame.image.load(img_path)
        if width == 0 and height == 0:
            height, width = self.image.get_size()
        super().__init__(x, y, width, height)


    def draw(self):
        WIN.blit(self.image, self.topleft)


    def to_str(self):
        return '{}, {}, {}, {}, '.format(self.x, self.y, self.width, self.height)


class Ship(Entity):
    SPEED = 5 # px


    def __init__(self, x, y) -> None:
        super().__init__(x, y, 60, 60, os.path.join('Assets', 'ship.png'))
        self.center = self.x, self.y
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.lives = 3
        self.last_laser = 0
        self.lasers = []


    # Ship movements
    def handle_keys(self, keys_pressed) -> None:
        if keys_pressed[pygame.K_LEFT]:
            self.left = max(self.left - self.SPEED, 0) # Border check left
        if keys_pressed[pygame.K_RIGHT]:
            self.right = min(self.right + self.SPEED, WIN_WIDTH) # border check right
        if keys_pressed[pygame.K_SPACE]:
            if (pygame.time.get_ticks() - self.last_laser > 300 
            and len(self.lasers) <= 3): # laser delay between shots in ms and maximum laser entities alive
                self.shoot_laser()
                self.last_laser = pygame.time.get_ticks() 


    # Ship Firing function
    def shoot_laser(self) -> None:
        l = Laser(self.centerx, self.y) # Middle-top of the ship
        self.lasers.append(l)


class Laser(Entity):
    SPEED = 5 # px


    def __init__(self, x, y) -> None:
        super().__init__(x, y, 20, 60, os.path.join('Assets', 'ship_laser.png'))
        self.centerx = self.x
        self.bottom = self.y
        self.image =  pygame.transform.scale(pygame.transform.rotate(self.image, 90),
                      (self.width, self.height)) 
        pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join('Assets', 'laser.mp3')))

    @classmethod
    def movement(cls, ship, aliens):
        for l in ship.lasers: # Out of bounds
            if l.bottom == 0:
                ship.lasers.remove(l)
                continue
            for a in aliens: # Hits alien
                if l.colliderect(a):
                    aliens.remove(a)
                    ship.lasers.remove(l)
                    pygame.mixer.Sound.play(pygame.mixer.Sound(os.path.join('Assets', 'brr.mp3')))
                    continue
            l.y -= cls.SPEED # Laser progression


class Ennemy(Entity):
    def __init__(self, x, y, width, height, img_path) -> None:
        super().__init__(x, y, width, height, img_path)
        self.center = self.x, self.y

class Alien(Entity):
    #I need to fix those. Most are here because my classmethods access them...
    WIDTH, HEIGHT = 40, 30
    MIN_BULLET_WAIT = 800 # ms
    MAX_BULLET_WAIT = 2000 # ms
    INITIAL_SPEED = 800 # ms
    PADDING = 60 # px (or 1.5 x width)
    last_move = 0
    speed = INITIAL_SPEED
    step = 20 # px
    last_bullet = 0
    bullet_timer = random.randint(MIN_BULLET_WAIT, MAX_BULLET_WAIT)

    def __init__(self, x, y) -> None:
        super().__init__(x, y, self.WIDTH, self.HEIGHT, os.path.join('Assets', 'alien.png'))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.bullets = []
        
         

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
            if max(map(lambda x: x.right, aliens)) + cls.step > WIN_WIDTH:
                cls.step *= -1
                cls.speed = max(cls.INITIAL_SPEED//10, cls.speed - cls.INITIAL_SPEED//10)
                for alien in aliens:
                    alien.y += abs(cls.step)
            elif min(map(lambda x: x.left, aliens)) + cls.step < 0:
                cls.step *= -1
                cls.speed = max(cls.INITIAL_SPEED//10, cls.speed - cls.INITIAL_SPEED//10)
                for alien in aliens:
                    alien.y += abs(cls.step)
            else:
                for alien in aliens:
                    alien.x += cls.step
            cls.last_move = pygame.time.get_ticks()
            
    
    # At a random time, random alien fires bullet
    @classmethod
    def try_fire(cls, aliens) -> None:
        if pygame.time.get_ticks() > cls.last_bullet + cls.bullet_timer:
            aliens[random.randint(0, len(aliens) - 1)].fire_bullet()
            cls.last_bullet = pygame.time.get_ticks()
            cls.bullet_timer = random.randint(cls.MIN_BULLET_WAIT, cls.MAX_BULLET_WAIT)

    
    # Alien bullet firing function
    def fire_bullet(self) -> None:
            b = Bullet(self.centerx, self.y) # Center-bottom of the alien
            self.bullets.append(b)


class Bullet(Entity):
    WIDTH, HEIGHT = 20, 30
    SPEED = 5 #px


    def __init__(self, x, y):
        x = x + self.WIDTH//2 # Center bullet on center ship
        super().__init__(x, y, self.WIDTH, self.HEIGHT, os.path.join('Assets', 'alien_bullet.png'))
        self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))


    @classmethod
    def movement(self, ship, aliens) -> None:
        for a in aliens:
            for b in a.bullets:
                if b.colliderect(ship):
                    ship.lives -= 1
                    a.bullets.remove(b)
                b.y += self.SPEED

    
    def draw(self):
        WIN.blit(self.image, self.topleft)


class Background(Entity):
    SPEED = 3 # px

    def __init__(self) -> None:
        super().__init__(0, 0, 0, 0, os.path.join('Assets', 'background.jpg'))
        self.image = pygame.transform.rotate(self.image, 90)
        self.WIDTH, self.HEIGHT = self.image.get_size()
        self.center = (WIN_WIDTH//2, WIN_HEIGHT//2)


    def movement(self):
        self.y += self.SPEED


    def draw(self):
        WIN.blit(self.image, (self.x, self.y % self.HEIGHT))
        WIN.blit(self.image, (self.x, (self.y % self.HEIGHT) - self.HEIGHT))

class Game():
    # FPS cap
    FPS = 60
    LEVEL = 4

    def __init__(self):
        pygame.mixer.init()
        pygame.font.init()
        self.TXT_FONT = pygame.font.SysFont('Times New Romans', 25)
        self.clock = pygame.time.Clock()
        self.ship = Ship(WIN_WIDTH//2, WIN_HEIGHT - 20) # center, center.
        self.aliens = Alien.place_aliens(self.LEVEL) #
        self.background = Background()
        self.ennemy = Ennemy(WIN_WIDTH//2, 20)
        self.game_state = 'running'
        pygame.display.set_caption('Vace Inspaders')
        pygame.display.set_icon(self.ship.image)


    def pack_data(self):
        data_str = ''
        for ent in self.local_entities:
            if type(ent) == list:
                for obj in ent:
                    data_str += obj.to_str() + ','
            else:
                data_str += obj.to_str() + ','

        return data_str

    def unpack_data(self, data_str):
        data = data_str.split(',')
        for ent in self.ennemy_entities:
            ent.x, ent.y = data
            


    
    def unpack_data(self):
        pass


    # Screen updating function
    def draw_screen(self):
        for ent in self.entities:
            if type(ent) == list:
                for obj in ent:
                    obj.draw()
            else:
                ent.draw()
        self.lives_display = self.TXT_FONT.render('LIVES: ' + str(self.ship.lives), False, (255, 255, 255))
        WIN.blit(self.lives_display, (10, 10))
        pygame.display.update()


    def draw_end(self):
        if self.game_state == 'win':
            # Win text
            YOU_WIN_IMAGE = pygame.image.load(os.path.join('Assets', 'you_win.png'))
            YOU_WIN_RATIO = YOU_WIN_IMAGE.get_size()[0] / YOU_WIN_IMAGE.get_size()[1]
            YOU_WIN = pygame.transform.scale(YOU_WIN_IMAGE, (WIN_WIDTH//2, (WIN_WIDTH//2) // YOU_WIN_RATIO))
            WIN.blit(YOU_WIN, ((WIN_WIDTH - YOU_WIN.get_width())//2, (WIN_HEIGHT - YOU_WIN.get_height())//2))
        elif self.game_state == 'lose':
            # Lose text
            YOU_LOSE_IMAGE = pygame.image.load(os.path.join('Assets', 'you_lose.png'))
            YOU_LOSE_RATIO = YOU_LOSE_IMAGE.get_size()[0] / YOU_LOSE_IMAGE.get_size()[1]
            YOU_LOSE = pygame.transform.scale(YOU_LOSE_IMAGE, (WIN_WIDTH//2, (WIN_WIDTH//2) // YOU_LOSE_RATIO))
            WIN.blit(YOU_LOSE, ((WIN_WIDTH - YOU_LOSE.get_width())//2, (WIN_HEIGHT - YOU_LOSE.get_height())//2))
  
        pygame.display.update()
        print('wait')
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False


    def run_game(self):

        while self.game_state == 'running':
            self.clock.tick(self.FPS)
            # Exit Condition
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = ''
                    pygame.quit()

            self.background.movement()

            keys_pressed = pygame.key.get_pressed() 

            self.ship.handle_keys(keys_pressed) # Read ship commands

            Laser.movement(self.ship, self.aliens) # Laser deletion, hit detection and movement

            if len(self.aliens) == 0:
                self.game_state = 'win'
                continue

            Alien.movement(self.aliens, self.ship) # Aliens movements

            Alien.try_fire(self.aliens)

            Bullet.movement(self.ship, self.aliens)

            if self.ship.lives <= 0: # See how to exit
                self.game_state = 'lose'
                continue

            # Update entities list
            self.entities = [self.background, self.ship, self.aliens,
                        self.ship.lasers]
            self.entities +=  map(lambda x:x.bullets, self.aliens)
            self.draw_screen() # Update screen
        
        self.draw_end()
        pygame.quit()


if __name__ == '__main__':
    g = Game()
    
    # Connection to the server
    player_id = g.n.connect()

    print('waiting for other player...')
    while True:
        ready = g.n.send('ready')
        if ready == 'ready':
            break

    g.run_game()
