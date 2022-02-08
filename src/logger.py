import logging.config
import os
from src import utils

LOG_FILE_DIR = "logs"  # Should match logging.json

os.makedirs(os.path.join(os.getcwd(), LOG_FILE_DIR), exist_ok=True)

logging.config.dictConfig(utils.load_yaml("logging.json"))

logger = logging.getLogger("Root.Logger")
