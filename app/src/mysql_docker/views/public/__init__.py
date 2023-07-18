'''
blueprint for this folder
'''

from flask import Blueprint

# create blueprint first
bp = Blueprint('public', __name__.split('.')[0], url_prefix='', static_folder='static/public', template_folder='templates/public')

# specific views
from . import home
