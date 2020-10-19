import pygame
import sys

import time

def key():
    SCREEN_WIDTH = 720
    SCREEN_HEIGHT = 580

    red = (255, 0, 0)
    
    pygame.init()
    pygame.display.set_caption("map")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #image
    map = pygame.image.load("/home/pi/Desktop/map.png").convert()

    pos_x = 200
    pos_y = 200

    clock = pygame.time.Clock()
    

    while True:
        clock.tick(15)#spot speed
        key_event = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if key_event[pygame.K_ESCAPE]:
                pygame.quit()
                #sys.exit()
                
        #key_event = pygame.key.get_pressed()
        if key_event[pygame.K_LEFT]:
            pos_x -= 1

        if key_event[pygame.K_RIGHT]:
            pos_x += 1

        if key_event[pygame.K_UP]:
            pos_y -= 1

        if key_event[pygame.K_DOWN]:
            pos_y += 1

        #screen.fill(black)
        screen.blit(map , (0,0))
        pygame.draw.circle(screen, red, (pos_x, pos_y), 11)
        pygame.display.update()

    #return 0
