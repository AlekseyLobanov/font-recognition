#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import tempfile
from collections import Counter
import json

import PIL
from PIL import ImageDraw, ImageFont

import settings


def generatePhrase():
    return ''.join([random.choice(settings.SYMBOLS_TO_PROCESS + ' ') for _ in range(random.randint(5,10))])


def getImageWithText(text, font_name, font_size=16):
    cur_font = PIL.ImageFont.truetype(font_name, 20)

    # Временная картинка, чтобы получить размер текста
    tmp_img = PIL.Image.new('RGBA', (100,100), (255,255,255,0))
    pil_draw = PIL.ImageDraw.Draw(tmp_img)
    text_size = pil_draw.textsize(text, cur_font)

    img_size = (text_size[0] + 10, text_size[1] + 10)
    img = PIL.Image.new('RGB', img_size, (255,255,255))
    pil_draw = ImageDraw.Draw(img)
    pil_draw.text((5,5), text, fill=(0,0,0), font=cur_font)
    return img


def main():
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    error_count = Counter()  # Количество ошибок по каждому из шрифтовы

    img_index = 1
    img_info = {}  # Сюда запишем информацию по каждому из индексов

    # Пишем по одному разу каждую букву каждого шрифта
    for font_name in settings.FONTS_TO_PROCESS:
        for symbol in settings.SYMBOLS_TO_PROCESS:
            for font_size in settings.FONTS_SIZES:
                try:
                    img = getImageWithText(symbol, font_name)
                    img.save('{}/{}.png'.format(temp_path,img_index),'PNG')
                    img_info[img_index] = {'font':font_name, 'symbol':symbol, 'size':font_size}
                except IOError:
                    error_count[font_name] += 1
                img_index += 1

    # Создаём тестовые данные: сколько-то фраз на каждый шрифт
    for font_name in settings.FONTS_TO_PROCESS:
        for _ in range(settings.NUMBER_OF_TEST_EXAMPLES_PER_FONT):
            try:
                font_size = random.choice(settings.FONTS_TO_PROCESS)
                phrase = generatePhrase()
                img = getImageWithText(phrase, font_name)
                img.save('{}/{}.png'.format(temp_path,img_index),'PNG')
                img_info[img_index] = {'font':font_name, 'phrase':phrase, 'size':font_size}
            except IOError:
                error_count[font_name] += 1
            img_index += 1

    with open('{}/info.json'.format(temp_path),'w') as f:
        json.dump(img_info, f)

    print('Data stores in {}'.format(temp_path))
    if len(error_count) != 0:
        print('Errors: ')
        print(error_count)

if __name__ == "__main__":
    main()
