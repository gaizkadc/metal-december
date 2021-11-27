import os

from instabot import Bot


def post_img(logger, img_path, caption):
    logger.info('posting img')

    ig_bot = instagram_login(logger)

    ig_bot.upload_photo(img_path, caption=caption)

    logger.info('img posted')


def instagram_login(logger):
    logger.info('logging in instagram')

    ig_username = os.getenv('IG_USERNAME')
    ig_password = os.getenv('IG_PASSWORD')

    cookie_path = 'config/Fohoma_uuid_and_cookie.json'
    if os.path.exists(cookie_path):
        os.remove(cookie_path)

    bot = Bot()
    bot.login(username=ig_username, password=ig_password)

    return bot
