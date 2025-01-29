from app import app  # Import your Dash app
from flask import Flask

# Create a Flask server
server = Flask(__name__)

# Expose the Dash app's server
server.wsgi_app = app.server

if __name__ == '__main__':
    app.run_server(debug=False)  # This line is for local development only
