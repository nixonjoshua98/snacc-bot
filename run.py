import sys
import os

if os.path.isdir(fp := os.path.join(os.getcwd(), "defectio")):
    sys.path.insert(0, fp)

from src import SnaccBot
from src.logger import logger

try:
    SnaccBot().run_with_token()
except Exception as e:
    logger.exception(e)
