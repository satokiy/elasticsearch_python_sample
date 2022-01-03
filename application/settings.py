import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ES_PASS = os.environ.get("ES_PASS")
RAKUTEN_APP_ID = os.environ.get("RAKUTEN_APP_ID")

