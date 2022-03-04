import sys
from random import randint

import pygame
from parameters import *
from functions import *
from sprites import *
from sprite_groups import *

pygame.init()

screen = get_screen(fullscreen)
pygame.display.set_caption(title)
clock = pygame.time.Clock()

cells = [Cell((width // 2 - 100, height // 2), "А"), Cell((width // 2 + 100, height // 2), "Б")]
drum = Drum(open_image("./drum.png"), (width // 4, height // 2))
arrow = Arrow(open_image("./arrow.png"), (width // 4, height // 2 + drum.radius*2.4))
last_power = 0

text1 = get_text(f"Последняя сила удара: {last_power}")

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
                drum.scale(fullscreen)
                arrow.scale(fullscreen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for cell in cells:
                    if 0 <= distance(event.pos, cell.rect.center) <= cell.size // 2:
                        cell.opened = not cell.opened
                        break
                if 0 <= distance(event.pos, drum.rect.center) <= drum.radius:
                    drum.last_click = time.time()
                    last_power = randint(15, 25)
                    drum.update_omega(last_power)

    all_sprites.update()
    arrow.update()

    screen.fill(white)
    all_sprites.draw(screen)
    arrows_group.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
