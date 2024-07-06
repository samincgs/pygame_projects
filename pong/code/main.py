from settings import * 
from player import Player
from sprites import Ball

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.all_sprites = pygame.sprite.Group()
        
        self.player = Player(POS['player'], SIZE['paddle'], self.all_sprites)
        self.ball = Ball(SIZE['ball'], self.all_sprites)
        
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            
            self.display_surface.fill(COLORS['bg'])

            self.all_sprites.update(dt)
            
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        
        
        
        pygame.quit()
        
        
        
if __name__ == '__main__':
    
    Game().run()