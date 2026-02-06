import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
