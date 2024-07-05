from settings import *
from player import Player


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.all_sprites = pygame.sprite.Group()
        Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), self.all_sprites)
        
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
            # update
            self.all_sprites.update(dt)
            # draw
            self.screen.fill((0,0,0))
            self.all_sprites.draw(self.screen)      
                    
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()