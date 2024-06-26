import sqlite3
import sys
import os
sys.path.append(os.getcwd())

from booklibrary.book import Book

class BookDao:
    _db_file: str

    def __init__(self: 'BookDao', db_file: str) -> None:
        self._db_file = db_file

    def create_book(self: 'BookDao', book: Book) -> None:
        create_sql = 'INSERT INTO book(title, book_path, patterns, author, has_real_copy, periodic_number, publishing_year) VALUES (?, ?, ?, ?, ?, ?, ?)'
        with sqlite3.connect(self._db_file) as connection:
            cursor = connection.cursor()
            cursor.execute(create_sql, (book.get_name(), book.get_path(), ", ".join(book.get_patterns()), book.get_author(), book.get_has_real_copy(), book.get_periodic_number(), book.get_publishing_year()))
            connection.commit()


    def get_book(self: 'BookDao', book_id: int) -> Book:
        get_book_sql = 'SELECT * FROM book WHERE book_id = ?'
        with sqlite3.connect(self._db_file).cursor()as connection:
            cursor = connection.cursor()
            cursor.execute(get_book_sql, (book_id, ))
            return cursor.fetchone()


    def update_book(self: 'BookDao', book: Book) -> None:
        update_book_sql = 'UPDATE book SET title = ?, book_path = ?, patterns = ?, author = ?, has_real_copy = ?, periodic_number = ?, publishing_year = ? WHERE book_id = ?'
        with sqlite3.connect(self._db_file).cursor() as connection:
            cursor = connection.cursor()
            cursor.execute(update_book_sql, (book.get_name(), book.get_path(), ", ".join(book.get_patterns()), book.get_author(), book.get_has_real_copy(), book.get_periodic_number(), book.get_publishing_year(), book.get_id()))
            connection.commit()


    def delete_book(self: 'BookDao', book_id: int) -> None:
        delete_book_sql = 'DELETE * FROM book WHERE book_id = ?'
        with sqlite3.connect(self._db_file).cursor() as connection:
            cursor = connection.cursor()
            cursor.execute(delete_book_sql, (book_id, ))
            connection.commit()


    @property
    def db_file(self: 'BookDao') -> str:
        return self._db_file
