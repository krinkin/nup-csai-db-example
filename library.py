import sqlite3
from dataclasses import dataclass

@dataclass
class Author:
    id: int
    name: str

@dataclass
class Book:
    title: str
    author_id: int

class Library:
    def __init__(self):
        # Connect to SQLite database (creates it if doesn't exist)
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Create Authors table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

        # Create Books table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                title TEXT NOT NULL,
                author_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors (id)
            )
        ''')
        self.conn.commit()

    def add_author(self, author: Author):
        self.cursor.execute(
            'INSERT INTO authors (id, name) VALUES (?, ?)',
            (author.id, author.name)
        )
        self.conn.commit()

    def add_book(self, book: Book):
        self.cursor.execute(
            'INSERT INTO books (title, author_id) VALUES (?, ?)',
            (book.title, book.author_id)
        )
        self.conn.commit()

    def get_books_by_author(self, author_id: int):
        self.cursor.execute('''
            SELECT a.name, b.title
            FROM authors a
            JOIN books b ON a.id = b.author_id
            WHERE a.id = ?
        ''', (author_id,))
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()


def main():
    # Create library instance
    library = Library()

    # Add authors
    library.add_author(Author(0, "Tolkien"))
    library.add_author(Author(1, "Rowling"))

    # Add books
    library.add_book(Book("The Hobbit", 0))
    library.add_book(Book("Harry Potter", 1))
    library.add_book(Book("The Silmarillion", 0))

    # Find books by author
    books = library.get_books_by_author(0)
    print(f"Books by Tolkien:")
    for author_name, book_title in books:
        print(f"- {book_title}")


if __name__ == "__main__":
    main()
