import img_utils
import utils
import twitter_utils
import ig_utils
import os
from dotenv import load_dotenv
load_dotenv()


# get logger
logger = utils.get_logger()

# get date
day = utils.get_day(logger)
year = utils.get_year(logger)

caption = ''

all_imgs = os.getenv('ALL_IMGS') == '1'

if all_imgs:
    logger.info('creating all imgs...')
    for i in range(1, 32):
        aotd = utils.get_aotd(logger, i, year)
        if aotd is not None:
            caption = aotd['content']

        logger.info(aotd)
        logger.info(caption)

        img_path = img_utils.create_img(logger, aotd)
        logger.info(img_path)

else:
    aotd = utils.get_aotd(logger, day, year)
    if aotd is not None:
        caption = aotd['content']

    logger.info(aotd)
    logger.info(caption)

    img_path = img_utils.create_img(logger, aotd)
    logger.info(img_path)

    # tweet img
    if os.getenv('TWITTER_POST') == '1':
        twitter_utils.tweet_img(logger, img_path, caption)

    # post collage to instagram
    if os.getenv('INSTAGRAM_POST') == '1':
        ig_utils.post_img(logger, img_path, caption)

    # done
    logger.info('done ✅')
