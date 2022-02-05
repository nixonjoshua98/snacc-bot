import sys
import os

sys.path.insert(0, os.path.join(os.getcwd(), "defectio"))

from src import SnaccBot
from src.logger import logger

try:
    SnaccBot().run_with_token()
except Exception as e:
    logger.exception(e)
