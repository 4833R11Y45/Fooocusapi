from flask import Flask
from apis.routes import api
import argparse
from modules.launch_util import prepare_environment
from modules.model_loader import load_file_from_url
import os
import modules.config as config
from modules.util import init_cache

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api/v1')
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen", type=str, default="0.0.0.0")  # Changed from --host to --listen
    parser.add_argument("--port", type=int, default=7865)
    args = parser.parse_args()

    # Initialize environment
    prepare_environment()

    # Initialize model cache
    init_cache()

    # Create and run app
    app = create_app()
    app.run(host=args.listen, port=args.port)  # Changed from args.host to args.listen