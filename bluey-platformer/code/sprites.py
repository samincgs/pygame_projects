from settings import *

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
    
class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames):
        super().__init__(pos, frames, groups)
        
        self.direction = pygame.Vector2()
        self.speed = 300
        self.gravity = 50
        self.on_floor = False
        
        self.flip = False
        self.collision_sprites = collision_sprites
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -20
             
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
        
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.flip(self.image, self.flip, False)
  
    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)