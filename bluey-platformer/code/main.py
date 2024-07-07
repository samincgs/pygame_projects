from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Bluey')
        self.clock = pygame.time.Clock()
        self.running = True
    
    def setup():
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        
        for x, y, image in map.get_layer_by_name('Main').tiles():
            pass
    
      
    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.display_surface.fill(BG_COLOR)
            
            pygame.display.update()
        
        pygame.quit()
        
        
if __name__ == '__main__':
    Game().run()