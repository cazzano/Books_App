# init_books.py
import sqlite3

def init_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Create a table for books
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
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

    # Insert initial book data
    books_data = [
        (1, "The Noble Quran", "Allah (Revealed to Prophet Muhammad)", "Holy Book", "The central religious text of Islam", "fas fa-book-quran", "text-green-600", "bg-green-100", 5.0),
        (2, "Sahih Al-Bukhari", "Imam Al-Bukhari", "Hadith", "Most authentic hadith collection", "fas fa-scroll", "text-blue-600", "bg-blue-100", 4.9),
        (3, "Riyad us-Saliheen", "Imam An-Nawawi", "Islamic Teachings", "Gardens of the Righteous", "fas fa-mosque", "text-red-600", "bg-red-100", 4.7)
    ]

    cursor.executemany('''
        INSERT INTO books (id, title, author, category, description, icon, text_color, bg_color, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', books_data)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
