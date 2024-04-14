import math
import operator
import os
import time
from enum import Enum
from functools import reduce
import io
import asyncio
from os.path import isfile, join

from PIL.Image import Resampling
from PIL import Image
from io import BytesIO
import base64

from dotenv import load_dotenv

load_dotenv()

URL = os.getenv('URL')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BUCKET = os.getenv('BUCKET')


async def image_difference(img1, img2):
    h1 = img1.histogram()
    h2 = img2.histogram()
    return math.sqrt(reduce(operator.add,
                            map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))


class MethodFragmentation(Enum):
    crop = 0
    cross = 1


class ImageCrops:
    def __init__(self, image, levels=3, window_size=5):
        self.levels = levels
        self.window_size = window_size
        self.fragments = self.get_fragments(image)

    def cross_fragment(self, image, center):
        x, y = center
        delta = self.window_size // 2 + 1
        result = [image.getpixel((x, y))[:3]]
        for i in range(1, delta):
            result.append(image.getpixel((x - i, y - i))[:3])  # 6➡...
            result.append(image.getpixel((x + i, y - i))[:3])  #  2➡3
            result.append(image.getpixel((x + i, y + i))[:3])  #  ⬆1 ⬇
            result.append(image.getpixel((x - i, y + i))[:3])  #  5⬅4
        return result

    def get_fragments(self, image):
        fragments = []
        img_width, img_height = image.size
        delta = int((((img_width + img_height) * 2 ** .5) / 8 - self.window_size * (.5 + self.levels - 1)) / max(
            (self.levels - 1), 1))

        center_x, center_y = img_width // 2, img_height // 2
        for i in range(-((self.levels * 2 - 1) // 2), (self.levels * 2 - 1) // 2 + 1):
            for j in range(-((self.levels * 2 - 1) // 2), (self.levels * 2 - 1) // 2 + 1):
                fragments.append(self.cross_fragment(image, (center_x + i * (self.window_size + delta), center_y + j * (self.window_size + delta))))
        return fragments

    def diff(self, other):
        diff_fragment = lambda f1, f2: sum(
            [sum([(f1[i][j] - f2[i][j]) ** 2 for j in range(3)]) / 3 for i in range(len(f1))]) / len(f1)
        if len(self.fragments) != len(other.fragments):
            raise Exception("difference len() fragments")
        result = sum([diff_fragment(self.fragments[i], other.fragments[i]) for i in range(len(self.fragments))]) / len(
            self.fragments)
        return result


class Determinant:
    def __init__(self, levels=3, window_size=5, method_fragmentation=MethodFragmentation.cross):
        self.levels = levels
        self.window_size = window_size
        self.images = []
        self.groups = {}
        self.create_groups()

    def solve(self, image):
        image_crop = ImageCrops(image, self.levels, self.window_size)
        min_diff = 10**10
        tgroup = None
        for group in self.groups:
            for gimage in self.groups[group]:
                if diff := image_crop.diff(gimage) < min_diff:
                    min_diff = diff
                    tgroup = group

        return tgroup

    def create_groups(self):
        dirs = [d for d in os.listdir("cimages")]
        for dir in dirs:
            images = [Image.open(join("cimages", dir, f)) for f in os.listdir(join("cimages", dir))]
            self.groups[dir] = []
            for image in images:
                self.groups[dir].append(ImageCrops(image, self.levels, self.window_size))
