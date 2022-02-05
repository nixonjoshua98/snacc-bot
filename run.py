import sys
import os

sys.path.insert(0, os.path.join(os.getcwd(), "defectio"))

from src import SnaccBot

try:
    SnaccBot().run_with_token()
except KeyboardInterrupt as e:
    raise e
except Exception as e:
    print(f"Bot has crashed\n{e}")
