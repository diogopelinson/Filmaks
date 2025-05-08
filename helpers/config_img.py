import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH = os.path.join(BASE_DIR, '..', 'uploads')


os.makedirs(UPLOAD_PATH, exist_ok=True)