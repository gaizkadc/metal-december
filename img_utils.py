import datetime
import os

from PIL import Image, ImageFont, ImageDraw


def create_img(logger, aotd):
    logger.info('creating img')

    artist = aotd['artist']
    album = aotd['album']

    img_path = create_background(logger, aotd)
    write_header(logger, img_path, artist, album)
    draw_rectangle(logger, img_path)
    paste_cover(logger, img_path, aotd)

    return img_path


def create_background(logger, aotd):
    logger.info('creating background')

    imgs_folder = os.getenv('IMGS_FOLDER')
    if not os.path.exists(imgs_folder):
        os.makedirs(imgs_folder)

    output_format = os.getenv('OUTPUT_FORMAT')
    img_path = imgs_folder + '/' + str(aotd['day']) + '.' + output_format

    img = Image.new('RGB', get_img_size(logger), color='black')
    img.save(img_path)

    return img_path


def write_header(logger, img_path, artist, album):
    logger.info('writing header')

    img = Image.open(img_path)
    img_size = get_img_size(logger)
    cover_border_height = 730

    artist_font_size = get_text_width(logger, artist, img_size[0])
    album_font_size = get_text_width(logger, album, img_size[0])
    fonts_path = os.getenv('FONTS_PATH')
    header_font = fonts_path + '/Angel wish.ttf'

    artist_font = ImageFont.truetype(header_font, artist_font_size)
    album_font = ImageFont.truetype(header_font, album_font_size)

    draw = ImageDraw.Draw(img)

    artist_w, artist_h = draw.textsize(artist, font=artist_font)
    # artist_position = ((img_size[0] - artist_w) / 2, (img_size[1] - 2 * artist_h - cover_height) / 4)
    artist_position = ((img_size[0] - artist_w) / 2, (img_size[1] - cover_border_height) / 4 - artist_h / 2)

    album_w, album_h = draw.textsize(album, font=album_font)
    # album_position = ((img_size[0] - album_w) / 2, 10 * (img_size[1] - 2 * album_h - cover_height) / 4)
    album_position = ((img_size[0] - album_w) / 2,  (3 * img_size[1] + cover_border_height - 2 * album_h) / 4)
    text_color = 'white'

    draw.text(artist_position, artist, text_color, font=artist_font)
    draw.text(album_position, album, text_color, font=album_font)

    img.save(img_path)


def get_img_size(logger):
    logger.info('getting img size...')

    img_width = int(os.getenv('IMG_WIDTH'))
    img_height = int(os.getenv('IMG_HEIGHT'))

    return img_width, img_height


def paste_cover(logger, img_path, aotd):
    logger.info('writing cover...')

    img = Image.open(img_path)
    img_size = get_img_size(logger)

    cover_path = os.getenv('COVERS_PATH') + '/' + str(aotd['day']) + '.jpg'

    cover_size = 700, 700
    cover = Image.open(cover_path)
    cover = cover.resize(cover_size, Image.ANTIALIAS)

    cover_offset = int((img_size[0] - cover_size[0]) / 2), int((img_size[1] - cover_size[1]) / 2)
    img.paste(cover, cover_offset)

    img.save(img_path)


def get_text_width(logger, text, width):
    logger.info('getting text size...')

    text_width = width, width
    text_size = 400

    fonts_path = os.getenv('FONTS_PATH')
    font = fonts_path + '/Angel wish.ttf'

    while text_width[0] > 9 * width / 10 or text_size > 200:
        img = Image.new('RGB', text_width, color='black')
        draw = ImageDraw.Draw(img)

        text_font = ImageFont.truetype(font, text_size)
        text_width = draw.textsize(text, font=text_font)
        text_size -= 10

        img.close()

    return text_size


def draw_rectangle(logger, img_path):
    logger.info('drawing rectangle...')

    border = 30
    cover_width = 700
    rectangle_width = cover_width + border
    img_size = get_img_size(logger)
    shape = [((img_size[0] - rectangle_width) / 2, (img_size[1] - rectangle_width) / 2), ((img_size[0] + rectangle_width) / 2, (img_size[1] + rectangle_width) / 2)]

    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    draw.rectangle(shape, outline='white', width=5)

    img.save(img_path)
