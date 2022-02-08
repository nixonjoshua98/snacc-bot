from src import SnaccBot
from src.logger import logger

try:
    SnaccBot().run_with_token()
except Exception as e:
    logger.exception(e)
