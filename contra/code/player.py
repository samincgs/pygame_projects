import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos ,groups):
        super().__init__(groups)
        self.image = pygame.Surface((40, 80))
        self.rect = self.image.get_rect(topleft = pos)
        
        self.pos = pygame.Vector2(self.rect.topleft)
        self.direction = pygame.Vector2()
        self.speed = 400
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
            
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
            
    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
    def update(self, dt):
        self.input()
        self.move(dt)