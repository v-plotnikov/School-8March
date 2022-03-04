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
word = get_word("word.txt").upper()
cell_size = min(width // (len(word)), 50)
cells = []
for i in range(len(word)):
    x = (width - len(word) * cell_size) // 2 + cell_size // 2 + i * cell_size
    y = height // 6
    cell = Cell((x, y), word[i], size=cell_size)
    cells.append(cell)


drum = Drum(open_image("./drum.png"), (width // 2, height * 3 // 5))
arrow = Arrow(open_image("./arrow.png"), (width // 2, height * 3 // 5 + drum.radius*2.4))
last_power = 0
score = 0

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
                    last_power = randint(8, 25)
                    score += last_power
                    drum.update_omega(last_power)
    text1 = get_text(f"Закрутили с силой: {last_power}", fullscreen=fullscreen)
    text2 = get_text(f"Очки: {score}", fullscreen=fullscreen)

    all_sprites.update()
    arrow.update()

    screen.fill(white)
    all_sprites.draw(screen)
    arrows_group.draw(screen)
    screen.blit(text1, (0, 0))
    screen.blit(text2, (width - text2.get_width(), 0))
    pygame.display.flip()
    clock.tick(fps)
