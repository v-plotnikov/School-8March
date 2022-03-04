import time

from colors import *
from pygame.sprite import Sprite

from functions import pil_to_pygame, to_degrees
from sprite_groups import *
from PIL import Image, ImageDraw, ImageFont
from parameters import fullscreen


class Cell(Sprite):
    line_width = 2
    line_color = black
    text_color = black
    fill = light_blue

    def __init__(self, pos, character, size=50):
        Sprite.__init__(self, all_sprites, cells_group)
        self.size = size
        self.pos = pos[0] - self.size // 2, pos[1] - self.size // 2
        self.character = character
        self.opened = False
        self.image = self.create_display()
        self.rect = self.image.get_rect()

    def new_pos(self, x, y):
        self.pos = x, y

    def scale(self, fullscreen=fullscreen):
        k = 0.5
        if fullscreen:
            k = 2
        self.pos = self.pos[0] * k, self.pos[1] * k
        self.size = int(self.size * k)

    def update(self):
        self.image = self.create_display()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def create_display(self):
        image = Image.new("RGBA", (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('./RobotoMono-LightItalic.ttf', size=int(self.size / 1.2))
        rect = (0, 0, self.size - self.line_width, self.size - self.line_width)
        if not self.opened:
            draw.rectangle(rect, fill=self.fill, outline=self.line_color, width=self.line_width)
        else:
            text_pos = (self.size // 2, self.size // 2)
            draw.rectangle(rect, fill=(0, 0, 0, 0), outline=self.line_color, width=self.line_width)
            draw.text(text_pos, self.character, fill=self.text_color, font=font, align="center", anchor="mm")
        return pil_to_pygame(image)


class Drum(Sprite):
    radius = 150
    torsion_braking = 0.25

    def __init__(self, pil_image: Image, pos):
        Sprite.__init__(self, all_sprites, drums_group)
        self.pil_image = pil_image
        self.pos = pos[0] - self.radius, pos[1] - self.radius
        self.cumulative_angle = 10
        self.omega = 0

        self.image = self.spin_image()
        self.rect = self.image.get_rect()
        self.last_click = 0

    def update_omega(self, value=0):
        k = 1
        if self.omega <= 0:
            self.omega = value
            return
        if 0 < self.omega <= 1:
            k = 0.05
        if 2 < self.omega <= 3:
            k = 0.25
        self.omega -= self.torsion_braking * k

    def spin_image(self):
        image = self.pil_image.rotate(to_degrees(self.cumulative_angle))
        image = image.resize((self.radius * 2, self.radius * 2))
        return pil_to_pygame(image)

    def scale(self, fullscreen=fullscreen):
        k = 0.5
        if fullscreen:
            k = 2
        self.pos = self.pos[0] * k, self.pos[1] * k
        self.radius = int(self.radius * k)

    def update(self):
        self.update_omega()
        self.cumulative_angle += self.omega / (time.time() - self.last_click)
        self.image = self.spin_image()

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Arrow(Sprite):
    size = 40

    def __init__(self, pil_image: Image, pos):
        Sprite.__init__(self, arrows_group)
        self.pil_image = pil_image.resize((self.size, self.size))
        self.image = pil_to_pygame(self.pil_image)
        self.pos = pos[0] - self.size // 2, pos[1] - (6 - (3 ** 0.5 / 6)) * self.size

        self.rect = self.image.get_rect()
        self.last_click = 0

    def scale(self, fullscreen=fullscreen):
        k = 0.5
        if fullscreen:
            k = 2
        self.pos = self.pos[0] * k, self.pos[1] * k
        self.size = int(self.size * k)

    def update(self):
        self.image = pil_to_pygame(self.pil_image.resize((self.size, self.size)))
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1] # + 535

