from settings import *
from player import Player
from sprites import *
from groups import AllSprites
from random import randint
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 200
        
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        
        self.load_images()
        self.setup()
        
        # sprites
        
        # for _ in range(5):
        #     x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
        #     w,h = randint(50, 150), randint(50, 100)
        #     CollisionSprites((x, y), (w,h), (self.all_sprites, self.collision_sprites))
    
    def input(self):
        mouse = pygame.mouse.get_pressed()
        
        if mouse[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
    
       
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
    
    
    def setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprites((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
       
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprites((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
       
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites) 
                self.gun = Gun(self.player, self.all_sprites)  
       
 
    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
            # update
            self.input()
            self.gun_timer()
            self.all_sprites.update(dt)
            
            # draw
            self.display_surface.fill((0,0,0))
            self.all_sprites.draw(self.player.rect.center)      
                    
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()