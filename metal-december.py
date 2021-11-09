import utils
from dotenv import load_dotenv
load_dotenv()


# get logger
logger = utils.get_logger()

# get date
day = utils.get_day(logger)
year = utils.get_year(logger)

aotd = utils.get_aotd(logger, day, year)
if aotd is not None:
    caption = aotd['content']

logger.info(caption)