from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player", "down", "0.png" )).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        
        self.direction = pygame.Vector2()
        self.speed = 400
        
    def move(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction.magnitude() > 0 else self.direction
        
    def update(self, dt):
        self.move()
        
        self.rect.center += self.direction * self.speed * dt