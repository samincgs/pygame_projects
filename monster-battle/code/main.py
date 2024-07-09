from settings import *
from support import *
from monster import *

class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()
        self.running = True
        self.import_assets()
        
        #groups
        self.all_sprites = pygame.sprite.Group()
        
        #data #player
        player_monster_list = ['Sparchu', 'Cleaf', 'Jacana']
        self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monster_list]
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        
        #opponent
        opponent_name = choice(list(MONSTER_DATA.keys()))
        self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.all_sprites)
    
    
    def import_assets(self):
        self.back_surfs = folder_importer('images', 'back')
        self.front_surfs = folder_importer('images', 'front')
        self.bg_surfs = folder_importer('images', 'other')
       
        
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            
            #update
            self.all_sprites.update(dt)
            
            #draw
            self.display_surface.blit(self.bg_surfs['bg'], (0, 0))
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
            
            
        pygame.quit()
        
        
        
        
if __name__ == '__main__':
    Game().run()
    
    
    