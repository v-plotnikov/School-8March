import importlib
import math
import os

from pygame import FULLSCREEN
from pygame.display import set_mode
from pygame.image import fromstring
from PIL import Image, ImageDraw, ImageFont

from parameters import monitor


def import_module(path: str, name: str = "module"):
    spec = importlib.util.spec_from_file_location(name, path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


def pil_to_pygame(img):
    mode = img.mode
    size = img.size
    data = img.tobytes()
    py_image = fromstring(data, size, mode)
    return py_image


def get_text(text, font_size=30, color=(0, 0, 0, 255), align="center", anchor="mm", pos=None):
    text = str(text)
    img_size = 345, round(font_size * 1.2)
    im = Image.new('RGBA', img_size, color=(255, 255, 255, 150))
    font = ImageFont.truetype('./RobotoMono-LightItalic.ttf', size=font_size)
    drawer = ImageDraw.Draw(im)
    if pos is None:
        pos = img_size[0] // 2, img_size[1] // 2
    else:
        pos = pos, img_size[1] // 2
    drawer.text(pos, text, fill=color, font=font, align=align, anchor=anchor)

    return pil_to_pygame(im)


def get_screen(fullscreen=False):
    if fullscreen:
        size = monitor
        pos = 0, 0
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{pos[0]},{pos[1]}"
        os.environ['SDL_VIDEO_CENTERED'] = '0'
        screen = set_mode(size, FULLSCREEN)
    else:
        size = monitor[0] // 2, monitor[1] // 2
        pos = size
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{pos[0]},{pos[1]}"
        os.environ["SDL_VIDEO_CENTERED"] = "0"
        screen = set_mode(size)
    return screen


def open_image(path):
    return Image.open(path)


def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def to_degrees(radians):
    return radians * 180 / math.pi
