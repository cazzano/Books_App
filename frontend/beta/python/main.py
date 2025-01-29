# main.py
from app import app  # Import your Dash app
from flask import Flask, jsonify
import sqlite3

# Create a Flask server
server = Flask(__name__)

# Expose the Dash app's server
server.wsgi_app = app.server

# Route to get all books
@server.route('/api/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    # Convert the books to a list of dictionaries
    books_list = [
        {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "category": book[3],
            "description": book[4],
            "icon": book[5],
            "text_color": book[6],
            "bg_color": book[7],
            "rating": book[8]
        }
        for book in books
    ]
    return jsonify(books_list)

if __name__ == '__main__':
    app.run_server(debug=False)  # This line is for local development only
