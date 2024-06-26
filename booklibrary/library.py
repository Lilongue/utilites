from book import Book


class Library:
    DEFAULT_LIB_FILE = 'library.log'

    def __init__(self: 'Library') -> None:
        self._books = []

    def add_book(self: 'Library', book: Book) -> None:
        self._books.append(book)

    def remove_book(self: 'Library', book: Book) -> None:
        self._books.remove(book)

    def get_books(self: 'Library') -> list[Book]:
        return self._books

    def get_books_names(self: 'Library') -> list[str]:
        return [book.get_name() for book in self._books]

    def get_books_patterns(self: 'Library') -> list[str]:
        return [book.get_patterns() for book in self._books]

    def get_books_authors(self: 'Library') -> list[str]:
        return [book.get_author() for book in self._books]

    def get_books_paths(self: 'Library') -> list[str]:
        return [book.get_path() for book in self._books]

    def save_books_to_file(self: 'Library', filename: str = DEFAULT_LIB_FILE) -> None:
        with open(filename, "w", encoding='utf-8') as f:
            for book in self._books:
                f.write(f"{book.get_id()};{book.get_name()};{','.join(book.get_patterns())};{book.get_path()};{book.get_author()}\n")

    def load_books_from_file(self: 'Library', filename: str = DEFAULT_LIB_FILE) -> None:
        with open(filename, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                book = Book.from_string(line.strip())
                self._books.append(book)
