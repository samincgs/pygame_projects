from settings import *

class UI:
    def __init__(self, monster):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.left = WINDOW_WIDTH / 2 - 100
        self.top = WINDOW_HEIGHT / 2 + 50
        self.monster = monster
        
    def general(self):
        #bg
        rect = pygame.FRect(self.left + 40, self.top + 60, 400, 200)
        pygame.draw.rect(self.display_surface, COLORS['white'],rect, 0, 4 )
        pygame.draw.rect(self.display_surface, COLORS['gray'],rect, 4, 4 )

        #menu
        cols, rows = 2, 2
        for col in range(cols):
            for row in range(rows):
                x = rect.left + rect.width / 4 + (rect.width / 2) * col
                y = rect.top + rect.height / 4 + (rect.height / 2) * row
                text_surf = self.font.render('option', True, COLORS['black'] )
                text_rect = text_surf.get_frect(center = (x, y))
                self.display_surface.blit(text_surf, text_rect)
        
    def draw(self):
        self.general()