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
        self.enemy_sprites = pygame.sprite.Group()
        
        #load game
        self.load_assets()
        self.setup()
        
        #timers
        self.bee_timer = Timer(1200, func = self.create_bee, autostart = True, repeat= True)
        
    def create_bee(self):
       Bee((self.level_width + WINDOW_WIDTH, randint(0, self.level_height)), self.bee_frames, randint(300, 500) , (self.all_sprites, self.enemy_sprites)) 
    
    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, (x, pos[1]), direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, pos,self.all_sprites, self.player)
        self.audio['shoot'].play()
    
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
        self.level_width = map.width * TILE_SIZE
        self.level_height = map.height * TILE_SIZE
        
        for x, y, image in map.get_layer_by_name('Main').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))
            
        for x, y, image, in map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)
            if obj.name == 'Worm':
                Worm(pygame.FRect(obj.x, obj.y, obj.width, obj.height), self.worm_frames, (self.all_sprites, self.enemy_sprites))  
        
        self.audio['music'].play(loops = -1)
        
    def collision(self):
        # bullets and enemies
        for bullet in self.bullet_sprites:
            sprite_collisions = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collisions:
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collisions:
                    sprite.destroy()
                    
        # player and enemies
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False
                  
    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
     
            #update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()
            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()
        
        
if __name__ == '__main__':
    Game().run()