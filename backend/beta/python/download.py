# download.py
from flask import Blueprint, send_from_directory, abort
import os

# Create a blueprint
download_bp = Blueprint('download', __name__)

# Define the path to the books directory
BOOKS_DIR = os.path.join(os.path.dirname(__file__), 'public', 'books')

@download_bp.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    """Serve a file for download."""
    try:
        return send_from_directory(BOOKS_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found")
