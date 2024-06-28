import pygame
from os.path import join
from random import randint
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running = True

# plain surface
surf = pygame.Surface((100, 200))

# import an image
player_surf = pygame.image.load(join("images", "player.png")).convert_alpha()
player_rect = player_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 300))
player_pos = pygame.Vector2(player_rect.center)
player_direction = pygame.Vector2()
player_speed = 300

meteor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
stars_arr = [(randint(0, WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)) for i in range(20)]

while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #     print("1")
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos
    
    # input
    keys = pygame.key.get_pressed()
    recent_keys = pygame.key.get_just_pressed()
    
    if recent_keys[pygame.K_SPACE]:
        print("laser")
    
    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    player_direction = player_direction.normalize() if player_direction.magnitude() > 0 else player_direction
    player_rect.center += player_direction * player_speed * dt
    
    
    # draw the game
    display_surface.fill('darkgray')
    
    # stars
    for star in stars_arr:
        display_surface.blit(star_surf, star)
        
    # meteors
    display_surface.blit(meteor_surf, meteor_rect)
    
    # lasers
    display_surface.blit(laser_surf, laser_rect)
    
    # player
    display_surface.blit(player_surf, player_rect)
    pygame.display.update()

pygame.quit()