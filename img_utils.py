import os
import random

from PIL import Image, ImageFont, ImageDraw
from colorthief import ColorThief


def create_img(logger, aotd):
    logger.info('creating img')

    artist = aotd['artist']
    album = aotd['album']

    cover_path = os.getenv('COVERS_PATH') + '/' + str(aotd['day']) + '.jpg'
    img_path, palette = create_background(logger, aotd, cover_path)

    write_header(logger, img_path, artist, album, palette)
    draw_rectangle(logger, img_path, palette)
    paste_cover(logger, img_path, cover_path)

    return img_path


def create_background(logger, aotd, cover_path):
    logger.info('creating background')

    imgs_folder = os.getenv('IMGS_FOLDER')
    if not os.path.exists(imgs_folder):
        os.makedirs(imgs_folder)

    output_format = os.getenv('OUTPUT_FORMAT')
    img_path = imgs_folder + '/' + str(aotd['day']) + '.' + output_format

    palette = get_color_palette(logger, cover_path)

    img = Image.new('RGB', get_img_size(logger), color=palette[0])
    img.save(img_path)

    return img_path, palette


def write_header(logger, img_path, artist, album, palette):
    logger.info('writing header')

    img = Image.open(img_path)
    img_size = get_img_size(logger)
    cover_border_height = int(os.getenv('COVER_WIDTH')) + int(os.getenv('BORDER_WIDTH'))

    artist_font_size = get_text_width(logger, artist, img_size[0], palette)
    album_font_size = get_text_width(logger, album, img_size[0], palette)
    fonts_path = os.getenv('FONTS_PATH')
    header_font = fonts_path + '/Angel wish.ttf'

    artist_font = ImageFont.truetype(header_font, artist_font_size)
    album_font = ImageFont.truetype(header_font, album_font_size)

    draw = ImageDraw.Draw(img)

    artist_w, artist_h = draw.textsize(artist, font=artist_font)
    artist_position = ((img_size[0] - artist_w) / 2, (img_size[1] - cover_border_height) / 4 - artist_h / 2)

    album_w, album_h = draw.textsize(album, font=album_font)
    album_position = ((img_size[0] - album_w) / 2,  (3 * img_size[1] + cover_border_height - 2 * album_h) / 4)
    text_color = palette[1]

    draw.text(artist_position, artist, text_color, font=artist_font)
    draw.text(album_position, album, text_color, font=album_font)

    img.save(img_path)


def get_img_size(logger):
    logger.info('getting img size...')

    img_width = int(os.getenv('IMG_WIDTH'))
    img_height = int(os.getenv('IMG_HEIGHT'))

    return img_width, img_height


def paste_cover(logger, img_path, cover_path):
    logger.info('writing cover...')

    img = Image.open(img_path)
    img_size = get_img_size(logger)

    cover_width = int(os.getenv('COVER_WIDTH'))
    cover_size = cover_width, cover_width
    cover = Image.open(cover_path)
    cover = cover.resize(cover_size, Image.ANTIALIAS)

    cover_offset = int((img_size[0] - cover_size[0]) / 2), int((img_size[1] - cover_size[1]) / 2)
    img.paste(cover, cover_offset)

    img.save(img_path)


def get_text_width(logger, text, width, palette):
    logger.info('getting text size...')

    text_width = width, width
    text_size = 400

    fonts_path = os.getenv('FONTS_PATH')
    font = fonts_path + '/Angel wish.ttf'

    while text_width[0] > 9 * width / 10 or text_size > 200:
        img = Image.new('RGB', text_width, color=palette[0])
        draw = ImageDraw.Draw(img)

        text_font = ImageFont.truetype(font, text_size)
        text_width = draw.textsize(text, font=text_font)
        text_size -= 10

        img.close()

    return text_size


def draw_rectangle(logger, img_path, palette):
    logger.info('drawing rectangle...')

    border = int(os.getenv('BORDER_WIDTH'))
    cover_width = int(os.getenv('COVER_WIDTH'))
    rectangle_width = cover_width + border
    img_size = get_img_size(logger)
    shape = [((img_size[0] - rectangle_width) / 2, (img_size[1] - rectangle_width) / 2), ((img_size[0] + rectangle_width) / 2, (img_size[1] + rectangle_width) / 2)]

    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    draw.rectangle(shape, outline=palette[1], width=5)

    img.save(img_path)


def get_color_palette(logger, img_path):
    logger.info('getting color palette...')

    palette = []

    color_thief = ColorThief(img_path)

    palette_raw = color_thief.get_palette(color_count=2)

    for color_raw in palette_raw:
        r = color_raw[0]
        g = color_raw[1]
        b = color_raw[2]

        palette.append(rgb_to_hex(logger, int(r), int(g), int(b)))

    return palette


def get_random_color(logger):
    logger.info('getting random color...')

    return '#' + '%06x' % random.randint(0, 0xFFFFFF)


def rgb_to_hex(logger, r, g, b):
    logger.info('rgb to hexing...')

    r_hex = "0x{:02x}".format(r)
    g_hex = "0x{:02x}".format(g)
    b_hex = "0x{:02x}".format(b)

    hex_color = '#' + str(r_hex)[2:4] + str(g_hex)[2:4] + str(b_hex)[2:4]

    return hex_color
