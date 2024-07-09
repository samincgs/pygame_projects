from settings import *
from timer import Timer
from math import sin

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft= pos)

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 10
        surf = self.frames[self.frame_index]
        super().__init__(pos, surf, groups)
        
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

class Bullet(Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(pos, surf, groups)
        
        #adjustment
        self.image = pygame.transform.flip(self.image, direction == -1, False)
        
        # movement
        self.direction = direction
        self.speed = 850
    
    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

class Fire(Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(100, autostart = True, func = self.kill)
        self.y_offset = pygame.Vector2(0, 8)
        
        if self.flip:
            self.rect.midright = self.player.rect.midleft  + self.y_offset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset
    
    def update(self, _):
        self.timer.update()
        
        if self.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset
            
        if self.flip != self.player.flip:
            self.kill()    

class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames, create_bullet):
        super().__init__(pos, frames, groups)
        
        # movement
        self.direction = pygame.Vector2()
        self.speed = 300
        self.gravity = 50
        self.on_floor = False
        
        self.shoot_timer = Timer(500)
        
        self.flip = False
        self.collision_sprites = collision_sprites
        
        self.create_bullet = create_bullet
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -20
        if keys[pygame.K_s] and not self.shoot_timer:
            self.create_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()
        
             
    def move(self, dt):
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        #vertical
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision('vertical')
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
    
    def check_floor(self):
       bottom_rect = pygame.FRect((0, 0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
       level_rects = [sprite.rect for sprite in self.collision_sprites]
       self.on_floor = True if bottom_rect.collidelist(level_rects) >= 0 else False

    def animate(self, dt):
        if self.direction.x: 
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0    
        else: self.frame_index = 0
        
        if not self.on_floor: self.frame_index = 1
        
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.flip(self.image, self.flip, False)
  
    def update(self, dt):
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)

class Enemy(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.death_timer = Timer(200, func = self.kill)
    
    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey((0, 0, 0))
    
    def update(self, dt):
        self.death_timer.update()
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
        self.constraint()

class Bee(Enemy):
    def __init__(self, pos, frames, speed, groups):
        super().__init__(pos, frames, groups)
        self.speed = speed
        self.amplitude = randint(500, 600)
        self.frequency = randint(300, 600)
    
    def move(self, dt):
        self.rect.x -=  self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt
    
    def constraint(self):
        if self.rect.right <= 0: self.kill()
        
class Worm(Enemy):
    def __init__(self, rect, frames, groups):
        super().__init__(rect.topleft, frames, groups)
        self.main_rect = rect
        self.rect.bottomleft = rect.bottomleft
        self.speed = randint(160, 200)
        self.direction = 1
    
    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt
    
    def constraint(self):
        if not self.main_rect.contains(self.rect):
            self.direction *= -1
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]
            
    