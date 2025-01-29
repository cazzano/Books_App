# main_backend.py
from flask import Flask, jsonify, request, abort
import sqlite3
import os

app = Flask(__name__)

# Database Connection Utility Functions
def get_db_connection():
    """Create a connection to the SQLite database"""
    try:
        conn = sqlite3.connect('books.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize the books database if it doesn't exist"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                icon TEXT,
                text_color TEXT,
                bg_color TEXT,
                rating REAL
            )
        ''')

        # Insert initial data if table is empty
        cursor.execute('SELECT COUNT(*) FROM books')
        if cursor.fetchone()[0] == 0:
            initial_books = [
                ("The Noble Quran", "Allah (Revealed to Prophet Muhammad)", "Holy Book",
                 "The central religious text of Islam", "fas fa-book-quran",
                 "text-green-600", "bg-green-100", 5.0),
                ("Sahih Al-Bukhari", "Imam Al-Bukhari", "Hadith",
                 "Most authentic hadith collection", "fas fa-scroll",
                 "text-blue-600", "bg-blue-100", 4.9),
                ("Riyad us-Saliheen", "Imam An-Nawawi", "Islamic Teachings",
                 "Gardens of the Righteous", "fas fa-mosque",
                 "text-red-600", "bg-red-100", 4.7)
            ]

            cursor.executemany('''
                INSERT INTO books
                (title, author, category, description, icon, text_color, bg_color, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', initial_books)

        conn.commit()
        conn.close()

# Initialize Database
init_database()

# Books CRUD Operations
@app.route('/api/books', methods=['GET'])
def get_books():
    """Retrieve all books or filter books"""
    conn = get_db_connection()
    if not conn:
        abort(500, description="Database connection failed")

    cursor = conn.cursor()

    # Optional query parameters
    category = request.args.get('category')
    search = request.args.get('search')

    query = "SELECT * FROM books WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if search:
        query += " AND (title LIKE ? OR author LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    cursor.execute(query, params)
    books = cursor.fetchall()
    conn.close()

    return jsonify([dict(book) for book in books])

@app.route('/api/books', methods=['POST'])
def add_book():
    """Add a new book to the database"""
    data = request.json

    if not all(key in data for key in ['title', 'author', 'category']):
        abort(400, description="Missing required fields")

    conn = get_db_connection()
    if not conn:
        abort(500, description="Database connection failed")

    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO books
            (title, author, category, description, icon, text_color, bg_color, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['title'],
            data['author'],
            data['category'],
            data.get('description', ''),
            data.get('icon', 'fas fa-book'),
            data.get('text_color', 'text-gray-600'),
            data.get('bg_color', 'bg-gray-100'),
            data.get('rating', 0.0)
        ))

        conn.commit()
        book_id = cursor.lastrowid
        conn.close()

        return jsonify({"message": "Book added successfully", "id": book_id}), 201

    except sqlite3.Error as e:
        conn.close()
        abort(500, description=f"Database error: {str(e)}")

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update an existing book"""
    data = request.json

    conn = get_db_connection()
    if not conn:
        abort(500, description="Database connection failed")

    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE books
            SET title = ?, author = ?, category = ?,
                description = ?, icon = ?, text_color = ?,
                bg_color = ?, rating = ?
            WHERE id = ?
        ''', (
            data.get('title', ''),
            data.get('author', ''),
            data.get('category', ''),
            data.get('description', ''),
            data.get('icon', ''),
            data.get('text_color', ''),
            data.get('bg_color', ''),
            data.get('rating', 0.0),
            book_id
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Book updated successfully"}), 200

    except sqlite3.Error as e:
        conn.close()
        abort(500, description=f"Database error: {str(e)}")

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book from the database"""
    conn = get_db_connection()
    if not conn:
        abort(500, description="Database connection failed")

    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Book deleted successfully"}), 200

    except sqlite3.Error as e:
        conn.close()
        abort(500, description=f"Database error: {str(e)}")

# Error Handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
