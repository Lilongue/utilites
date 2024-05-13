import unittest

from book import Book
from library import Library



class BookTest(unittest.TestCase):

    def test_from_string(self):
        book_string = "1;The Hitchhiker's Guide to the Galaxy;space,travel;path/to/book.txt;Douglas Adams"
        expected = Book(1, "The Hitchhiker's Guide to the Galaxy", ['space', 'travel'], 'path/to/book.txt', 'Douglas Adams')
        actual = Book.from_string(book_string)
        self.assertEqual(actual, expected)


class LibraryTest(unittest.TestCase):

    def test_load_books_from_file(self):
        library = Library()
        book_string1 = "1;The Hitchhiker's Guide to the Galaxy;space,travel;path/to/book.txt;Douglas Adams"
        book_string2 = "2;The Lord of the Rings;fantasy,adventure;path/to/lord_of_the_rings.txt;J.R. R. Tolkien"
        book1 = Book.from_string(book_string1)
        book2 = Book.from_string(book_string2)
        library.add_book(book1)
        library.add_book(book2)
        library.save_books_to_file('tmp_file')
        library2 = Library()
        library2.load_books_from_file('tmp_file')
        self.assertEqual(len(library2._books), 2)
        self.assertTrue(library2.get_books()[0] == book2 or library2.get_books()[1] == book2)
        

if __name__ == '__main__':
    unittest.main()
