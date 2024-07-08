from settings import *
from sprites import *
from groups import AllSprites
from support import *
from timer import Timer

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Bluey')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        
        #load game
        self.load_assets()
        self.setup()
        
        #timers
        self.bee_timer = Timer(500, func = self.create_bee, autostart = True, repeat= True)
        
    def create_bee(self):
       Bee((randint(300, 600), randint(300, 600)), self.bee_frames, self.all_sprites) 
    
    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, (x, pos[1]), direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, pos,self.all_sprites, self.player )
    
    
    def load_assets(self):
        #graphics
        self.player_frames = import_folder('images', 'player')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')
        
        #sounds
        self.audio = audio_importer('audio')
        
    
    
    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        
        for x, y, image in map.get_layer_by_name('Main').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))
            
        for x, y, image, in map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)
            
        
        Worm((700, 600), self.worm_frames, self.all_sprites)    
    
      
    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
     
            #update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()
        
        
if __name__ == '__main__':
    Game().run()