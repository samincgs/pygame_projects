import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        
        self.direction = pygame.Vector2()
        self.speed = 300
        
        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction.magnitude() > 0 else self.direction
        
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            Laser(laser_surf, self.rect.midtop, all_sprites)
    
    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        self.input()
        self.move(dt)
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)
    
    def update(self, dt):
        self.rect.centery -= 500 * dt
        if self.rect.bottom <= 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.time = pygame.time.get_ticks()
        
        self.direction = pygame.Vector2(uniform(-0.5, 0.5) ,1)
        self.speed = randint(300, 500)
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.time >=4000:
            self.kill()
          
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True

star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
laser_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()
meteor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()


all_sprites = pygame.sprite.Group()
for i in range(20):
    Star(star_surf, all_sprites)
player = Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT/ 2 + 300), all_sprites)

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, (randint(0, WINDOW_WIDTH), -50), all_sprites)
            
            
       
     
    # draw the game
    all_sprites.update(dt)
    display_surface.fill('darkgray')
    
    # update the game
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()