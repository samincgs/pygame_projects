from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        
        self.load_images()
        self.frame_index = 0
        self.status = 'down'
        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -60)
        
        self.direction = pygame.Vector2()
        self.speed = 600
        self.collision_sprites = collision_sprites
        
    
    def load_images(self):
        self.frames = {'down': [], 'up' : [], 'left': [], 'right': []}
      
        for i in self.frames.keys():  
            for _, _, files in walk(join("images", "player", i)):
                for file in sorted(files, key=lambda x: int(x.split('.')[0]) ):
                    path = join("images", "player", i, file)
                    surf = pygame.image.load(path).convert_alpha()
                    self.frames[i].append(surf)
            
    def animate(self, dt):
        
        if self.direction.x != 0:
            self.status = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y !=0:
            self.status = 'down' if self.direction.y > 0 else 'up'
        
        self.frame_index = self.frame_index + 7 * dt if self.direction.magnitude() > 0 else 0
        if self.frame_index >= len(self.frames[self.status]):
            self.frame_index = 0
            
        self.image = self.frames[self.status][int(self.frame_index)]
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction.magnitude() > 0 else self.direction
        
    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
    
    def update(self, dt):
        self.input()
        self.animate(dt)
        self.move(dt)
        
        