from colors import *
from pygame.sprite import Sprite

from functions import pil_to_pygame
from sprite_groups import *
from PIL import Image, ImageDraw, ImageFont
from parameters import fullscreen


class Cell(Sprite):
    line_width = 2
    line_color = black
    text_color = black
    fill = light_blue
    size = 50

    def __init__(self, pos, character):
        Sprite.__init__(self, all_sprites, cells_group)
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

