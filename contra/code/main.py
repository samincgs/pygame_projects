import pygame, sys
from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join
from tile import Tile
from player import Player

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Contra')
        self.clock = pygame.time.Clock()
        
        #groups
        self.all_sprites = AllSprites()
        self.setup()
    
    def setup(self):
        tmx_map = load_pygame(join('data', 'map.tmx'))
        
        # tiles
        for x,y,surf in tmx_map.get_layer_by_name('Level').tiles():
            Tile((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['main'])
        
        for layer in ['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS[layer.lower()])  
        
        
        # objects
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, join('graphics', 'player'))
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            dt = self.clock.tick() / 1000
            self.screen.fill((249, 131, 103))
            
            self.all_sprites.update(dt)
            
            self.all_sprites.custom_draw(self.player)
            pygame.display.update()

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2()
    
    def custom_draw(self, player):
        
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2
        
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.screen.blit(sprite.image, offset_rect)
           
if __name__ == '__main__':
    Main().run()