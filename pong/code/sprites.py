from settings import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill(COLORS['ball'])
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/ 2, WINDOW_HEIGHT/ 2))
        
        self.direction = pygame.Vector2(1, 1)
        self.speed = SPEED['ball']
        
    def wall_collision(self):
        if self.rect.bottom > WINDOW_HEIGHT or self.rect.top < 0:
            self.direction.y *= -1
        if self.rect.right > WINDOW_WIDTH or self.rect.left < 0:
            self.direction.x *= -1
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        
        self.wall_collision()