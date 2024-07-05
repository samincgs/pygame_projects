import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        
        self.direction = pygame.Vector2()
        self.speed = 500
        
        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        
        
        # mask
        self.mask = pygame.mask.from_surface(self.image)
        
        
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction.magnitude() > 0 else self.direction
        
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
    
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
        self.rotated_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.time = pygame.time.get_ticks()
        
        self.direction = pygame.Vector2(uniform(-0.5, 0.5) ,1)
        self.speed = randint(300, 500)
        
        self.rotation = 0
        self.rotation_speed = randint(40, 80)
        
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.time >=4000:
            self.kill()
        
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.rotated_surf, self.rotation, 1) 
        self.rect = self.image.get_frect(center=self.rect.center)   

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
    
    def update(self, dt):
        self.frame_index += 30 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
    
def collision():
    global running
    player_collided_sprites = pygame.sprite.spritecollide(player, meteor_sprites, False)
    if player_collided_sprites:
        running = False
         
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)
        if collided_sprites:
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            laser.kill()

def display_score():
    current_time = pygame.time.get_ticks()
    text_surf = font.render(f"Score: {str(current_time // 100)}", True, (240, 240, 240))
    text_rect = text_surf.get_frect(topleft=(30, 30))
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20, 20).move(0, -5), 5, 10)
    display_surface.blit(text_surf, text_rect)
    
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True

# import images
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
laser_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()
meteor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()
explosion_frames = [pygame.image.load(join("images", "explosion", f"{i}.png" )).convert_alpha() for i in range(21)]

# import sounds
laser_sound = pygame.mixer.Sound(join())

font = pygame.font.Font(join("images", "Oxanium-Bold.ttf"), 30)

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(star_surf, all_sprites)
player = Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT/ 2 + 300), all_sprites)

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 700)

while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == meteor_event:
            Meteor(meteor_surf, (randint(0, WINDOW_WIDTH), -50), (all_sprites, meteor_sprites))
            
    # update the game
    all_sprites.update(dt)
    
    collision()
      
    # draw the game
    display_surface.fill('#3a2e3f')
    display_score()
    all_sprites.draw(display_surface)    
    pygame.display.update()
    

pygame.quit()