from book import Book


class Library:
    DEFAULT_LIB_FILE = 'library.log'

    def __init__(self):
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def remove_book(self, book):
        self._books.remove(book)

    def get_books(self):
        return self._books


    def save_books_to_file(self, filename=DEFAULT_LIB_FILE):
        with open(filename, "w", encoding='utf-8') as f:
            for book in self._books:
                f.write(f"{book.get_id()};{book.get_name()};{','.join(book.get_patterns())};{book.get_path()};{book.get_author()}\n")

    def load_books_from_file(self, filename):
        with open(filename, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                book = Book.from_string(line.strip())
                self._books.append(book)


if __name__ == '__main__':
    print('Library is building...')
