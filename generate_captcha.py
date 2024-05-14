import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import choices

import string

import os

template = Image.open("template.png")
font = ImageFont.truetype("segoeprint_bold.ttf", size=36)
def gen_captcha():
    image = template.copy()
    draw = ImageDraw.Draw(image)
    capcha = choices(string.digits, k=2) + choices(string.ascii_lowercase, k=2) + choices(string.ascii_uppercase, k=2)
    random.shuffle(capcha)
    capcha = ''.join(capcha)
    # draw.text((4, y), capcha , font=font, fill="gray")
    path = os.path.join('gen_captcha', capcha)
    if not os.path.exists(path):
        os.mkdir(path)
    offset = 3
    shadowColor = '#4d4d4d'

    imgWidth,imgHeight = image.size

    x = 5
    y = 5

    for off in range(offset):
        #move right
        draw.text((x-off, y), capcha, font=font, fill=shadowColor)
        #move left
        draw.text((x+off, y), capcha, font=font, fill=shadowColor)
        #move up
        draw.text((x, y+off), capcha, font=font, fill=shadowColor)
        #move down
        draw.text((x, y-off), capcha, font=font, fill=shadowColor)
        #diagnal left up
        draw.text((x-off, y+off), capcha, font=font, fill=shadowColor)
        #diagnal right up
        draw.text((x+off, y+off), capcha, font=font, fill=shadowColor)
        #diagnal left down
        draw.text((x-off, y-off), capcha, font=font, fill=shadowColor)
        #diagnal right down
        draw.text((x+off, y-off), capcha, font=font, fill=shadowColor)


    draw.text((x,y), capcha, font=font, fill="#fff")
    image.filter(ImageFilter.BLUR)
    image.filter(ImageFilter.MinFilter(3))
    image.save(f"{path}/{capcha}.jpg")
    for i in range(random.randint(2,3)):
        parts = random.randint(6,8)
        lly = random.randint(20, 50)
        for j in range(parts):
            llx = 160//parts*j
            lrx = 160//parts*(j+1)
            lry = 64 - random.randint(20, 50)
            draw.line((llx, lly, lrx, lry), fill=(255, 255, 255), width=3)
            lly = lry
    image.save(f"{path}/{capcha}_with_line.jpg")
    del draw

for i in range(2000):
    gen_captcha()
