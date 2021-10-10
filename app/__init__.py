from flask import *
from config import Config


def debug_message(message):
    if Config.DEBUG:
        print('DEBUG: {}'.format(message))


app = Flask(__name__)
app.config.from_object(Config)

from app import routes
