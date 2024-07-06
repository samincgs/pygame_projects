from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill(COLORS['paddle'])
        self.rect = self.image.get_frect(center= pos)
        
        self.direction = 0
        self.speed = SPEED['player']
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    
    def move(self, dt):
        self.rect.y += self.direction * self.speed * dt
    
    def collision(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
    
    def update(self, dt):
        self.input()
        self.move(dt)      
        self.collision()  
        
