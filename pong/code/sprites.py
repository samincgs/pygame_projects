from settings import *
from random import choice, uniform


class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0, 0), (SIZE['paddle'])), 0, 5)
        self.rect = self.image.get_frect(center= POS['player'])
        self.old_rect = self.rect.copy()
        
        self.direction = 0
        
    def move(self, dt):
        self.rect.y += self.direction * self.speed * dt
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT: self.rect.bottom = WINDOW_HEIGHT     
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)    

class Player(Paddle):
    def __init__(self, groups):
       super().__init__(groups)
       
       self.speed = SPEED['player']
        
    def get_direction(self):
        keys = pygame.key.get_pressed()
        
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    
class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.rect = self.image.get_frect(center= POS['opponent'])
        self.speed = SPEED['opponent']
        self.ball = ball
    
    def get_direction(self):
        if self.ball.rect.centery > self.rect.centery: self.direction = 1
        else: self.direction = -1
                     
class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites):
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), SIZE['ball'][1] / 2) 
        self.rect = self.image.get_frect(center = POS['ball'])
        self.old_rect = self.rect.copy()
        
        self.direction = pygame.Vector2(choice((-1, 1)), choice((-1 , 1)) * uniform(0.7, 0.8) )
        self.speed = SPEED['ball']
        
        self.paddle_sprites = paddle_sprites

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1
                    

    def wall_collision(self):
        if self.rect.top <=0: 
            self.rect.top = 0
            self.direction.y *= -1
        if self.rect.bottom >= WINDOW_HEIGHT: 
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1
            
        if self.rect.left <=0: 
            self.rect.left = 0
            self.direction.x *= -1
        if self.rect.right >= WINDOW_WIDTH: 
            self.rect.right = WINDOW_WIDTH
            self.direction.x *= -1
        
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.wall_collision()
        