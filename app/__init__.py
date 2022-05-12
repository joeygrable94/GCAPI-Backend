import os
from dotenv import load_dotenv
from app.core.config import Settings
load_dotenv()

mode = os.environ.get('APP_MODE')
config = Settings()
