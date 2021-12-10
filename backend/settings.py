import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE = {
    # 'ENGINE': 'postgresql',
    'NAME': os.getenv("DB_NAME"),
    'USER': os.getenv("DB_USER"),
    'PASSWORD': os.getenv("DB_PASSWORD"),
    # 'HOST': 'localhost',
    # 'PORT': '5432',
}
