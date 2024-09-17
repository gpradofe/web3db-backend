import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    file_handler = RotatingFileHandler(f'{log_dir}/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Web3DB startup')

def handle_error(e):
    return {'error': str(e)}, 500