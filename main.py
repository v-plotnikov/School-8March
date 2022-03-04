import sys
import pygame
import os

from colors import *
from parameters import *
from functions import *
from sprites import *
from sprite_groups import *

pygame.init()

screen = get_screen(fullscreen)
pygame.display.set_caption(title)
clock = pygame.time.Clock()

cells = [Cell((width // 2 - 100, height // 2), "А"), Cell((width // 2 + 100, height // 2), "Б")]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                fullscreen = not fullscreen
                screen = get_screen(fullscreen)
                if fullscreen:
                    size = width, height = monitor[0], monitor[1]
                else:
                    size = width, height = monitor[0] // 2, monitor[1] // 2
                for cell in cells:
                    cell.scale(fullscreen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for cell in cells:
                    if 0 <= distance(event.pos, cell.rect.center) <= cell.size // 2:
                        cell.opened = not cell.opened
                        break

    all_sprites.update()

    screen.fill(white)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
