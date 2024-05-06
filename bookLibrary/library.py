class Library:

    def __init__(self):
        pass

    def get_books(self):
        """
        Get a list of books from the library.

        Returns:
            list: A list of book objects.
        """
        books = [
            {'title': 'Book 1', 'author': 'Author 1'},
            {'title': 'Book 2', 'author': 'Author 2'},
            {'title': 'Book 3', 'author': 'Author 3'},
        ]
        return books

    def search_books(self, query):
        """
        Search for books in the library.

        Args:
            query (str): The search query.

        Returns:
            list: A list of book objects that match the query.
        """
        results = []
        for book in self.get_books():
            if query in book['title']:
                results.append(book)
        return results

    def borrow_book(self, book):
        """
        Borrow a book from the library.

        Args:
            book (dict): The book to borrow.
        """
        book['borrowed'] = True