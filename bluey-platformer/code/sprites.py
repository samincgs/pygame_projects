from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft= pos)
        
class Player(Sprite):
    def __init__(self, pos, groups, collision_sprites):
        surf = pygame.Surface((100, 50))
        super().__init__(pos, surf, groups)
        
        # self.import_assets()
        self.frame_index = 0
        
        # self.image = self.animations[self.frame_index]
        # self.rect = self.image.get_frect(center = pos)
        
        self.direction = pygame.Vector2()
        self.speed = 300
        
        self.collision_sprites = collision_sprites
    
    def import_assets(self):
        self.animations = []
        
        for main_folders, _, files in walk(join('images', 'player')):
            for x in files:
                surf = pygame.image.load(join(main_folders, x)).convert_alpha()
                self.animations.append(surf)
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction.magnitude() > 0 else self.direction
        
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
     
    # def animate(self, dt):
    #     self.frame_index += 7 * dt
    #     if self.frame_index >= len(self.animations):
    #         self.frame_index = 0
            
    #     self.image = self.animations[int(self.frame_index)]
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
           
    def update(self, dt):
        self.input()
        self.move(dt)
        # self.animate(dt)