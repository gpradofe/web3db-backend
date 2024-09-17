from flask import Flask
from flask_restx import Api
from .config import Config
from .utils import setup_logging
import asyncio

app = Flask(__name__)
setup_logging(app)
api = Api(app, version='1.0', title='Web3DB API', description='A decentralized database system')

config = Config.get_config()

# Import and register blueprints/resources
from .app import peers_ns, query_ns
api.add_namespace(peers_ns)
api.add_namespace(query_ns)

# Initialize P2P manager
from .p2p_manager import create_p2p_manager
p2p_manager = None

@app.before_first_request
def start_p2p_manager():
    global p2p_manager
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    p2p_manager = loop.run_until_complete(create_p2p_manager())

# Initialize query engine
from .query_engine import query_engine

# Error handlers
from .utils import handle_error

@app.errorhandler(Exception)
def handle_exception(e):
    return handle_error(e)

# Additional initialization code can be added here

def create_app():
    return app