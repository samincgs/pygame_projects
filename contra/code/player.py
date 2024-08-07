import pygame
from settings import *
from os import walk
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos ,groups, path, collision_sprites):
        super().__init__(groups)
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'right'
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['main']
        
        self.pos = pygame.Vector2(self.rect.topleft)
        self.direction = pygame.Vector2()
        self.speed = 400
        
        # collision
        self.collision_sprites = collision_sprites
        self.old_rect = self.rect.copy()
        
        # vertical movement
        self.gravity = 15
        self.jump_speed = 1200
        self.on_floor = False
        self.duck = False
    
    def import_assets(self, path):
        self.animations = {}
        
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []        
            else:
                for file in sorted(folder[2], key= lambda name: int(name.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[2]
                    self.animations[key].append(surf)
                
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        if keys[pygame.K_UP]:
            self.direction.y = -self.speed
            
        if keys[pygame.K_DOWN]:
            self.duck = True
        else:
            self.duck = False
     
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                   if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                       self.rect.left = sprite.rect.right
                   if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                       self.rect.right = sprite.rect.left
                   self.pos.x = self.rect.x
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.y
                    self.direction.y = 0
            
    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')
        
        #gravity
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt
        self.rect.y = round(self.pos.y)
        self.collision('vertical')
       
    
    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
            
        self.image = self.animations[self.status][int(self.frame_index)]
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        
        self.input()
        self.move(dt)
        self.animate(dt)