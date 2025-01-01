# controlnet_app.py
import os
import sys
from launch import prepare_environment, download_models
from args_manager import args
from apis.api import app
import uvicorn

def main():
    # Prepare environment
    prepare_environment()
    
    # Download required models
    download_models(args)
    
    # Set API port
    api_port = int(os.environ.get('API_PORT', 7866))
    
    # Run server
    uvicorn.run(app, host="0.0.0.0", port=api_port)

if __name__ == "__main__":
    main()
